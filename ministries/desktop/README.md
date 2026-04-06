# 🖥️ Министерство Десктопных Приложений

> *"Код, который работает на твоей машине"*

## 🎯 Миссия

Разработка высокопроизводительных десктопных приложений с интеграцией AI для повышения продуктивности пользователей.

## 📁 Структура отдела

```
ministries/desktop/
├── 📁 projects/           # Проекты министерства
│   ├── ai-assistant/      # AI-Помощник
│   ├── codeforge/         # IDE с AI
│   └── securevault/       # Криптографический менеджер
├── 📁 templates/          # Шаблоны десктопных приложений
│   ├── electron-react/    # Electron + React
│   ├── tauri-rust/        # Tauri + Rust
│   └── flutter-desktop/   # Flutter для десктопа
├── 📁 shared/             # Общие компоненты
│   ├── ui-kit/            # UI компоненты
│   └── ai-core/           # Ядро AI-функций
├── 📁 docs/               # Документация
└── Makefile              # Команды управления
```

## 🚀 Проекты

### AI-Помощник (`ai-assistant`)

Локальный AI-ассистент для ПК с приватностью данных.

**Технологии:**
- Python 3.11+
- PyQt6 / Tauri
- llama.cpp (локальные модели)
- SQLite (локальная БД)

**Функции:**
- 🤖 Локальные LLM (без облака)
- 🔍 Умный поиск по файлам
- 📝 Автоматизация задач
- 🔒 100% приватность данных

[Подробнее →](./projects/ai-assistant/README.md)

---

### CodeForge (`codeforge`)

IDE нового поколения с встроенным AI-копилотом.

**Технологии:**
- TypeScript
- Electron
- Monaco Editor
- Tree-sitter

**Функции:**
- ✨ AI-автодополнение
- 🔍 Интеллектуальный рефакторинг
- 🐛 Автоисправление багов
- 📚 Встроенная документация

[Подробнее →](./projects/codeforge/README.md)

---

### SecureVault (`securevault`)

Криптографический менеджер паролей и секретов.

**Технологии:**
- Rust
- Tauri
- Argon2id
- AES-256-GCM

**Функции:**
- 🔐 Zero-knowledge архитектура
- 🔑 Управление паролями
- 📝 Зашифрованные заметки
- 🗂️ Защищённое хранилище файлов

[Подробнее →](./projects/securevault/README.md)

---

## 🛠️ Быстрый старт

```bash
# Перейти в министерство
cd ministries/desktop

# Выбрать шаблон для нового проекта
make template NAME=my-app TEMPLATE=electron-react

# Или клонировать существующий проект
make clone PROJECT=ai-assistant

# Запуск разработки
cd projects/ai-assistant
make dev
```

## 📋 Стандарты разработки

### Структура проекта
```
project-name/
├── src/                   # Исходный код
│   ├── main/             # Точка входа
│   ├── core/             # Ядро приложения
│   ├── modules/          # Модули
│   └── utils/            # Утилиты
├── tests/                # Тесты
├── docs/                 # Документация
├── assets/               # Ресурсы
├── package.json          # Зависимости
└── README.md            # Описание
```

### Качество кода
- ✅ TypeScript / Rust / Python строгие типы
- ✅ Unit-тесты (min 80% покрытие)
- ✅ E2E тесты для UI
- ✅ ESLint / Clippy / Ruff
- ✅ Prettier / rustfmt / black

## 👥 Команда

| Роль | Ответственный | Контакт |
|------|---------------|---------|
| Министр | AI-Agent-01 | minister@desktop.ai-gov.ru |
| Tech Lead | AI-Agent-02 | techlead@desktop.ai-gov.ru |
| QA Lead | AI-Agent-03 | qa@desktop.ai-gov.ru |

---

**🏛️ Возврат в [Кабинет Министров](../../README.md)**
