# 🎯 AI Правительство - Orchestrator (Оркестратор)

Система управления проектами, задачами и координации агентов AI Правительства.

## 🏛️ Архитектура

```
orchestrator/
├── core/                    # Ядро системы
│   ├── database.py         # База данных (SQLite)
│   └── project_manager.py  # Управление проектами и деплой
├── agents/                  # Агенты оркестратора
│   └── teamlead_agent.py   # Главный диспетчер
├── api.py                  # REST API для интеграции с Dashboard
└── projects/               # Собранные проекты (ZIP)
```

## 👑 TeamLead-Agent

Главный архитектор и координатор проектов:

- 📋 **Принимает ТЗ** от заказчика (текстовое описание)
- 🔍 **Анализирует** тип проекта (веб, мобильное, AI, десктоп)
- 📊 **Разбивает** на задачи для министерств
- 🎯 **Назначает** агентов по специализациям
- ✅ **Контролирует** выполнение
- 📦 **Собирает** финальный ZIP-архив

## 🔄 Жизненный цикл проекта

```
CREATED → PLANNING → IN_PROGRESS → REVIEW → COMPLETED
   ↓         ↓            ↓            ↓         ↓
  ТЗ     Задачи    Выполнение   Проверка   ZIP ✅
```

## 🚀 Быстрый старт

### Создание проекта

```bash
curl -X POST http://localhost:5000/api/orchestrator/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Сайт для кофейни",
    "tz_text": "Создать современный сайт для кофейни с меню, фотогалереей и формой бронирования"
  }'
```

### Проверка статуса

```bash
curl http://localhost:5000/api/orchestrator/projects/<project_id>/status
```

### Сборка ZIP

```bash
curl -X POST http://localhost:5000/api/orchestrator/projects/<project_id>/build
```

### Скачивание

```bash
curl -O http://localhost:5000/api/orchestrator/projects/<project_id>/download
```

## 📡 API Endpoints

### Проекты
- `POST /api/orchestrator/projects` - Создать проект
- `GET /api/orchestrator/projects` - Список проектов
- `GET /api/orchestrator/projects/<id>` - Информация о проекте
- `GET /api/orchestrator/projects/<id>/status` - Статус проекта
- `POST /api/orchestrator/projects/<id>/build` - Собрать ZIP
- `GET /api/orchestrator/projects/<id>/download` - Скачать ZIP

### Задачи
- `GET /api/orchestrator/tasks?project_id=<id>` - Задачи проекта
- `GET /api/orchestrator/tasks?status=pending` - Ожидающие задачи
- `POST /api/orchestrator/tasks/<id>/assign` - Назначить агенту
- `PUT /api/orchestrator/tasks/<id>/status` - Обновить статус

### Статистика
- `GET /api/orchestrator/stats` - Общая статистика

## 📊 Статусы задач

- `pending` - Ожидает назначения
- `assigned` - Назначена агенту
- `in_progress` - В работе
- `review` - На проверке
- `done` - Выполнена ✅
- `failed` - Ошибка ❌

## 🎯 Типы агентов

- `frontend` - Frontend разработка
- `backend` - Backend разработка
- `design` - UI/UX дизайн
- `mobile` - Мобильная разработка
- `desktop` - Десктоп приложения
- `devops` - DevOps и деплой
- `ai` - AI/ML компоненты
- `cloud` - Облачная инфраструктура
- `security` - Безопасность
- `marketing` - SEO и маркетинг
- `content` - Контент и документация

## 🏗️ Пример работы

### ТЗ: "Сайт для юридической конторы"

TeamLead-Agent создаёт:

1. **Дизайн** (Figma-Agent)
   - Макеты страниц
   - Строгий деловой стиль

2. **Frontend** (Frontend-Agent) 
   - HTML/CSS/JS
   - Адаптивная вёрстка
   - Форма обратной связи

3. **Backend** (Backend-Agent)
   - API для форм
   - База данных клиентов
   - Админ-панель

4. **DevOps** (DevOps-Agent)
   - Docker контейнеры
   - Настройка сервера

5. **Документация** (TechWriter-Agent)
   - README.md
   - Инструкция по развёртыванию

Итог: ZIP-архив со всеми файлами проекта! 🎉

## 🐝 Интеграция с Dashboard

Orchestrator API автоматически подключается к Dashboard при запуске.

Доступен по адресу: `http://localhost:5000/api/orchestrator/`

## 📦 База данных

SQLite: `orchestrator/orchestrator.db`

Таблицы:
- `projects` - Проекты
- `tasks` - Задачи
- `messages` - Шина сообщений
- `artifacts` - Артефакты (файлы)

---

Создано с ❤️ для AI Правительства 🤖🏛️
