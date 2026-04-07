"""
🔗 Orchestrator API
Интеграция с Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, send_file
from orchestrator.core.database import Database, ProjectStatus, TaskStatus
from orchestrator.agents.teamlead_agent import TeamLeadAgent
from orchestrator.core.project_manager import ProjectManager
from orchestrator.core.task_executor import TaskExecutor
from orchestrator.core.deploy_agent import deploy_project_api, get_deployed_projects_api, undeploy_project_api
from orchestrator.core.github_client import get_github_client

# Создаём Blueprint
orchestrator_bp = Blueprint('orchestrator', __name__, url_prefix='/api/orchestrator')

# Инициализация
db = Database()
teamlead = TeamLeadAgent(db)
project_manager = ProjectManager(db)


# ========== Проекты ==========

@orchestrator_bp.route('/projects', methods=['POST'])
def create_project():
    """Создать новый проект"""
    data = request.get_json()
    
    tz_text = data.get('tz_text')
    project_name = data.get('project_name')
    
    if not tz_text:
        return jsonify({'error': 'ТЗ не может быть пустым'}), 400
    
    result = teamlead.process_request(tz_text, project_name)
    return jsonify(result)


@orchestrator_bp.route('/projects', methods=['GET'])
def list_projects():
    """Список всех проектов"""
    projects = db.get_all_projects()
    return jsonify({
        'projects': [p.to_dict() for p in projects],
        'count': len(projects)
    })


@orchestrator_bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    """Информация о проекте"""
    project = db.get_project(project_id)
    if not project:
        return jsonify({'error': 'Проект не найден'}), 404
    
    tasks = db.get_tasks_by_project(project_id)
    status = teamlead.check_project_status(project_id)
    
    return jsonify({
        'project': project.to_dict(),
        'tasks': [t.to_dict() for t in tasks],
        'status': status
    })


@orchestrator_bp.route('/projects/<project_id>/status', methods=['GET'])
def get_project_status(project_id):
    """Статус проекта"""
    status = teamlead.check_project_status(project_id)
    return jsonify(status)


# ========== Задачи ==========

@orchestrator_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """Список задач"""
    project_id = request.args.get('project_id')
    agent_type = request.args.get('agent_type')
    status = request.args.get('status')
    
    if project_id:
        tasks = db.get_tasks_by_project(project_id)
    elif status == 'pending':
        tasks = db.get_pending_tasks(agent_type)
    else:
        # Все задачи (ограничим 100)
        return jsonify({'error': 'Укажите project_id или status=pending'}), 400
    
    return jsonify({
        'tasks': [t.to_dict() for t in tasks],
        'count': len(tasks)
    })


@orchestrator_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Информация о задаче"""
    task = db.get_task(task_id)
    if not task:
        return jsonify({'error': 'Задача не найдена'}), 404
    
    return jsonify(task.to_dict())


@orchestrator_bp.route('/tasks/<task_id>/assign', methods=['POST'])
def assign_task(task_id):
    """Назначить задачу агенту"""
    data = request.get_json()
    agent_id = data.get('agent_id')
    
    if not agent_id:
        return jsonify({'error': 'agent_id обязателен'}), 400
    
    result = teamlead.assign_task(task_id, agent_id)
    return jsonify({'success': result})


@orchestrator_bp.route('/tasks/<task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    """Обновить статус задачи"""
    data = request.get_json()
    new_status = data.get('status')
    artifacts = data.get('artifacts', {})
    
    if not new_status:
        return jsonify({'error': 'status обязателен'}), 400
    
    try:
        status = TaskStatus(new_status)
        db.update_task_status(task_id, status, artifacts=artifacts)
        return jsonify({'success': True, 'status': new_status})
    except ValueError:
        return jsonify({'error': f'Неверный статус: {new_status}'}), 400


# ========== Сборка и деплой ==========

@orchestrator_bp.route('/projects/<project_id>/build', methods=['POST'])
def build_project(project_id):
    """Собрать проект в ZIP"""
    result = project_manager.build_project(project_id)
    return jsonify(result)


@orchestrator_bp.route('/projects/<project_id>/download', methods=['GET'])
def download_project(project_id):
    """Скачать ZIP проекта"""
    zip_path = project_manager.projects_dir / f"{project_id}.zip"
    
    if not zip_path.exists():
        return jsonify({'error': 'ZIP не найден. Сначала соберите проект.'}), 404
    
    return send_file(
        zip_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"project-{project_id}.zip"
    )


@orchestrator_bp.route('/projects/<project_id>/deploy', methods=['POST'])
def deploy_project(project_id):
    """Деплоить проект на хостинг"""
    data = request.get_json()
    hosting_config = data.get('hosting_config', {})
    
    result = project_manager.deploy_to_hosting(project_id, hosting_config)
    return jsonify(result)


@orchestrator_bp.route('/builds', methods=['GET'])
def list_builds():
    """Список собранных проектов"""
    builds = project_manager.list_builds()
    return jsonify({'builds': builds, 'count': len(builds)})


# ========== Отчёты ==========

@orchestrator_bp.route('/projects/<project_id>/report', methods=['GET'])
def get_project_report(project_id):
    """Получить отчёт о проекте"""
    report = teamlead.generate_project_report(project_id)
    return jsonify({'report': report})


# ========== Статистика ==========

@orchestrator_bp.route('/stats', methods=['GET'])
def get_stats():
    """Статистика оркестратора"""
    projects = db.get_all_projects()
    
    total = len(projects)
    completed = sum(1 for p in projects if p.status == ProjectStatus.COMPLETED)
    in_progress = sum(1 for p in projects if p.status == ProjectStatus.IN_PROGRESS)
    
    # Подсчитаем задачи
    total_tasks = 0
    completed_tasks = 0
    
    for project in projects:
        tasks = db.get_tasks_by_project(project.id)
        total_tasks += len(tasks)
        completed_tasks += sum(1 for t in tasks if t.status == TaskStatus.DONE)
    
    return jsonify({
        'projects': {
            'total': total,
            'completed': completed,
            'in_progress': in_progress
        },
        'tasks': {
            'total': total_tasks,
            'completed': completed_tasks,
            'progress': round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0
        }
    })


# ========== Инициализация БД ==========

@orchestrator_bp.route('/init', methods=['POST'])
def init_database():
    """Инициализировать базу данных"""
    try:
        db.init_db()
        return jsonify({'success': True, 'message': 'База данных инициализирована'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== Task Execution ==========

@orchestrator_bp.route('/tasks/<task_id>/execute', methods=['POST'])
def execute_task(task_id):
    """Выполнить задачу"""
    executor = TaskExecutor(db)
    result = executor.execute_task(task_id)
    return jsonify(result)


@orchestrator_bp.route('/execute-pending', methods=['POST'])
def execute_pending():
    """Выполнить все ожидающие задачи"""
    data = request.get_json() or {}
    agent_type = data.get('agent_type')
    
    executor = TaskExecutor(db)
    results = executor.execute_pending_tasks(agent_type)
    
    return jsonify({
        'executed': len(results),
        'results': results
    })


# ========== Deploy ==========

@orchestrator_bp.route('/projects/<project_id>/deploy', methods=['POST'])
def deploy_project_endpoint(project_id):
    """Деплой проекта на сервер"""
    result = deploy_project_api(project_id, db)
    return jsonify(result)


@orchestrator_bp.route('/projects/<project_id>/undeploy', methods=['POST'])
def undeploy_project_endpoint(project_id):
    """Снять проект с публикации"""
    result = undeploy_project_api(project_id, db)
    return jsonify(result)


@orchestrator_bp.route('/deployed', methods=['GET'])
def get_deployed_projects_endpoint():
    """Получить список развёрнутых проектов"""
    projects = get_deployed_projects_api(db)
    return jsonify({'projects': projects})


# ========== GitHub Integration ==========

@orchestrator_bp.route('/github/sync-project/<project_id>', methods=['POST'])
def sync_project_to_github(project_id):
    """Синхронизировать проект с GitHub Projects и Issues"""
    try:
        # Получаем проект и задачи
        project = db.get_project(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Проект не найден'}), 404
        
        tasks = db.get_tasks_by_project(project_id)
        
        # Преобразуем задачи в dict
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'agent_type': task.agent_type,
                'status': task.status.value if hasattr(task.status, 'value') else task.status,
                'priority': task.priority,
                'description': task.description,
                'project_id': task.project_id
            })
        
        # Синхронизируем с GitHub
        client = get_github_client()
        result = client.sync_project_to_github(
            {'name': project.name, 'description': project.description or ''},
            tasks_data
        )
        
        return jsonify({
            'success': True,
            'message': '✅ Проект синхронизирован с GitHub!',
            'github_project_url': result['project']['html_url'],
            'issues_created': result['total'],
            'project': result['project']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@orchestrator_bp.route('/github/issues', methods=['GET'])
def get_github_issues():
    """Получить список задач из GitHub"""
    try:
        client = get_github_client()
        state = request.args.get('state', 'open')
        issues = client.list_issues(state=state)
        return jsonify({'success': True, 'issues': issues, 'count': len(issues)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@orchestrator_bp.route('/github/create-issue', methods=['POST'])
def create_github_issue():
    """Создать задачу в GitHub"""
    try:
        data = request.get_json()
        client = get_github_client()
        
        issue = client.create_issue(
            title=data.get('title'),
            body=data.get('body', ''),
            labels=data.get('labels', []),
            assignee=data.get('assignee')
        )
        
        return jsonify({
            'success': True,
            'message': '✅ Задача создана в GitHub!',
            'issue_url': issue['html_url'],
            'issue': issue
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@orchestrator_bp.route('/github/push-file', methods=['POST'])
def push_file_to_github():
    """Загрузить файл в репозиторий GitHub"""
    try:
        data = request.get_json()
        client = get_github_client()
        
        result = client.create_or_update_file(
            path=data.get('path'),
            content=data.get('content'),
            message=data.get('message', 'Update from AI Правительство'),
            branch=data.get('branch', 'main')
        )
        
        return jsonify({
            'success': True,
            'message': '✅ Файл загружен в GitHub!',
            'file_url': result['content']['html_url'] if 'content' in result else None,
            'commit': result.get('commit', {})
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== Agent Chat ==========

@orchestrator_bp.route('/agent/<agent_type>/chat', methods=['POST'])
def chat_with_agent(agent_type):
    """Чат с агентом"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        # Получаем информацию об агенте
        agent_info = {
            'frontend': {
                'name': 'Frontend Agent',
                'role': 'Frontend Developer',
                'icon': '🎨',
                'description': 'Создаёт HTML, CSS, JavaScript код'
            },
            'backend': {
                'name': 'Backend Agent',
                'role': 'Backend Developer',
                'icon': '⚙️',
                'description': 'Создаёт серверный код, API'
            },
            'devops': {
                'name': 'DevOps Agent',
                'role': 'DevOps Engineer',
                'icon': '🚀',
                'description': 'Настраивает Docker, CI/CD'
            },
            'content': {
                'name': 'Content Agent',
                'role': 'Content Manager',
                'icon': '📝',
                'description': 'Создаёт документацию'
            },
            'design': {
                'name': 'Design Agent',
                'role': 'UI/UX Designer',
                'icon': '✨',
                'description': 'Создаёт дизайн и макеты'
            }
        }
        
        info = agent_info.get(agent_type, {
            'name': f'{agent_type.title()} Agent',
            'role': 'AI Agent',
            'icon': '🤖',
            'description': 'AI агент'
        })
        
        # Формируем ответ от агента
        if 'привет' in message.lower() or 'hello' in message.lower():
            reply = f"{info['icon']} Привет! Я {info['name']}. {info['description']}. Чем могу помочь?"
        elif 'что ты умеешь' in message.lower() or 'skills' in message.lower():
            reply = f"{info['icon']} Я {info['role']}. Моя задача — {info['description']}. Могу выполнять задачи из очереди и генерировать код."
        elif 'задачи' in message.lower() or 'tasks' in message.lower():
            # Получаем задачи для этого агента
            tasks = db.get_pending_tasks(agent_type)
            if tasks:
                reply = f"{info['icon']} У меня {len(tasks)} задач в очереди:\n"
                for i, task in enumerate(tasks[:5], 1):
                    reply += f"{i}. {task.title}\n"
            else:
                reply = f"{info['icon']} У меня нет задач в очереди. Всё выполнено! ✅"
        elif 'выполни' in message.lower() or 'execute' in message.lower():
            # Выполняем первую ожидающую задачу
            executor = TaskExecutor(db)
            results = executor.execute_pending_tasks(agent_type)
            if results:
                result = results[0]
                if result['success']:
                    reply = f"{info['icon']} ✅ Выполнил задачу '{result['task_title']}'! {result.get('message', '')}"
                else:
                    reply = f"{info['icon']} ❌ Ошибка: {result.get('message', 'Неизвестная ошибка')}"
            else:
                reply = f"{info['icon']} Нет задач для выполнения."
        else:
            reply = f"{info['icon']} Я понял: \"{message}\". Для выполнения задач используй кнопку '▶️ Выполнить' в проекте, или напиши 'выполни задачи'."
        
        return jsonify({
            'success': True,
            'agent': agent_type,
            'agent_info': info,
            'reply': reply,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== GitHub Projects v2 ==========

@orchestrator_bp.route('/github/sync-project-v2/<project_id>', methods=['POST'])
def sync_project_v2(project_id):
    """
    Синхронизация проекта с GitHub Projects v2 (GraphQL)
    Новое поколение Projects с автоматизацией
    """
    try:
        from orchestrator.core.github_projects_v2 import GitHubProjectsV2
        
        # Получаем проект и задачи
        project = db.get_project(project_id)
        if not project:
            return jsonify({'error': 'Проект не найден'}), 404
        
        tasks = db.get_tasks_by_project(project_id)
        if not tasks:
            return jsonify({'error': 'Нет задач для синхронизации'}), 400
        
        # Конвертируем задачи в формат для GitHub
        github_tasks = []
        for task in tasks:
            priority_map = {5: 'High', 4: 'High', 3: 'Medium', 2: 'Low', 1: 'Low'}
            github_tasks.append({
                'title': task.title,
                'description': f"{task.description}\n\n**ID задачи:** {task.id}\n**Тип агента:** {task.agent_type}",
                'agent_type': task.agent_type,
                'priority': priority_map.get(task.priority, 'Medium')
            })
        
        # Создаём клиент и синхронизируем
        client = GitHubProjectsV2()
        result = client.sync_project_with_github(
            ai_project_id=project_id,
            ai_project_name=project.name,
            tasks=github_tasks
        )
        
        return jsonify({
            'success': True,
            'message': f'✅ Проект синхронизирован с GitHub Projects v2',
            'github_project_url': result['project_url'],
            'project_number': result['project_number'],
            'issues_created': result['issues_created'],
            'tasks': [t.title for t in tasks]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '❌ Ошибка синхронизации с GitHub Projects v2'
        }), 500
