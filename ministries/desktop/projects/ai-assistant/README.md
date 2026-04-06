# AI-Помощник

Локальный AI-ассистент для ПК с приватностью данных.

## 🚀 Быстрый старт

```bash
# Установка
make install

# Разработка
make dev

# Сборка
make build
```

## 🏗️ Архитектура

```
ai-assistant/
├── src/                   # Исходный код
│   ├── main.py           # Точка входа
│   ├── core/             # Ядро
│   │   ├── assistant.py  # Логика ассистента
│   │   ├── memory.py     # Память контекста
│   │   └── plugins.py    # Система плагинов
│   ├── ui/               # Интерфейс
│   │   ├── main_window.py
│   │   └── chat_widget.py
│   ├── llm/              # LLM интеграция
│   │   ├── local_model.py
│   │   └── prompts.py
│   └── utils/            # Утилиты
├── tests/                # Тесты
├── models/               # Локальные модели
├── config/               # Конфигурация
└── docs/                 # Документация
```

## ⚙️ Конфигурация

Создайте `config/local.yaml`:

```yaml
llm:
  model_path: "./models/llama-2-7b.gguf"
  context_length: 4096
  temperature: 0.7

ui:
  theme: "dark"
  language: "ru"

memory:
  max_history: 50
  persist: true
```

## 📝 Лицензия

MIT © AI Правительство
