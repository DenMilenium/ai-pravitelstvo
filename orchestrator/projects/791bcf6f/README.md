# ⚖️ Судебный департамент при Верховном суде РФ

<div align="center">
  
  ![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
  ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
  ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
  
  <strong>🎨 Клон cdep.ru с современным дизайном | 🚀 Полный стек с бэкендом</strong>
  
  <br />
  <br />
  
  <a href="#-особенности">Особенности</a> •
  <a href="#-api">API</a> •
  <a href="#-запуск">Запуск</a> •
  <a href="#-структура">Структура</a>
  
</div>

---

## ✨ Особенности v3.1 (Full Stack)

### 🎨 Frontend (Next.js 14)
- **Glassmorphism UI** — современные стеклянные эффекты
- **Анимации** — fade, slide, count-up
- **Адаптивность** — mobile-first
- **TypeScript** — полная типизация

### ⚙️ Backend (FastAPI)
- **REST API** — полный CRUD для всех сущностей
- **PostgreSQL** — надёжная база данных
- **Pydantic** — валидация данных
- **SQLAlchemy** — ORM
- **CORS** — поддержка кросс-доменных запросов

### 📰 Контент (cdep.ru)
- ✅ **РЕАЛЬНЫЕ НОВОСТИ** — парсятся с cdep.ru
- ✅ **РЕАЛЬНАЯ НАВИГАЦИЯ** — все 8 разделов
- ✅ **РЕАЛЬНЫЕ КОНТАКТЫ**
- ✅ **"РОССИЙСКАЯ ФЕДЕРАЦИЯ"** — везде

---

## 🔌 API Endpoints

### Новости
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/news` | Список новостей (с пагинацией) |
| `GET` | `/api/news/{id}` | Одна новость (+просмотры) |
| `POST` | `/api/news` | Создать новость |
| `PUT` | `/api/news/{id}` | Обновить новость |
| `DELETE` | `/api/news/{id}` | Удалить новость |

**Параметры:**
```
GET /api/news?limit=10&skip=0&category=events
```

### Документы
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/documents` | Список документов |
| `GET` | `/api/documents/{id}` | Один документ |
| `POST` | `/api/documents` | Создать документ |
| `POST` | `/api/documents/{id}/download` | Скачать документ |

### Обращения граждан
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/appeals` | Список обращений (админ) |
| `GET` | `/api/appeals/{id}` | Одно обращение |
| `POST` | `/api/appeals` | Создать обращение |
| `PUT` | `/api/appeals/{id}/respond` | Ответить на обращение |

**Форма обращения:**
```json
{
  "full_name": "Иванов Иван Иванович",
  "email": "ivan@example.com",
  "phone": "+7 (999) 123-45-67",
  "subject": "Тема обращения",
  "message": "Текст обращения (минимум 20 символов)"
}
```

### Статистика
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/statistics` | Статистика по регионам |
| `GET` | `/api/statistics/summary` | Сводная статистика |
| `POST` | `/api/statistics` | Добавить статистику |

### Системные
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/seed` | Заполнить тестовыми данными |

---

## 🚀 Запуск

### Docker (Рекомендуется)

```bash
# Запуск всего стека
docker-compose up -d

# Сервисы:
# - Frontend: http://localhost:3000
# - API: http://localhost:8000
# - Adminer (БД): http://localhost:8080
#   Server: db
#   User: postgres
#   Password: postgres
#   Database: court_db

# Заполнить тестовыми данными
curl -X POST http://localhost:8000/api/seed

# Логи
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Локальная разработка

**Бэкенд:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Фронтенд:**
```bash
npm install
npm run dev
```

---

## 📁 Структура проекта

```
court-department/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Главная страница
│   ├── layout.tsx         # Корневой layout
│   └── globals.css        # Глобальные стили
├── backend/               # FastAPI Backend ⭐ NEW
│   ├── main.py           # API endpoints
│   ├── requirements.txt  # Python deps
│   └── Dockerfile
├── components/            # React компоненты
│   ├── AppealForm.tsx    # Форма обращений
│   └── ...
├── lib/                   # Утилиты
│   └── api.ts            # React hooks для API
├── nginx/                 # Nginx config
│   └── nginx.conf
├── docker-compose.yml     # Docker стек
└── README.md
```

---

## 🗄 Модели данных

### News (Новости)
```python
id: int
 title: str
 content: str
 excerpt: str
 image_url: str
 published_at: datetime
 is_published: bool
 category: str
 views: int
```

### Document (Документы)
```python
id: int
title: str
description: str
file_url: str
file_size: int
file_type: str
category: str
published_at: datetime
downloads: int
```

### Appeal (Обращения)
```python
id: int
full_name: str
email: str
phone: str
subject: str
message: str
created_at: datetime
status: str  # new, in_progress, resolved
response: str
responded_at: datetime
```

### Statistic (Статистика)
```python
id: int
year: int
region: str
total_cases: int
civil_cases: int
criminal_cases: int
arbitration_cases: int
updated_at: datetime
```

---

## 🎨 Дизайн-система

| Элемент | Значение |
|---------|----------|
| Primary | `#1a365d` (тёмно-синий) |
| Accent | `#f59e0b` (золотой) |
| Glass | `bg-white/80 backdrop-blur-xl` |
| Border | `border-white/20` |
| Shadow | `shadow-[0_8px_32px_rgba(31,38,135,0.15)]` |

---

## 📞 Контакты

**Судебный департамент при Верховном Суде РФ**

- 📍 121260, г. Москва, ул. Новый Арбат, д. 16
- 📞 +7 (495) 606-16-16
- ✉️ info@cdep.ru
- 🌐 https://cdep.ru

---

<div align="center">
  
  **⚖️ Создано с помощью [AI Правительства](https://github.com/DenMilenium/ai-pravitelstvo)**
  
  <br />
  
  🎨 Frontend • ⚙️ Backend • 🗄️ Database • 🐳 Docker
  
</div>
