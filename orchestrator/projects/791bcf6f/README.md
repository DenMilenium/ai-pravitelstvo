# ⚖️ Судебный департамент при Верховном суде РФ

Современный официальный веб-сайт Судебного департамента при Верховном суде Российской Федерации.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![React](https://img.shields.io/badge/React-18-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6)
![Tailwind](https://img.shields.io/badge/Tailwind-3.0-06B6D4)

## 📋 Описание

Проект представляет собой полнофункциональный веб-сайт для Судебного департамента с:
- Современным адаптивным дизайном
- Разделом электронного правосудия
- Системой новостей и документов
- Интерактивной статистикой
- Личным кабинетом участников процесса

## 🎨 Дизайн-система

### Цветовая палитра
| Цвет | HEX | Применение |
|------|-----|------------|
| Тёмно-синий | `#1a365d` | Основной, шапка, футер |
| Золотой | `#d4af37` | Акценты, кнопки |
| Белый | `#ffffff` | Фон карточек |
| Серый | `#f5f5f5` | Фон секций |

### Типографика
- **Заголовки**: system-ui, bold
- **Текст**: system-ui, regular
- **Размеры**: 4xl (hero), 3xl (h2), xl (h3)

## 🚀 Быстрый старт

### Требования
- Node.js 18+
- npm или yarn

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/DenMilenium/court-department.git
cd court-department

# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

### Сборка для production

```bash
npm run build
npm start
```

## 📁 Структура проекта

```
court-department/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Главная страница
│   ├── layout.tsx         # Корневой layout
│   ├── globals.css        # Глобальные стили
│   ├── news/              # Раздел новостей
│   ├── documents/         # Раздел документов
│   ├── statistics/        # Статистика
│   └── e-justice/         # Электронное правосудие
├── components/            # React компоненты
│   ├── ui/               # Базовые компоненты
│   ├── news/             # Компоненты новостей
│   ├── documents/        # Компоненты документов
│   └── statistics/       # Компоненты статистики
├── lib/                   # Утилиты
│   ├── utils.ts
│   └── data.ts           # Моковые данные
├── public/               # Статические файлы
├── backend/              # FastAPI backend
│   ├── main.py
│   └── routers/
├── cms/                  # Django CMS
│   └── content/
└── docker-compose.yml    # Docker конфигурация
```

## ✨ Функциональность

### 🏠 Главная страница
- Hero-секция с призывом к действию
- Блок статистики (судов, судей, дел)
- Быстрые ссылки на сервисы
- Последние новости

### 📰 Новости
- Лента новостей с пагинацией
- Фильтрация по категориям
- Поиск по заголовкам
- Карточки новостей с датами

### 📄 Документы
- Таблица нормативных актов
- Поиск по названию
- Фильтры по типу
- Скачивание PDF

### 📊 Статистика
- Интерактивные графики
- Динамика за 5 лет
- Категории дел
- Региональное распределение

### 💻 Электронное правосудие
- Подача исковых заявлений
- Проверка статуса дела
- Оплата госпошлин
- Видеоконференцсвязь

## 🛠 Технологический стек

### Frontend
- **Next.js 14** - React framework
- **React 18** - UI библиотека
- **TypeScript** - Типизация
- **Tailwind CSS** - Стилизация
- **Lucide React** - Иконки
- **Recharts** - Графики

### Backend
- **FastAPI** - Python API
- **SQLAlchemy** - ORM
- **SQLite/PostgreSQL** - БД
- **JWT** - Авторизация

### CMS
- **Django** - Админ-панель
- **CKEditor** - Редактор контента

### DevOps
- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация
- **Nginx** - Reverse proxy

## 🔧 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/news` | Список новостей |
| GET | `/api/news/:id` | Одна новость |
| GET | `/api/documents` | Список документов |
| POST | `/api/auth/login` | Вход в систему |
| POST | `/api/auth/register` | Регистрация |
| GET | `/api/statistics` | Данные статистики |

## 🐳 Docker

```bash
# Запуск всего стека
docker-compose up -d

# Остановка
docker-compose down
```

Сервисы:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- CMS Admin: http://localhost:8001/admin

## 📞 Контакты

**Судебный департамент при Верховном суде РФ**

- 📍 Адрес: 121260, Москва, ул. Новый Арбат, 16
- 📞 Телефон: +7 (495) 606-16-16
- ✉️ Email: info@court.gov.ru
- 🌐 Сайт: https://court.gov.ru

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

⚖️ Создано с помощью AI Правительства | 2024
