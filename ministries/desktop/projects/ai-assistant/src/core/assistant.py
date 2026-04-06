"""
Ядро AI-ассистента
"""

import yaml
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Message:
    """Сообщение в диалоге"""
    role: str  # "user" или "assistant"
    content: str
    timestamp: Optional[str] = None


class AIAssistant:
    """
    Главный класс AI-ассистента.
    
    Управляет:
    - Загрузкой и использованием LLM
    - Контекстом разговора
    - Плагинами и инструментами
    """
    
    def __init__(self, config_path: str = "config/local.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
        self.model = None
        self.memory: List[Message] = []
        self.plugins = {}
        
        self.logger.info("AI-Ассистент инициализирован")
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации"""
        if not self.config_path.exists():
            return self._default_config()
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict[str, Any]:
        """Конфигурация по умолчанию"""
        return {
            "llm": {
                "model_path": "./models/default.gguf",
                "context_length": 4096,
                "temperature": 0.7,
                "max_tokens": 512
            },
            "memory": {
                "max_history": 50,
                "persist": True
            },
            "plugins": {
                "enabled": ["file_search", "calculator"]
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Настройка логирования"""
        logger = logging.getLogger("AIAssistant")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_model(self) -> bool:
        """
        Загрузка локальной LLM модели.
        
        Returns:
            True если модель загружена успешно
        """
        try:
            # Здесь будет интеграция с llama.cpp или аналогом
            model_path = self.config["llm"]["model_path"]
            self.logger.info(f"Загрузка модели: {model_path}")
            
            # TODO: Реальная загрузка модели
            # from llama_cpp import Llama
            # self.model = Llama(model_path=model_path, ...)
            
            self.model = MockModel(self.config["llm"])
            self.logger.info("Модель загружена успешно")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модели: {e}")
            return False
    
    def process(self, user_input: str) -> str:
        """
        Обработка пользовательского запроса.
        
        Args:
            user_input: Текст запроса
            
        Returns:
            Ответ от AI
        """
        if not self.model:
            return "❌ Модель не загружена. Выполните load_model()"
        
        # Сохраняем в память
        self.memory.append(Message(role="user", content=user_input))
        
        # Проверяем команды
        if user_input.startswith("/"):
            return self._handle_command(user_input)
        
        # Генерируем ответ
        response = self._generate_response(user_input)
        
        # Сохраняем ответ
        self.memory.append(Message(role="assistant", content=response))
        
        # Обрезаем историю если нужно
        self._trim_memory()
        
        return response
    
    def _generate_response(self, user_input: str) -> str:
        """Генерация ответа через LLM"""
        # Строим промпт с историей
        prompt = self._build_prompt(user_input)
        
        # Генерируем через модель
        response = self.model.generate(prompt)
        
        return response
    
    def _build_prompt(self, user_input: str) -> str:
        """Построение промпта с контекстом"""
        system_prompt = """Ты AI-Помощник, дружелюбный искусственный интеллект. 
Ты помогаешь пользователю с различными задачами, отвечаешь на вопросы и поддерживаешь разговор.
Отвечай на русском языке, будь краток и по делу."""
        
        # Добавляем историю
        history = ""
        for msg in self.memory[-10:]:  # Последние 10 сообщений
            prefix = "Пользователь:" if msg.role == "user" else "Ассистент:"
            history += f"{prefix} {msg.content}\n"
        
        prompt = f"{system_prompt}\n\n{history}Пользователь: {user_input}\nАссистент:"
        return prompt
    
    def _handle_command(self, command: str) -> str:
        """Обработка слэш-команд"""
        parts = command.split()
        cmd = parts[0].lower()
        
        commands = {
            "/help": self._cmd_help,
            "/clear": self._cmd_clear,
            "/history": self._cmd_history,
            "/status": self._cmd_status,
        }
        
        handler = commands.get(cmd, lambda _: "❌ Неизвестная команда. Используйте /help")
        return handler(parts[1:])
    
    def _cmd_help(self, args) -> str:
        return """📋 Доступные команды:
/help - Показать справку
/clear - Очистить историю
/history - Показать историю
/status - Статус системы"""
    
    def _cmd_clear(self, args) -> str:
        self.memory.clear()
        return "🗑️ История очищена"
    
    def _cmd_history(self, args) -> str:
        if not self.memory:
            return "История пуста"
        return "\n".join([f"{m.role}: {m.content[:50]}..." for m in self.memory[-10:]])
    
    def _cmd_status(self, args) -> str:
        return f"""📊 Статус системы:
Модель: {'✅ Загружена' if self.model else '❌ Не загружена'}
История: {len(self.memory)} сообщений
Плагины: {len(self.plugins)} активных"""
    
    def _trim_memory(self):
        """Обрезка истории до максимума"""
        max_history = self.config["memory"]["max_history"]
        if len(self.memory) > max_history:
            self.memory = self.memory[-max_history:]


class MockModel:
    """Заглушка модели для тестирования"""
    
    def __init__(self, config):
        self.config = config
    
    def generate(self, prompt: str) -> str:
        """Мок-генерация ответа"""
        responses = [
            "Я понимаю ваш запрос. Вот что я могу сказать...",
            "Интересный вопрос! Давайте разберём...",
            "На основе доступной информации...",
            "Я могу помочь с этим. Вот мой ответ...",
        ]
        import random
        return random.choice(responses)
