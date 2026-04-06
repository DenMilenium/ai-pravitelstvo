"""
👑 TeamLead-Agent
Главный диспетчер AI Правительства
Анализирует ТЗ, создаёт задачи, назначает министерства, контролирует выполнение
"""

import uuid
import json
from datetime import datetime
from typing import List, Dict, Optional
import sys
import os

# Добавляем путь к агентам
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from orchestrator.core.database import Database, Project, Task, ProjectStatus, TaskStatus


class TeamLeadAgent:
    """
    👑 TeamLead-Agent
    
    Роль: Главный архитектор и координатор проектов
    Задачи:
    - Принимает ТЗ от заказчика
    - Разбивает на подзадачи
    - Назначает министерства (агентов)
    - Следит за выполнением
    - Собирает финальный результат
    """
    
    NAME = "👑 TeamLead-Agent"
    ROLE = "Chief Architect & Project Coordinator"
    EXPERTISE = ["Project Planning", "Task Decomposition", "Team Coordination", "Quality Control"]
    
    # Типы агентов для разных задач
    AGENT_TYPES = {
        'frontend': ['frontend_agent', 'ui_agent', 'ux_agent', 'react_agent', 'vue_agent'],
        'backend': ['backend_agent', 'django_agent', 'laravel_agent', 'api_agent', 'database_agent'],
        'fullstack': ['fullstack_agent', 'nextjs_agent', 'mern_agent'],
        'design': ['figma_agent', 'ui_agent', 'threejs_agent'],
        'mobile': ['mobile_agent', 'ios_agent', 'android_agent', 'react_native_agent'],
        'desktop': ['pyqt_agent', 'electron_agent', 'tauri_agent', 'wpf_agent'],
        'devops': ['docker_agent', 'k8s_agent', 'nginx_agent', 'ci_cd_agent'],
        'ai': ['ml_agent', 'data_agent', 'chatbot_agent', 'ai_integration_agent'],
        'cloud': ['aws_agent', 'azure_agent', 'gcp_agent', 'yandex_cloud_agent', 'serverless_agent'],
        'security': ['secops_agent', 'auth_agent', 'security_scanner_agent'],
        'marketing': ['seo_agent', 'marketer_agent', 'ad_agent', 'analytics_agent'],
        'content': ['cms_agent', 'techwriter_agent', 'docsgenerator_agent']
    }
    
    def __init__(self, db: Database = None):
        self.db = db or Database()
    
    def process_request(self, tz_text: str, project_name: str = None) -> Dict:
        """
        Главный метод: принимает ТЗ и запускает проект
        
        Args:
            tz_text: Техническое задание (описание проекта)
            project_name: Название проекта (если не указано — сгенерирует)
            
        Returns:
            Dict с информацией о созданном проекте
        """
        # Создаём проект
        project_id = str(uuid.uuid4())[:8]
        project_name = project_name or f"Проект-{project_id}"
        
        project = Project(
            id=project_id,
            name=project_name,
            description=self._extract_summary(tz_text),
            tz_text=tz_text,
            status=ProjectStatus.PLANNING,
            tasks=[],
            created_at=datetime.now().isoformat()
        )
        
        self.db.create_project(project)
        
        # Анализируем ТЗ и создаём задачи
        tasks = self._analyze_tz_and_create_tasks(project_id, tz_text)
        
        # Обновляем проект со списком задач
        project.tasks = [task.id for task in tasks]
        
        return {
            'success': True,
            'project_id': project_id,
            'project_name': project_name,
            'tasks_count': len(tasks),
            'tasks': [task.to_dict() for task in tasks],
            'message': f'✅ Проект "{project_name}" создан. Назначено {len(tasks)} задач.'
        }
    
    def _extract_summary(self, tz_text: str) -> str:
        """Извлекает краткое описание из ТЗ"""
        # Первая строка или первые 100 символов
        first_line = tz_text.split('\n')[0][:100]
        return first_line if first_line else tz_text[:100]
    
    def _analyze_tz_and_create_tasks(self, project_id: str, tz_text: str) -> List[Task]:
        """
        Анализирует ТЗ и создаёт задачи для разных министерств
        """
        tasks = []
        tz_lower = tz_text.lower()
        
        # === Анализ типа проекта ===
        
        # Веб-сайт
        if any(word in tz_lower for word in ['сайт', 'веб', 'web', 'landing', 'лендинг', 'корпоративный', 'магазин']):
            
            # Дизайн
            if any(word in tz_lower for word in ['дизайн', 'figma', 'макет']):
                tasks.append(self._create_task(
                    project_id, "UI/UX Дизайн", 
                    "Создать макеты интерфейса в Figma",
                    "design", priority=5
                ))
            
            # Frontend
            tasks.append(self._create_task(
                project_id, "Frontend разработка",
                "Создать клиентскую часть сайта (HTML, CSS, JS/React)",
                "frontend", priority=5,
                dependencies=[tasks[-1].id] if tasks else []
            ))
            
            # Backend (если нужен)
            if any(word in tz_lower for word in ['админка', 'база данных', 'формы', 'авторизация', 'api']):
                tasks.append(self._create_task(
                    project_id, "Backend разработка",
                    "Создать серверную часть (API, база данных)",
                    "backend", priority=4,
                    dependencies=[tasks[-1].id]
                ))
            
            # DevOps/Деплой
            tasks.append(self._create_task(
                project_id, "DevOps и деплой",
                "Настроить сервер, контейнеризацию, деплой",
                "devops", priority=3,
                dependencies=[t.id for t in tasks[-2:]]
            ))
        
        # Мобильное приложение
        elif any(word in tz_lower for word in ['приложение', 'app', 'android', 'ios', 'мобильное']):
            
            tasks.append(self._create_task(
                project_id, "Мобильная разработка",
                "Создать мобильное приложение",
                "mobile", priority=5
            ))
            
            if any(word in tz_lower for word in ['backend', 'api', 'сервер']):
                tasks.append(self._create_task(
                    project_id, "Backend для приложения",
                    "API для мобильного приложения",
                    "backend", priority=4,
                    dependencies=[tasks[-1].id]
                ))
        
        # Десктопное приложение
        elif any(word in tz_lower for word in ['программа', 'приложение для windows', 'desktop', 'клиент']):
            tasks.append(self._create_task(
                project_id, "Десктопное приложение",
                "Создать приложение для ПК",
                "desktop", priority=5
            ))
        
        # AI/ML проект
        elif any(word in tz_lower for word in ['нейросеть', 'ai', 'ml', 'машинное обучение', 'чат-бот', 'анализ данных']):
            tasks.append(self._create_task(
                project_id, "AI/ML разработка",
                "Создать модель машинного обучения",
                "ai", priority=5
            ))
            
            if any(word in tz_lower for word in ['интерфейс', 'веб', 'сайт']):
                tasks.append(self._create_task(
                    project_id, "Frontend для AI",
                    "Интерфейс для взаимодействия с моделью",
                    "frontend", priority=4
                ))
        
        # Если не определили тип — создаём универсальный набор
        else:
            tasks.append(self._create_task(
                project_id, "Анализ и планирование",
                "Детальный анализ требований и создание плана",
                "frontend", priority=5  # Используем как аналитика
            ))
        
        # === Дополнительные задачи ===
        
        # SEO/Маркетинг
        if any(word in tz_lower for word in ['seo', 'продвижение', 'реклама', 'маркетинг']):
            tasks.append(self._create_task(
                project_id, "SEO и маркетинг",
                "Настроить SEO, аналитику",
                "marketing", priority=3
            ))
        
        # Безопасность
        if any(word in tz_lower for word in ['безопасность', 'защита', 'ssl', 'шифрование']):
            tasks.append(self._create_task(
                project_id, "Безопасность",
                "Настроить аутентификацию, защиту данных",
                "security", priority=4
            ))
        
        # Документация
        tasks.append(self._create_task(
            project_id, "Документация",
            "Создать README, документацию по развёртыванию",
            "content", priority=2,
            dependencies=[t.id for t in tasks]
        ))
        
        # Сохраняем задачи в БД
        for task in tasks:
            self.db.create_task(task)
        
        return tasks
    
    def _create_task(self, project_id: str, title: str, description: str,
                    agent_type: str, priority: int = 3, 
                    dependencies: List[str] = None) -> Task:
        """Создаёт задачу"""
        return Task(
            id=str(uuid.uuid4())[:8],
            project_id=project_id,
            title=title,
            description=description,
            agent_type=agent_type,
            status=TaskStatus.PENDING,
            priority=priority,
            dependencies=dependencies or [],
            artifacts={},
            created_at=datetime.now().isoformat()
        )
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """
        Назначает задачу конкретному агенту
        """
        self.db.update_task_status(
            task_id, 
            TaskStatus.ASSIGNED,
            assigned_to=agent_id
        )
        
        # Отправляем сообщение в шину
        self.db.send_message(
            task_id=task_id,
            agent_type=self.db.get_task(task_id).agent_type,
            message_type='assign',
            payload={'agent_id': agent_id, 'task_id': task_id}
        )
        
        return True
    
    def check_project_status(self, project_id: str) -> Dict:
        """
        Проверяет статус проекта и прогресс
        """
        project = self.db.get_project(project_id)
        if not project:
            return {'error': 'Проект не найден'}
        
        tasks = self.db.get_tasks_by_project(project_id)
        
        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == TaskStatus.DONE)
        in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
        pending = sum(1 for t in tasks if t.status == TaskStatus.PENDING)
        failed = sum(1 for t in tasks if t.status == TaskStatus.FAILED)
        
        progress = (completed / total * 100) if total > 0 else 0
        
        # Проверяем, все ли задачи выполнены
        if completed == total and total > 0:
            self.db.update_project_status(project_id, ProjectStatus.COMPLETED)
            status_message = "✅ Проект завершён!"
        elif failed > 0:
            status_message = f"⚠️ Есть ошибки ({failed} задач)"
        elif in_progress > 0:
            status_message = f"🚀 В работе ({in_progress} задач)"
        else:
            status_message = f"⏳ Ожидание ({pending} задач)"
        
        return {
            'project_id': project_id,
            'project_name': project.name,
            'status': project.status.value,
            'progress': f"{progress:.1f}%",
            'tasks_total': total,
            'tasks_completed': completed,
            'tasks_in_progress': in_progress,
            'tasks_pending': pending,
            'tasks_failed': failed,
            'message': status_message,
            'tasks': [task.to_dict() for task in tasks]
        }
    
    def get_ready_projects(self) -> List[Dict]:
        """
        Возвращает проекты, готовые к сборке (все задачи DONE)
        """
        projects = self.db.get_all_projects()
        ready = []
        
        for project in projects:
            if project.status == ProjectStatus.COMPLETED:
                ready.append({
                    'id': project.id,
                    'name': project.name,
                    'created_at': project.created_at,
                    'tasks_count': len(project.tasks)
                })
        
        return ready
    
    def generate_project_report(self, project_id: str) -> str:
        """
        Генерирует отчёт о проекте в Markdown
        """
        project = self.db.get_project(project_id)
        tasks = self.db.get_tasks_by_project(project_id)
        artifacts = self.db.get_project_artifacts(project_id)
        
        report = f"""# 📊 Отчёт по проекту: {project.name}

## 📝 Техническое задание
{project.tz_text}

## 📈 Статистика
- **Создан**: {project.created_at}
- **Статус**: {project.status.value}
- **Всего задач**: {len(tasks)}
- **Выполнено**: {sum(1 for t in tasks if t.status == TaskStatus.DONE)}
- **Артефактов**: {len(artifacts)}

## 📋 Задачи
"""
        
        for task in tasks:
            status_emoji = {
                TaskStatus.DONE: "✅",
                TaskStatus.IN_PROGRESS: "🚀",
                TaskStatus.PENDING: "⏳",
                TaskStatus.FAILED: "❌"
            }.get(task.status, "❓")
            
            report += f"\n### {status_emoji} {task.title}\n"
            report += f"- **Тип**: {task.agent_type}\n"
            report += f"- **Описание**: {task.description}\n"
            report += f"- **Статус**: {task.status.value}\n"
            
            if task.artifacts:
                report += f"- **Файлы**: {', '.join(task.artifacts.keys())}\n"
        
        report += f"\n\n## 📁 Артефакты\n"
        for art in artifacts:
            report += f"- `{art['file_name']}` ({art['file_type']})\n"
        
        return report


if __name__ == "__main__":
    # Тест
    agent = TeamLeadAgent()
    
    result = agent.process_request(
        tz_text="Создать сайт для юридической конторы. Нужен лендинг с формой обратной связи, описанием услуг, разделом о компании. Дизайн должен быть строгим и деловым.",
        project_name="Сайт ЮрКонсульт"
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Проверяем статус
    status = agent.check_project_status(result['project_id'])
    print("\n" + json.dumps(status, indent=2, ensure_ascii=False))
