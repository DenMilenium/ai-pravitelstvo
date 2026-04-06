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
