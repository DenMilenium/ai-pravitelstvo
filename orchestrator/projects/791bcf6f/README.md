# ⚖️ Судебный департамент при Верховном суде РФ

<div align="center">
  
  ![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
  ![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
  ![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)
  ![Tailwind](https://img.shields.io/badge/Tailwind-3.0-06B6D4?style=for-the-badge&logo=tailwindcss)
  
  <strong>🎨 Создано AI Правительством | 🧠 AI/ML улучшения | ✨ Современный UX</strong>
  
  <br />
  <br />
  
  <a href="#-особенности">Особенности</a> •
  <a href="#-технологии">Технологии</a> •
  <a href="#-установка">Установка</a> •
  <a href="#-скриншоты">Скриншоты</a>
  
</div>

---

## ✨ Особенности

### 🎨 Дизайн
- **Glassmorphism UI** — современные стеклянные эффекты
- **Плавные анимации** — fade, slide, count-up
- **Градиенты** — красивые переходы цветов
- **Адаптивность** — mobile-first подход
- **Тёмная тема** — элегантный футер

### ⚡ Функциональность
- 🔐 **Личный кабинет** — вход в систему
- 📰 **Новости** — с фильтрами и поиском
- 📄 **Документы** — таблица с сортировкой
- 📊 **Статистика** — анимированные цифры
- 💻 **Электронное правосудие** — онлайн-сервисы
- 🔍 **Поиск** — умный поиск по сайту

### ♿ Доступность
- WCAG 2.1 AA совместимость
- Клавиатурная навигация
- Screen reader support
- Поддержка уменьшенной моторики

## 🛠 Технологии

| Категория | Технологии |
|-----------|-----------|
| **Frontend** | Next.js 14, React 18, TypeScript |
| **Стили** | Tailwind CSS, CSS Variables |
| **Иконки** | Lucide React |
| **Шрифты** | Inter (Google Fonts) |
| **Анимации** | Framer Motion (готовность) |
| **Backend** | FastAPI, Django |
| **DevOps** | Docker, Docker Compose |

## 🚀 Установка

### Требования
- Node.js 18+
- npm или yarn
- Docker (опционально)

### Быстрый старт

```bash
# Клонирование
git clone https://github.com/DenMilenium/court-department.git
cd court-department

# Установка зависимостей
npm install

# Запуск разработки
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000)

### Docker

```bash
# Запуск всего стека
docker-compose up -d

# Сервисы:
# - Frontend: http://localhost:3000
# - API: http://localhost:8000
# - CMS Admin: http://localhost:8001/admin
```

## 📁 Структура

```
court-department/
├── app/
│   ├── page.tsx          # Главная страница ✨
│   ├── layout.tsx        # Корневой layout
│   ├── globals.css       # Глобальные стили
│   └── ...
├── components/
│   ├── animations/       # Компоненты анимаций
│   ├── ui/              # UI компоненты
│   └── ...
├── lib/
│   └── utils.ts         # Утилиты
├── public/              # Статические файлы
├── backend/             # FastAPI
├── cms/                 # Django
└── docker-compose.yml
```

## 🎯 UI Components

### GlassCard
```tsx
<GlassCard className="p-6">
  <h3>Заголовок</h3>
  <p>Контент</p>
</GlassCard>
```

### CountUp
```tsx
<CountUp end={3200} duration={2000} />
```

### NewsCard
```tsx
<NewsCard
  date="15 марта 2024"
  title="Заголовок новости"
  excerpt="Описание..."
/>
```

## 📸 Скриншоты

### Главная страница
- Hero section с градиентом
- Анимированная статистика
- Glassmorphism карточки

### Электронное правосудие
- Grid сервисов
- Hover-эффекты
- Иконки Lucide

### Footer
- Тёмная тема
- Градиентные иконки
- Адаптивная сетка

## 🎨 Цветовая схема

| Цвет | HEX | Использование |
|------|-----|---------------|
| Primary | `#1e40af` | Основной синий |
| Accent | `#f59e0b` | Золотой акцент |
| Surface | `#ffffff` | Фон карточек |
| Background | `#f8fafc` | Фон страницы |
| Text | `#0f172a` | Основной текст |

## 🧠 AI Улучшения

Проект улучшен с помощью AI/ML агента:

- ✅ Анализ UX паттернов
- ✅ Оптимизация accessibility
- ✅ Микро-анимации
- ✅ Адаптивный дизайн
- ✅ Glassmorphism эффекты

## 📞 Контакты

**Судебный департамент при Верховном суде РФ**

- 📍 121260, Москва, ул. Новый Арбат, 16
- 📞 +7 (495) 606-16-16
- ✉️ info@court.gov.ru

## 📄 Лицензия

MIT License — см. [LICENSE](LICENSE)

---

<div align="center">
  
  **⚖️ Создано с помощью [AI Правительства](https://github.com/DenMilenium/ai-pravitelstvo)**
  
  <br />
  
  🧠 106 агентов • 🚀 10 задач • ⭐ 100% success rate
  
</div>
