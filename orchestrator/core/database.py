"""
🎯 AI Правительство - Система Оркестрации (Orchestrator)
Управление проектами, задачами и агентами
"""

import sqlite3
import json
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict


class TaskStatus(Enum):
    """Статусы задачи"""
    PENDING = "pending"           # Ожидает назначения
    ASSIGNED = "assigned"         # Назначена агенту
    IN_PROGRESS = "in_progress"   # В работе
    REVIEW = "review"             # На проверке
    DONE = "done"                 # Выполнена
    FAILED = "failed"             # Ошибка


class ProjectStatus(Enum):
    """Статусы проекта"""
    CREATED = "created"           # Создан
    PLANNING = "planning"         # Планирование
    IN_PROGRESS = "in_progress"   # В работе
    REVIEW = "review"             # На проверке
    COMPLETED = "completed"       # Завершён
    ARCHIVED = "archived"         # Архивирован


@dataclass
class Task:
    """Задача для агента"""
    id: str
    project_id: str
    title: str
    description: str
    agent_type: str           # Тип агента (frontend, backend, etc)
    status: TaskStatus
    priority: int             # 1-5
    dependencies: List[str]   # ID зависимых задач
    artifacts: Dict           # Сгенерированные файлы
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    assigned_to: Optional[str] = None
    parent_task_id: Optional[str] = None
    
    def to_dict(self):
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data):
        data['status'] = TaskStatus(data['status'])
        return cls(**data)


@dataclass
class Project:
    """Проект для выполнения"""
    id: str
    name: str
    description: str
    tz_text: str              # Полное ТЗ
    status: ProjectStatus
    tasks: List[str]          # ID задач
    created_at: str
    completed_at: Optional[str] = None
    output_zip: Optional[str] = None
    
    def to_dict(self):
        data = asdict(self)
        data['status'] = self.status.value
        return data


class Database:
    """База данных оркестратора"""
    
    def __init__(self, db_path: str = "orchestrator/orchestrator.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица проектов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    tz_text TEXT,
                    status TEXT DEFAULT 'created',
                    tasks TEXT,  -- JSON array of task IDs
                    created_at TEXT,
                    completed_at TEXT,
                    output_zip TEXT
                )
            ''')
            
            # Таблица задач
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    agent_type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 3,
                    dependencies TEXT,  -- JSON array
                    artifacts TEXT,     -- JSON object
                    created_at TEXT,
                    started_at TEXT,
                    completed_at TEXT,
                    assigned_to TEXT,
                    parent_task_id TEXT,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            ''')
            
            # Таблица сообщений (Message Bus)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT,
                    agent_type TEXT,
                    message_type TEXT,  -- assign, complete, review, etc
                    payload TEXT,       -- JSON
                    created_at TEXT,
                    processed BOOLEAN DEFAULT 0
                )
            ''')
            
            # Таблица артефактов (файлы)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artifacts (
                    id TEXT PRIMARY KEY,
                    task_id TEXT,
                    project_id TEXT,
                    file_name TEXT,
                    file_path TEXT,
                    file_type TEXT,
                    content TEXT,
                    created_at TEXT,
                    FOREIGN KEY (task_id) REFERENCES tasks(id),
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            ''')
            
            conn.commit()
    
    # === Проекты ===
    
    def create_project(self, project: Project) -> bool:
        """Создать проект"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO projects (id, name, description, tz_text, status, tasks, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                project.id,
                project.name,
                project.description,
                project.tz_text,
                project.status.value,
                json.dumps(project.tasks),
                project.created_at
            ))
            conn.commit()
            return True
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Получить проект"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            row = cursor.fetchone()
            
            if row:
                return Project(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    tz_text=row[3],
                    status=ProjectStatus(row[4]),
                    tasks=json.loads(row[5]) if row[5] else [],
                    created_at=row[6],
                    completed_at=row[7],
                    output_zip=row[8]
                )
            return None
    
    def update_project_status(self, project_id: str, status: ProjectStatus):
        """Обновить статус проекта"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            completed_at = datetime.now().isoformat() if status == ProjectStatus.COMPLETED else None
            cursor.execute('''
                UPDATE projects SET status = ?, completed_at = ? WHERE id = ?
            ''', (status.value, completed_at, project_id))
            conn.commit()
    
    def get_all_projects(self) -> List[Project]:
        """Все проекты"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
            rows = cursor.fetchall()
            
            projects = []
            for row in rows:
                projects.append(Project(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    tz_text=row[3],
                    status=ProjectStatus(row[4]),
                    tasks=json.loads(row[5]) if row[5] else [],
                    created_at=row[6],
                    completed_at=row[7],
                    output_zip=row[8]
                ))
            return projects
    
    # === Задачи ===
    
    def create_task(self, task: Task) -> bool:
        """Создать задачу"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (id, project_id, title, description, agent_type, 
                                 status, priority, dependencies, artifacts, created_at,
                                 parent_task_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.id,
                task.project_id,
                task.title,
                task.description,
                task.agent_type,
                task.status.value,
                task.priority,
                json.dumps(task.dependencies),
                json.dumps(task.artifacts),
                task.created_at,
                task.parent_task_id
            ))
            conn.commit()
            return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Получить задачу"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            
            if row:
                return Task(
                    id=row[0],
                    project_id=row[1],
                    title=row[2],
                    description=row[3],
                    agent_type=row[4],
                    status=TaskStatus(row[5]),
                    priority=row[6],
                    dependencies=json.loads(row[7]) if row[7] else [],
                    artifacts=json.loads(row[8]) if row[8] else {},
                    created_at=row[9],
                    started_at=row[10],
                    completed_at=row[11],
                    assigned_to=row[12],
                    parent_task_id=row[13]
                )
            return None
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          assigned_to: str = None, artifacts: Dict = None):
        """Обновить статус задачи"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            updates = ['status = ?']
            params = [status.value]
            
            if status == TaskStatus.IN_PROGRESS:
                updates.append('started_at = ?')
                params.append(datetime.now().isoformat())
            
            if status in [TaskStatus.DONE, TaskStatus.FAILED]:
                updates.append('completed_at = ?')
                params.append(datetime.now().isoformat())
            
            if assigned_to:
                updates.append('assigned_to = ?')
                params.append(assigned_to)
            
            if artifacts:
                updates.append('artifacts = ?')
                params.append(json.dumps(artifacts))
            
            params.append(task_id)
            
            cursor.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
    
    def get_tasks_by_project(self, project_id: str) -> List[Task]:
        """Все задачи проекта"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE project_id = ? ORDER BY created_at', (project_id,))
            rows = cursor.fetchall()
            
            tasks = []
            for row in rows:
                tasks.append(Task(
                    id=row[0],
                    project_id=row[1],
                    title=row[2],
                    description=row[3],
                    agent_type=row[4],
                    status=TaskStatus(row[5]),
                    priority=row[6],
                    dependencies=json.loads(row[7]) if row[7] else [],
                    artifacts=json.loads(row[8]) if row[8] else {},
                    created_at=row[9],
                    started_at=row[10],
                    completed_at=row[11],
                    assigned_to=row[12],
                    parent_task_id=row[13]
                ))
            return tasks
    
    def get_pending_tasks(self, agent_type: str = None) -> List[Task]:
        """Задачи в ожидании"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if agent_type:
                cursor.execute('''
                    SELECT * FROM tasks 
                    WHERE status = ? AND agent_type = ?
                    ORDER BY priority DESC, created_at
                ''', (TaskStatus.PENDING.value, agent_type))
            else:
                cursor.execute('''
                    SELECT * FROM tasks 
                    WHERE status = ?
                    ORDER BY priority DESC, created_at
                ''', (TaskStatus.PENDING.value,))
            
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append(Task(
                    id=row[0],
                    project_id=row[1],
                    title=row[2],
                    description=row[3],
                    agent_type=row[4],
                    status=TaskStatus(row[5]),
                    priority=row[6],
                    dependencies=json.loads(row[7]) if row[7] else [],
                    artifacts=json.loads(row[8]) if row[8] else {},
                    created_at=row[9],
                    started_at=row[10],
                    completed_at=row[11],
                    assigned_to=row[12],
                    parent_task_id=row[13]
                ))
            return tasks
    
    # === Сообщения (Message Bus) ===
    
    def send_message(self, task_id: str, agent_type: str, 
                    message_type: str, payload: Dict) -> int:
        """Отправить сообщение в шину"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages (task_id, agent_type, message_type, payload, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (task_id, agent_type, message_type, json.dumps(payload), 
                  datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid
    
    def get_unprocessed_messages(self, agent_type: str = None) -> List[Dict]:
        """Получить необработанные сообщения"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if agent_type:
                cursor.execute('''
                    SELECT * FROM messages 
                    WHERE processed = 0 AND agent_type = ?
                    ORDER BY created_at
                ''', (agent_type,))
            else:
                cursor.execute('''
                    SELECT * FROM messages 
                    WHERE processed = 0
                    ORDER BY created_at
                ''')
            
            rows = cursor.fetchall()
            messages = []
            for row in rows:
                messages.append({
                    'id': row[0],
                    'task_id': row[1],
                    'agent_type': row[2],
                    'message_type': row[3],
                    'payload': json.loads(row[4]),
                    'created_at': row[5],
                    'processed': row[6]
                })
            return messages
    
    def mark_message_processed(self, message_id: int):
        """Отметить сообщение обработанным"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE messages SET processed = 1 WHERE id = ?', (message_id,))
            conn.commit()
    
    # === Артефакты ===
    
    def save_artifact(self, artifact_id: str, task_id: str, project_id: str,
                     file_name: str, file_path: str, file_type: str, content: str):
        """Сохранить артефакт"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO artifacts (id, task_id, project_id, file_name, file_path, file_type, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (artifact_id, task_id, project_id, file_name, file_path, 
                  file_type, content, datetime.now().isoformat()))
            conn.commit()
    
    def get_project_artifacts(self, project_id: str) -> List[Dict]:
        """Все артефакты проекта"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM artifacts WHERE project_id = ?', (project_id,))
            rows = cursor.fetchall()
            
            artifacts = []
            for row in rows:
                artifacts.append({
                    'id': row[0],
                    'task_id': row[1],
                    'project_id': row[2],
                    'file_name': row[3],
                    'file_path': row[4],
                    'file_type': row[5],
                    'content': row[6],
                    'created_at': row[7]
                })
            return artifacts
