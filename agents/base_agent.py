"""
🤖 Base Agent
Базовый класс для всех агентов AI Правительства
Все агенты должны наследоваться от этого класса
"""

import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class AgentStatus(Enum):
    """Статусы агента"""
    IDLE = "idle"           # Простаивает
    BUSY = "busy"           # Выполняет задачу
    ERROR = "error"         # Ошибка
    OFFLINE = "offline"     # Не доступен


@dataclass
class AgentTask:
    """Задача для агента"""
    id: str
    title: str
    description: str
    project_id: str
    status: str = "pending"
    priority: int = 3
    created_at: str = None
    completed_at: str = None
    artifacts: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.artifacts is None:
            self.artifacts = {}


@dataclass  
class AgentMessage:
    """Сообщение от/для агента"""
    id: str
    from_agent: str
    to_agent: str
    message_type: str  # 'task', 'result', 'status', 'chat'
    payload: Dict[str, Any]
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class BaseAgent(ABC):
    """
    🤖 Базовый класс для всех агентов AI Правительства
    
    Все агенты должны:
    1. Наследоваться от BaseAgent
    2. Определять NAME, ROLE, EXPERTISE
    3. Реализовывать метод process_task()
    4. Подчиняться TeamLead-Agent через message bus
    """
    
    # Обязательные поля для каждого агента
    NAME: str = "Base Agent"
    ROLE: str = "Base Role"
    EXPERTISE: List[str] = []
    EMOJI: str = "🤖"
    
    def __init__(self, agent_id: str = None, message_bus=None):
        self.agent_id = agent_id or f"{self.__class__.__name__.lower()}_{uuid.uuid4().hex[:8]}"
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self.message_bus = message_bus
        self.task_history: List[AgentTask] = []
        self.created_at = datetime.now().isoformat()
    
    def get_info(self) -> Dict[str, Any]:
        """Возвращает информацию об агенте"""
        return {
            'agent_id': self.agent_id,
            'name': self.NAME,
            'role': self.ROLE,
            'emoji': self.EMOJI,
            'expertise': self.EXPERTISE,
            'status': self.status.value,
            'current_task': self.current_task.id if self.current_task else None,
            'tasks_completed': len(self.task_history),
            'created_at': self.created_at
        }
    
    @abstractmethod
    def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Главный метод выполнения задачи.
        Каждый агент должен реализовать этот метод!
        
        Args:
            task: Задача для выполнения
            
        Returns:
            Dict с результатами:
            {
                'success': bool,
                'message': str,
                'artifacts': Dict[str, str],  # filename -> content
                'files_created': List[str]
            }
        """
        pass
    
    def receive_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Получает задачу от TeamLead-Agent.
        Не переопределять! Использует process_task()
        """
        # Уведомляем TeamLead что начали
        self._notify_teamlead('task_started', {
            'task_id': task.id,
            'agent_id': self.agent_id
        })
        
        # Меняем статус
        self.status = AgentStatus.BUSY
        self.current_task = task
        
        try:
            # Выполняем задачу
            result = self.process_task(task)
            
            # Обновляем статус
            task.status = "completed" if result.get('success') else "failed"
            task.completed_at = datetime.now().isoformat()
            task.artifacts = result.get('artifacts', {})
            
            # Добавляем в историю
            self.task_history.append(task)
            
            # Уведомляем TeamLead
            self._notify_teamlead('task_completed', {
                'task_id': task.id,
                'agent_id': self.agent_id,
                'success': result.get('success'),
                'artifacts_count': len(result.get('artifacts', {}))
            })
            
            return result
            
        except Exception as e:
            # Обрабатываем ошибку
            task.status = "failed"
            self.status = AgentStatus.ERROR
            
            self._notify_teamlead('task_failed', {
                'task_id': task.id,
                'agent_id': self.agent_id,
                'error': str(e)
            })
            
            return {
                'success': False,
                'message': f'Ошибка: {str(e)}',
                'artifacts': {}
            }
        finally:
            # Возвращаем в idle
            self.status = AgentStatus.IDLE
            self.current_task = None
    
    def _notify_teamlead(self, message_type: str, payload: Dict):
        """Отправляет сообщение TeamLead-Agent"""
        if self.message_bus:
            message = AgentMessage(
                id=uuid.uuid4().hex[:8],
                from_agent=self.agent_id,
                to_agent="teamlead",
                message_type=message_type,
                payload=payload
            )
            self.message_bus.send_message(message)
    
    def send_message(self, to_agent: str, message_type: str, payload: Dict) -> bool:
        """Отправляет сообщение другому агенту"""
        if not self.message_bus:
            return False
        
        message = AgentMessage(
            id=uuid.uuid4().hex[:8],
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload
        )
        return self.message_bus.send_message(message)
    
    def receive_message(self, message: AgentMessage) -> Optional[Dict]:
        """Обрабатывает входящее сообщение"""
        if message.message_type == 'task':
            task_data = message.payload.get('task')
            if task_data:
                task = AgentTask(**task_data)
                return self.receive_task(task)
        
        elif message.message_type == 'status_request':
            return {'status': self.status.value, 'info': self.get_info()}
        
        elif message.message_type == 'chat':
            return self.chat_response(message.payload.get('text', ''))
        
        return None
    
    def chat_response(self, message: str) -> Dict[str, Any]:
        """
        Отвечает на сообщение в чате.
        Можно переопределить для более умных ответов!
        """
        responses = {
            'привет': f'{self.EMOJI} Привет! Я {self.NAME}. {self.ROLE}.',
            'кто ты': f'{self.EMOJI} Я {self.NAME}. Моя специализация: {", ".join(self.EXPERTISE)}.',
            'что ты умеешь': f'{self.EMOJI} Я умею: {", ".join(self.EXPERTISE)}.',
            'статус': f'{self.EMOJI} Статус: {self.status.value}. Выполнено задач: {len(self.task_history)}.',
        }
        
        message_lower = message.lower()
        for key, response in responses.items():
            if key in message_lower:
                return {'type': 'chat', 'message': response}
        
        return {
            'type': 'chat', 
            'message': f'{self.EMOJI} Я понял: "{message}". Используй "Выполнить задачу" для работы.'
        }
    
    def can_handle(self, task_type: str) -> bool:
        """Проверяет, может ли агент выполнить задачу этого типа"""
        task_type_lower = task_type.lower()
        return any(expertise.lower() in task_type_lower 
                  for expertise in self.EXPERTISE)


class MessageBus:
    """
    🚌 Шина сообщений для связи агентов с TeamLead
    """
    
    def __init__(self):
        self.messages: List[AgentMessage] = []
        self.agents: Dict[str, BaseAgent] = {}
        self.teamlead = None
    
    def register_agent(self, agent: BaseAgent):
        """Регистрирует агента в шине"""
        self.agents[agent.agent_id] = agent
        agent.message_bus = self
    
    def register_teamlead(self, teamlead):
        """Регистрирует TeamLead"""
        self.teamlead = teamlead
    
    def send_message(self, message: AgentMessage) -> bool:
        """Отправляет сообщение"""
        self.messages.append(message)
        
        # Доставляем получателю
        if message.to_agent == "teamlead" and self.teamlead:
            self.teamlead.receive_message(message)
        elif message.to_agent in self.agents:
            self.agents[message.to_agent].receive_message(message)
        
        return True
    
    def get_messages_for(self, agent_id: str) -> List[AgentMessage]:
        """Получает сообщения для агента"""
        return [m for m in self.messages if m.to_agent == agent_id]


# ========== Конкретные реализации агентов ==========

class FrontendAgent(BaseAgent):
    """🎨 Frontend разработчик"""
    NAME = "Frontend Agent"
    ROLE = "Frontend Developer"
    EMOJI = "🎨"
    EXPERTISE = ["HTML", "CSS", "JavaScript", "React", "Vue", "UI/UX"]
    
    def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Генерирует frontend код"""
        # Здесь будет реальная генерация кода
        return {
            'success': True,
            'message': '✅ Frontend код сгенерирован',
            'artifacts': {
                'index.html': '<!DOCTYPE html><html>...</html>',
                'style.css': 'body { ... }'
            },
            'files_created': ['index.html', 'style.css']
        }


class BackendAgent(BaseAgent):
    """⚙️ Backend разработчик"""
    NAME = "Backend Agent"
    ROLE = "Backend Developer"
    EMOJI = "⚙️"
    EXPERTISE = ["Python", "Node.js", "API", "Database", "FastAPI", "Django"]
    
    def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Генерирует backend код"""
        return {
            'success': True,
            'message': '✅ Backend код сгенерирован',
            'artifacts': {
                'api.py': '# API код...',
                'models.py': '# Модели...'
            },
            'files_created': ['api.py', 'models.py']
        }


class DevOpsAgent(BaseAgent):
    """🚀 DevOps инженер"""
    NAME = "DevOps Agent"
    ROLE = "DevOps Engineer"
    EMOJI = "🚀"
    EXPERTISE = ["Docker", "CI/CD", "Nginx", "Kubernetes", "AWS", "Azure"]
    
    def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Генерирует DevOps конфигурацию"""
        return {
            'success': True,
            'message': '✅ DevOps конфигурация создана',
            'artifacts': {
                'Dockerfile': 'FROM python:3.9...',
                'docker-compose.yml': 'version: "3.8"...'
            },
            'files_created': ['Dockerfile', 'docker-compose.yml']
        }


if __name__ == "__main__":
    # Тест
    print("🤖 Тест Base Agent")
    
    # Создаём шину
    bus = MessageBus()
    
    # Создаём агентов
    frontend = FrontendAgent()
    backend = BackendAgent()
    
    # Регистрируем
    bus.register_agent(frontend)
    bus.register_agent(backend)
    
    # Тест информации
    print(f"\n{frontend.get_info()}")
    print(f"\n{backend.get_info()}")
    
    # Тест задачи
    task = AgentTask(
        id="task_001",
        title="Создать лендинг",
        description="Создать HTML страницу для кофейни",
        project_id="proj_001"
    )
    
    result = frontend.receive_task(task)
    print(f"\nРезультат: {result}")
    
    # Тест чата
    chat = frontend.chat_response("Что ты умеешь?")
    print(f"\nЧат: {chat}")
