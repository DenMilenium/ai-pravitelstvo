#!/usr/bin/env python3
"""
🎯 Agent Dispatcher (Диспетчер Агентов)
Главный контроллер всех AI-агентов программистов

Запуск:
    python agent_dispatcher.py "Создай дашборд для AI" --agent frontend
    python agent_dispatcher.py "Настройки для приложения" --agent pyqt
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class AgentType(Enum):
    """Типы агентов"""
    PYQT = "pyqt"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DEVOPS = "devops"
    DOCS = "docs"
    ALL = "all"


@dataclass
class AgentInfo:
    """Информация об агенте"""
    name: str
    role: str
    file: str
    description: str
    keywords: List[str]


class AgentDispatcher:
    """
    🎯 Диспетчер Агентов
    
    Распределяет задачи между специализированными агентами.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.agents: Dict[AgentType, AgentInfo] = {
            AgentType.PYQT: AgentInfo(
                name="🖥️ PyQt-Agent",
                role="Разработчик GUI",
                file="pyqt_agent.py",
                description="Создаёт десктопные приложения на Python/PyQt6",
                keywords=["окно", "gui", "приложение", "виджет", "pyqt", "desktop", "chat", "настройки"]
            ),
            AgentType.FRONTEND: AgentInfo(
                name="🌐 Frontend-Agent",
                role="Frontend разработчик",
                file="frontend_agent.py",
                description="Создаёт веб-интерфейсы на React",
                keywords=["сайт", "веб", "dashboard", "лендинг", "форма", "react", "frontend", "page"]
            ),
            AgentType.BACKEND: AgentInfo(
                name="⚙️ Backend-Agent",
                role="Backend разработчик",
                file="backend_agent.py",
                description="Создаёт API и серверную часть",
                keywords=["api", "сервер", "backend", "auth", "websocket", "база данных", "go", "python"]
            ),
            AgentType.DEVOPS: AgentInfo(
                name="🔧 DevOps-Agent",
                role="DevOps инженер",
                file="devops_agent.py",
                description="Настраивает CI/CD, Docker, Kubernetes",
                keywords=["docker", "ci/cd", "kubernetes", "deploy", "контейнер", "github actions"]
            ),
            AgentType.DOCS: AgentInfo(
                name="📝 Docs-Agent",
                role="Технический писатель",
                file="docs_agent.py",
                description="Создаёт документацию",
                keywords=["документация", "readme", "docs", "wiki", "инструкция"]
            ),
        }
    
    def detect_agent(self, request: str) -> AgentType:
        """
        Автоматическое определение подходящего агента
        
        Args:
            request: Описание задачи
            
        Returns:
            Тип агента
        """
        request_lower = request.lower()
        scores: Dict[AgentType, int] = {agent: 0 for agent in AgentType if agent != AgentType.ALL}
        
        for agent_type, info in self.agents.items():
            for keyword in info.keywords:
                if keyword.lower() in request_lower:
                    scores[agent_type] += 1
        
        # Выбираем агента с максимальным счётом
        best_agent = max(scores, key=scores.get)
        
        # Если ничего не найдено - по умолчанию frontend
        if scores[best_agent] == 0:
            return AgentType.FRONTEND
        
        return best_agent
    
    def route_request(self, request: str, agent_type: Optional[AgentType] = None) -> str:
        """
        Маршрутизация запроса к агенту
        
        Args:
            request: Описание задачи
            agent_type: Конкретный агент (или автоопределение)
            
        Returns:
            Результат работы агента
        """
        # Определяем агента
        if agent_type is None or agent_type == AgentType.ALL:
            detected = self.detect_agent(request)
        else:
            detected = agent_type
        
        info = self.agents[detected]
        
        print(f"🎯 Диспетчер: запрос направлен к {info.name}")
        print(f"   Задача: {request}")
        print(f"   Роль: {info.role}")
        print()
        
        # Здесь был бы вызов реального агента
        # Пока возвращаем инструкцию
        return self._generate_instruction(detected, request)
    
    def _generate_instruction(self, agent_type: AgentType, request: str) -> str:
        """Генерация инструкции для агента"""
        info = self.agents[agent_type]
        
        instruction = f"""
╔══════════════════════════════════════════════════════════╗
║  {info.name} - ЗАДАЧА                                    ║
╚══════════════════════════════════════════════════════════╝

📋 ЗАПРОС: {request}

🎯 РОЛЬ: {info.role}

📁 ФАЙЛ: agents/{info.file}

📝 ОПИСАНИЕ:
{info.description}

⚡ ДЕЙСТВИЕ:
Запустить агента и передать запрос:

    python agents/{info.file} "{request}"

💡 ПРИМЕР:
"""
        
        if agent_type == AgentType.PYQT:
            instruction += '''    python agents/pyqt_agent.py "Создай окно настроек" -o settings.py
    python agents/pyqt_agent.py "Чат с тёмной темой"'''
        elif agent_type == AgentType.FRONTEND:
            instruction += '''    python agents/frontend_agent.py "Дашборд для AI" -o dashboard
    python agents/frontend_agent.py "Лендинг продукта"'''
        elif agent_type == AgentType.BACKEND:
            instruction += '''    python agents/backend_agent.py "API для чата" -o chat-api
    python agents/backend_agent.py "JWT авторизация" -l python'''
        
        return instruction
    
    def list_agents(self) -> str:
        """Список всех агентов"""
        output = "\n🤖 ДОСТУПНЫЕ АГЕНТЫ:\n"
        output += "=" * 60 + "\n\n"
        
        for agent_type, info in self.agents.items():
            output += f"{info.name}\n"
            output += f"   Роль: {info.role}\n"
            output += f"   Файл: {info.file}\n"
            output += f"   Ключевые слова: {', '.join(info.keywords[:5])}...\n"
            output += "\n"
        
        return output
    
    def show_status(self) -> str:
        """Статус системы агентов"""
        output = f"""
╔══════════════════════════════════════════════════════════╗
║        🤖 AI ПРАВИТЕЛЬСТВО - СТАТУС АГЕНТОВ              ║
╚══════════════════════════════════════════════════════════╝

Версия диспетчера: {self.VERSION}

┌─────────────────────────────────────────────────────────┐
│ Активные агенты: {len(self.agents)}                                        │
└─────────────────────────────────────────────────────────┘

🖥️  Desktop:     PyQt-Agent          [ГОТОВ]
🌐 Web:          Frontend-Agent      [ГОТОВ]
⚙️  Backend:      Backend-Agent       [ГОТОТВ]
🔧 DevOps:       DevOps-Agent        [В РАЗРАБОТКЕ]
📝 Docs:         Docs-Agent          [В РАЗРАБОТКЕ]

📊 СТАТИСТИКА:
   • Всего агентов: {len(self.agents)}
   • Готовы к работе: 3
   • В разработке: 2
   • Выполнено задач: 0

🎯 РЕЖИМ РАБОТЫ:
   Автоматическое определение агента по ключевым словам

💡 ИСПОЛЬЗОВАНИЕ:
   python agent_dispatcher.py "Создай дашборд"
   python agent_dispatcher.py "Окно настроек" --agent pyqt
"""
        return output


def main():
    parser = argparse.ArgumentParser(
        description="🎯 Agent Dispatcher - Диспетчер AI-агентов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Автоопределение агента
  python agent_dispatcher.py "Создай дашборд"
  
  # Конкретный агент
  python agent_dispatcher.py "Чат" --agent pyqt
  
  # Список агентов
  python agent_dispatcher.py --list
  
  # Статус системы
  python agent_dispatcher.py --status
        """
    )
    
    parser.add_argument("request", nargs="?", help="Описание задачи")
    parser.add_argument(
        "--agent", "-a",
        choices=["pyqt", "frontend", "backend", "devops", "docs"],
        help="Выбрать конкретного агента"
    )
    parser.add_argument("--list", "-l", action="store_true", help="Список агентов")
    parser.add_argument("--status", "-s", action="store_true", help="Статус системы")
    
    args = parser.parse_args()
    
    dispatcher = AgentDispatcher()
    
    if args.list:
        print(dispatcher.list_agents())
    elif args.status:
        print(dispatcher.show_status())
    elif args.request:
        agent_type = AgentType(args.agent) if args.agent else None
        result = dispatcher.route_request(args.request, agent_type)
        print(result)
    else:
        print(dispatcher.show_status())


if __name__ == "__main__":
    main()
