"""
🔌 WebSocket Module
Логи и обновления в реальном времени
"""

from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from datetime import datetime

# Инициализация SocketIO
socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')


def init_socketio(app: Flask):
    """Инициализирует SocketIO с приложением Flask"""
    socketio.init_app(app)
    return socketio


# ========== Events ==========

@socketio.on('connect')
def handle_connect():
    """Клиент подключился"""
    emit('connected', {
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Подключено к AI Правительство WebSocket'
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Клиент отключился"""
    print(f'Client disconnected')


@socketio.on('join_project')
def handle_join_project(data):
    """Клиент присоединяется к комнате проекта"""
    project_id = data.get('project_id')
    if project_id:
        join_room(f'project_{project_id}')
        emit('joined', {
            'project_id': project_id,
            'message': f'Присоединился к проекту {project_id}'
        })


@socketio.on('leave_project')
def handle_leave_project(data):
    """Клиент покидает комнату проекта"""
    project_id = data.get('project_id')
    if project_id:
        leave_room(f'project_{project_id}')
        emit('left', {'project_id': project_id})


@socketio.on('join_task')
def handle_join_task(data):
    """Клиент присоединяется к комнате задачи"""
    task_id = data.get('task_id')
    if task_id:
        join_room(f'task_{task_id}')
        emit('joined', {
            'task_id': task_id,
            'message': f'Присоединился к задаче {task_id}'
        })


# ========== Broadcast Functions ==========

def broadcast_task_update(task_id: str, project_id: str, data: dict):
    """
    Отправляет обновление задачи всем подписанным клиентам
    
    Args:
        task_id: ID задачи
        project_id: ID проекта
        data: Данные для отправки {status, progress, message, etc.}
    """
    payload = {
        'type': 'task_update',
        'task_id': task_id,
        'project_id': project_id,
        'timestamp': datetime.now().isoformat(),
        **data
    }
    
    # Отправляем в комнату задачи
    socketio.emit('task_update', payload, room=f'task_{task_id}')
    
    # Отправляем в комнату проекта
    socketio.emit('task_update', payload, room=f'project_{project_id}')


def broadcast_task_log(task_id: str, message: str, level: str = 'info'):
    """
    Отправляет лог выполнения задачи
    
    Args:
        task_id: ID задачи
        message: Сообщение лога
        level: Уровень (info, success, warning, error)
    """
    payload = {
        'type': 'task_log',
        'task_id': task_id,
        'timestamp': datetime.now().isoformat(),
        'message': message,
        'level': level
    }
    
    socketio.emit('task_log', payload, room=f'task_{task_id}')


def broadcast_project_update(project_id: str, data: dict):
    """
    Отправляет обновление проекта
    """
    payload = {
        'type': 'project_update',
        'project_id': project_id,
        'timestamp': datetime.now().isoformat(),
        **data
    }
    
    socketio.emit('project_update', payload, room=f'project_{project_id}')


def broadcast_progress(project_id: str, current: int, total: int, message: str = None):
    """
    Отправляет прогресс выполнения
    
    Args:
        project_id: ID проекта
        current: Текущее количество выполненных задач
        total: Общее количество задач
        message: Сообщение о прогрессе
    """
    progress = (current / total * 100) if total > 0 else 0
    
    payload = {
        'type': 'progress',
        'project_id': project_id,
        'timestamp': datetime.now().isoformat(),
        'progress': round(progress, 1),
        'current': current,
        'total': total,
        'message': message or f'{current} из {total} задач ({round(progress)}%)'
    }
    
    socketio.emit('progress', payload, room=f'project_{project_id}')


def broadcast_agent_status(agent_id: str, status: str, message: str = None):
    """
    Отправляет статус агента
    """
    payload = {
        'type': 'agent_status',
        'agent_id': agent_id,
        'timestamp': datetime.now().isoformat(),
        'status': status,
        'message': message
    }
    
    socketio.emit('agent_status', payload, broadcast=True)


# ========== Real-time Analytics ==========

def broadcast_analytics_update(data: dict):
    """
    Отправляет обновление аналитики в реальном времени
    
    Args:
        data: Данные аналитики {event_type, agent_type, timestamp, ...}
    """
    payload = {
        'type': 'analytics_update',
        'timestamp': datetime.now().isoformat(),
        **data
    }
    
    socketio.emit('analytics_update', payload, room='analytics')
    socketio.emit('analytics_update', payload, broadcast=True)


def broadcast_alert(alert: dict):
    """
    Отправляет алерт всем подключенным клиентам
    
    Args:
        alert: {level, title, message, metric, threshold, current_value}
    """
    payload = {
        'type': 'alert',
        'timestamp': datetime.now().isoformat(),
        **alert
    }
    
    socketio.emit('alert', payload, broadcast=True)


@socketio.on('join_analytics')
def handle_join_analytics():
    """Клиент присоединяется к аналитике"""
    join_room('analytics')
    emit('joined', {'room': 'analytics', 'message': 'Подключено к аналитике real-time'})


# ========== Integration with TaskExecutor ==========

class WebSocketLogger:
    """
    Логгер для TaskExecutor, отправляющий сообщения через WebSocket
    """
    
    def __init__(self, task_id: str, project_id: str):
        self.task_id = task_id
        self.project_id = project_id
    
    def info(self, message: str):
        """Информационное сообщение"""
        broadcast_task_log(self.task_id, message, 'info')
        print(f"[{self.task_id}] INFO: {message}")
    
    def success(self, message: str):
        """Успешное выполнение"""
        broadcast_task_log(self.task_id, message, 'success')
        broadcast_task_update(self.task_id, self.project_id, {
            'status': 'in_progress',
            'message': message
        })
        print(f"[{self.task_id}] SUCCESS: {message}")
    
    def warning(self, message: str):
        """Предупреждение"""
        broadcast_task_log(self.task_id, message, 'warning')
        print(f"[{self.task_id}] WARNING: {message}")
    
    def error(self, message: str):
        """Ошибка"""
        broadcast_task_log(self.task_id, message, 'error')
        broadcast_task_update(self.task_id, self.project_id, {
            'status': 'error',
            'message': message
        })
        print(f"[{self.task_id}] ERROR: {message}")
    
    def complete(self, artifacts_count: int):
        """Задача выполнена"""
        message = f"✅ Задача выполнена! Создано {artifacts_count} файлов."
        broadcast_task_log(self.task_id, message, 'success')
        broadcast_task_update(self.task_id, self.project_id, {
            'status': 'done',
            'message': message,
            'artifacts_count': artifacts_count
        })
        print(f"[{self.task_id}] COMPLETE: {message}")


def create_websocket_logger(task_id: str, project_id: str) -> WebSocketLogger:
    """Создаёт WebSocket логгер для задачи"""
    return WebSocketLogger(task_id, project_id)


if __name__ == "__main__":
    # Тест
    from flask import Flask
    
    app = Flask(__name__)
    init_socketio(app)
    
    @app.route('/')
    def index():
        return "WebSocket Server Running"
    
    print("🚀 Запуск WebSocket сервера...")
    print("   URL: http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
