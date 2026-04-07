#!/usr/bin/env python3
"""
⚖️ Судебный департамент - Расширенное задание
Детальные ТЗ для каждого агента
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.core.database import Database, Project, Task, TaskStatus, ProjectStatus
import uuid
from datetime import datetime

db = Database()

# Создаем расширенный проект
project_id = str(uuid.uuid4())[:8]
project = Project(
    id=project_id,
    name='⚖️ Судебный департамент Верховного суда РФ',
    description='''Современный официальный сайт Судебного департамента при Верховном суде Российской Федерации.

КОНЦЕПЦИЯ ДИЗАЙНА:
- Цвета: Тёмно-синий (#1a365d), Золотой (#d4af37), Белый (#ffffff), Серый фон (#f5f5f5)
- Шрифты: Georgia (заголовки), system-ui (текст)
- Стиль: Строгий, авторитетный, современный минимализм

СТРУККТУРА САЙТА:
1. Главная страница - Hero с гербом, новости, быстрые ссылки
2. О департаменте - История, руководство, контакты
3. Деятельность - Направления работы, статистика
4. Документы - Нормативные акты, приказы, методические материалы
5. Электронное правосудие - Подача документов, проверка статуса
6. Новости - Лента новостей с фильтрами
7. Контакты - Адреса, телефоны, форма обратной связи

ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ:
- React 18 + Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Адаптивная верстка (mobile-first)
- SEO-оптимизация
- WCAG 2.1 AA доступность
''',
    tz_text='Europe/Moscow',
    status=ProjectStatus.IN_PROGRESS,
    tasks=[],
    created_at=datetime.now().isoformat()
)
db.create_project(project)

print(f'✅ Проект создан: {project_id}')

# Детальные задачи для агентов
detailed_tasks = [
    # FRONTEND - Дизайн система
    {
        'title': '🎨 Design System & UI Kit',
        'agent_type': 'frontend',
        'description': '''Создать полноценную дизайн-систему для сайта Судебного департамента.

COLORS (CSS variables):
--color-primary: #1a365d (тёмно-синий)
--color-secondary: #d4af37 (золотой)
--color-background: #f5f5f5 (серый фон)
--color-surface: #ffffff (белый)
--color-text-primary: #1a202c (тёмный текст)
--color-text-secondary: #4a5568 (серый текст)

COMPONENTS to create:
1. styles/design-tokens.css - Все CSS переменные
2. components/Button.tsx - Кнопки (primary, secondary, outline)
3. components/Card.tsx - Карточки с тенью
4. components/Input.tsx - Поля ввода
5. components/Header.tsx - Шапка с навигацией
6. components/Footer.tsx - Подвал с контактами
7. components/Hero.tsx - Hero секция
8. assets/gerb.svg - SVG герб (упрощённый)

Use Tailwind CSS classes where possible.''',
        'priority': 1
    },
    
    # NEXTJS - Главная страница
    {
        'title': '🏠 Homepage (Next.js App Router)',
        'agent_type': 'nextjs',
        'description': '''Создать главную страницу сайта Судебного департамента.

FILES to create:
1. app/layout.tsx - Корневой layout с метаданными, шрифтами
2. app/page.tsx - Главная страница
3. app/globals.css - Глобальные стили

PAGE SECTIONS:
1. Header - Логотип + герб, навигация (Главная, О департаменте, Деятельность, Документы, Электронное правосудие, Контакты)
2. Hero - Большой заголовок "Судебный департамент при Верховном суде Российской Федерации", подзаголовок, кнопка CTA
3. News Section - Последние 3 новости с датами
4. Quick Links - Быстрые ссылки (Электронное правосудие, Статистика, Документы)
5. Statistics Preview - 4 цифры: количество судов, судей, дел, обращений
6. Footer - Адрес, телефон, email, соцсети

Use design tokens from design-system.''',
        'priority': 1
    },
    
    # REACT - Компоненты
    {
        'title': '📰 News System Components',
        'agent_type': 'react',
        'description': '''Создать систему компонентов для раздела новостей.

FILES:
1. components/news/NewsCard.tsx - Карточка новости (дата, заголовок, анонс, тег)
2. components/news/NewsList.tsx - Список новостей с сеткой
3. components/news/NewsFilter.tsx - Фильтры по дате и категории
4. components/news/Pagination.tsx - Пагинация
5. app/news/page.tsx - Страница всех новостей
6. lib/news-data.ts - Моковые данные новостей (6 штук)

NewsCard должен содержать:
- Дата (формат: 15 марта 2024)
- Заголовок (h3)
- Анонс 2-3 предложения
- Тег категории (цветной бейдж)
- Ссылка "Подробнее"''',
        'priority': 2
    },
    
    # REACT - Документы
    {
        'title': '📄 Documents Section',
        'agent_type': 'react',
        'description': '''Создать раздел документов с таблицей и поиском.

FILES:
1. components/documents/DocumentTable.tsx - Таблица документов
2. components/documents/DocumentRow.tsx - Строка таблицы
3. components/documents/SearchBar.tsx - Поисковая строка
4. components/documents/FilterTags.tsx - Фильтры по типу
5. app/documents/page.tsx - Страница документов
6. lib/documents-data.ts - Моковые данные (8 документов)

DocumentTable columns:
- Название документа (ссылка)
- Тип (PDF, DOC)
- Дата публикации
- Размер файла
- Кнопка скачать

Include search by name and filter by type.''',
        'priority': 2
    },
    
    # ANALYTICS - Статистика
    {
        'title': '📊 Statistics Dashboard',
        'agent_type': 'analytics',
        'description': '''Создать интерактивную страницу статистики.

FILES:
1. app/statistics/page.tsx - Страница статистики
2. components/statistics/StatsCard.tsx - Карточка с цифрой
3. components/statistics/ChartSection.tsx - Секция с графиком
4. lib/chart-utils.ts - Утилиты для графиков
5. lib/stats-data.ts - Данные для графиков

Statistics to show:
1. Total courts: 3200+ (карточка)
2. Judges: 25000+ (карточка)
3. Cases per year: 15M+ (карточка)
4. E-justice users: 5M+ (карточка)

Charts (use Recharts or Chart.js):
- Line chart: Динамика рассмотренных дел за 5 лет
- Bar chart: Категории дел (гражданские, уголовные, арбитраж)
- Pie chart: Распределение по регионам

Create responsive grid layout.''',
        'priority': 2
    },
    
    # REACT - Электронное правосудие
    {
        'title': '💻 E-Justice Portal',
        'agent_type': 'react',
        'description': '''Создать портал электронного правосудия.

FILES:
1. app/e-justice/page.tsx - Главная страница портала
2. components/ejustice/LoginForm.tsx - Форма входа
3. components/ejustice/ServiceCard.tsx - Карточка услуги
4. components/ejustice/CaseTracker.tsx - Отслеживание дела

Sections:
1. Hero с заголовком "Электронное правосудие"
2. Grid of services (6 карточек):
   - Подача искового заявления
   - Проверка статуса дела
   - Получение копий решений
   - Оплата госпошлины
   - Видеоконференцсвязь
   - Электронная подпись
3. Login form (email, password, кнопка входа)
4. Case tracker (номер дела → статус)

Use icons from Lucide React.''',
        'priority': 1
    },
    
    # FASTAPI - Backend API
    {
        'title': '🔥 FastAPI Backend',
        'agent_type': 'fastapi',
        'description': '''Создать полноценный backend API.

FILES:
1. backend/main.py - Главный файл приложения
2. backend/routers/news.py - API новостей
3. backend/routers/documents.py - API документов
4. backend/routers/auth.py - Авторизация
5. backend/models.py - SQLAlchemy модели
6. backend/schemas.py - Pydantic схемы
7. backend/database.py - Подключение к БД
8. backend/requirements.txt - Зависимости

Endpoints to implement:
GET /api/news - Список новостей (с пагинацией)
GET /api/news/{id} - Одна новость
GET /api/documents - Список документов
GET /api/documents/{id} - Скачать документ
POST /api/auth/login - Вход
POST /api/auth/register - Регистрация
GET /api/statistics - Данные статистики

Include CORS middleware, JWT auth, SQLite database.''',
        'priority': 1
    },
    
    # DJANGO - Admin Panel
    {
        'title': '🐍 Django Admin CMS',
        'agent_type': 'django',
        'description': '''Создать CMS на Django для управления контентом.

FILES:
1. cms/manage.py
2. cms/cms/settings.py
3. cms/cms/urls.py
4. cms/content/models.py - Модели: News, Document, Page
5. cms/content/admin.py - Настройка админки
6. cms/content/views.py - API views
7. cms/templates/admin/base_site.html - Кастомная тема
8. cms/requirements.txt

Models:
- News: title, content, date, category, image, is_published
- Document: title, file, type, date, description
- Page: slug, title, content, meta_description

Admin features:
- Rich text editor (CKEditor)
- Image upload
- Filter by date
- Search
- Bulk actions''',
        'priority': 2
    },
    
    # DOCKER - Containerization
    {
        'title': '🐳 Docker Setup',
        'agent_type': 'docker',
        'description': '''Создать полную Docker инфраструктуру.

FILES:
1. docker-compose.yml - Полный стек
2. frontend/Dockerfile - Next.js контейнер
3. backend/Dockerfile - FastAPI контейнер
4. cms/Dockerfile - Django контейнер
5. nginx/nginx.conf - Reverse proxy
6. .env.example - Пример переменных
7. .dockerignore
8. Makefile - Команды управления

Services in docker-compose:
- frontend (Next.js, port 3000)
- backend (FastAPI, port 8000)
- cms (Django, port 8001)
- nginx (port 80/443)
- postgres (database)
- redis (cache)

Nginx config:
- / -> frontend
- /api -> backend
- /admin -> cms
- Static files caching''',
        'priority': 3
    },
    
    # DOCUMENTATION
    {
        'title': '📚 Full Documentation',
        'agent_type': 'documentation',
        'description': '''Создать полную документацию проекта.

FILES:
1. README.md - Общее описание, скриншоты
2. docs/ARCHITECTURE.md - Архитектура системы
3. docs/API.md - Документация API (OpenAPI/Swagger)
4. docs/DEPLOY.md - Инструкция по развёртыванию
5. docs/CONTRIBUTING.md - Как contribute
6. docs/CHANGELOG.md - История изменений
7. LICENSE - Лицензия MIT

README structure:
- Заголовок с бейджами
- Описание проекта
- Скриншоты (placeholder)
- Технологический стек
- Быстрый старт
- Структура проекта
- API endpoints table
- Лицензия''',
        'priority': 3
    }
]

# Создаем задачи
for i, task_data in enumerate(detailed_tasks, 1):
    task_id = str(uuid.uuid4())[:8]
    task = Task(
        id=task_id,
        project_id=project_id,
        title=task_data['title'],
        description=task_data['description'],
        agent_type=task_data['agent_type'],
        status=TaskStatus.PENDING,
        priority=task_data['priority'],
        dependencies=[],
        artifacts={},
        created_at=datetime.now().isoformat()
    )
    db.create_task(task)
    task_title = task_data['title']
    print(f'✅ Задача {i}: {task_title}')

print(f'\n🎯 Всего задач: {len(detailed_tasks)}')
print(f'📋 Project ID: {project_id}')
print(f'\n🚀 Запустить выполнение:')
print(f'python3 -c "from orchestrator.core.task_executor import TaskExecutor; e = TaskExecutor(); e.execute_pending_tasks()"')
