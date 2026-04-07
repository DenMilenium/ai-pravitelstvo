# 🤖 AI Правительство - Документация

## 📋 Содержание

1. [Общая информация](#общая-информация)
2. [Быстрый старт](#быстрый-старт)
3. [Каталог агентов](#каталог-агентов)
4. [Как использовать агентов](#как-использовать-агентов)
5. [API Reference](#api-reference)
6. [Развертывание](#развертывание)

---

## Общая информация

**AI Правительство** — это AI IT-компания с 106 агентами-разработчиками, каждый из которых специализируется на своей технологии.

### 🏛️ Структура

```
ai-pravitelstvo/
├── 🖥️ ministries/desktop/     # Десктопные приложения
├── ☁️ ministries/cloud/        # Облачные решения
├── 🔬 ministries/research/     # Исследования
├── 📊 ministries/pm/           # Управление проектами
├── 🏗️ ministries/infrastructure/ # Инфраструктура
├── 👥 ministries/hr/           # Кадры
└── 📋 ministries/advisory/     # Консультации
```

### 🎯 Возможности

- ✅ **106 агентов** — от Frontend до Blockchain
- ✅ **Генерация кода** — каждый агент создает реальный код
- ✅ **Dashboard** — веб-интерфейс управления
- ✅ **GitHub интеграция** — автопуш и PR
- ✅ **WebSocket** — live-обновления

---

## Быстрый старт

### 1. Установка

```bash
git clone https://github.com/DenMilenium/ai-pravitelstvo.git
cd ai-pravitelstvo
```

### 2. Запуск Dashboard

```bash
cd dashboard
pip install -r requirements.txt
python app.py
```

### 3. Доступ

- Dashboard: http://localhost:5000
- Логин: `admin`
- Пароль: `admin123`

---

## Каталог агентов

### ⚛️ Frontend (14 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| ⚛️ React Agent | `react` | React приложения: Dashboard, Form, Landing, App |
| ⚡ Vue Agent | `vue` | Vue 3 с Composition API |
| 🅰️ Angular Agent | `angular` | Angular с TypeScript |
| 🟥 Svelte Agent | `svelte` | Svelte приложения |
| ▲ Next.js Agent | `nextjs` | Full-stack React с SSR |
| ⛰️ Nuxt Agent | `nuxt` | Vue с SSR |
| 🎸 Remix Agent | `remix` | Full-stack React |
| 📝 WordPress Agent | `wordpress` | WordPress темы и плагины |
| 🛍️ Shopify Agent | `shopify` | Shopify темы и Liquid |
| ⚡ Gatsby Agent | `gatsby` | Static site generator |
| 🤗 Hugo Agent | `hugo` | Go-based SSG |
| 💎 Jekyll Agent | `jekyll` | Ruby SSG |
| 🚀 Astro Agent | `astro` | Fast SSG |
| 🪟 Electron Agent | `electron` | Desktop приложения |

### 🖥️ Backend (9 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| 🐍 Django Agent | `django` | Django/DRF бэкенд |
| 🔥 FastAPI Agent | `fastapi` | Async Python API |
| 🟢 Node.js Agent | `nodejs` | Express/NestJS |
| 🐹 Go Agent | `go` | Go/Gin высокая производительность |
| 💎 Ruby Agent | `ruby` | Ruby on Rails |
| 🐘 Laravel Agent | `laravel` | PHP Laravel |
| ☕ Java Agent | `java` | Spring Boot |
| #️⃣ C# Agent | `csharp` | .NET Core |
| 🦀 Rust Agent | `rust` | Actix-web |

### 📱 Mobile (5 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| 📱 Flutter Agent | `flutter` | Кросс-платформенные приложения |
| 🍎 iOS Agent | `ios` | Swift/SwiftUI для iOS |
| 🤖 Android Agent | `android` | Kotlin/Jetpack Compose |
| ⚛️ React Native Agent | `react-native` | React для мобильных |
| 📱 PWA Agent | `pwa` | Progressive Web Apps |

### ☁️ Cloud & DevOps (18 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| ☁️ AWS Agent | `aws` | Terraform для AWS |
| 🔷 Azure Agent | `azure` | Microsoft Azure |
| 🔵 GCP Agent | `gcp` | Google Cloud |
| 🐳 Docker Agent | `docker` | Dockerfile и compose |
| ☸️ Kubernetes Agent | `kubernetes` | K8s и Helm |
| 🏗️ Terraform Agent | `terraform` | Infrastructure as Code |
| 🔄 GitHub Actions Agent | `github-actions` | CI/CD для GitHub |
| 🦊 GitLab CI Agent | `gitlab-ci` | GitLab CI/CD |
| 🏗️ Jenkins Agent | `jenkins` | Jenkins pipelines |
| 🌐 Nginx Agent | `nginx` | Nginx конфигурация |
| 🪶 Apache Agent | `apache` | Apache HTTP Server |
| 🌎 CDN Agent | `cdn` | Cloudflare/AWS CloudFront |
| 🔐 SSL Agent | `ssl` | SSL/TLS настройки |

### 🗄️ Database (9 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| 🐘 PostgreSQL Agent | `postgres` | PostgreSQL схемы |
| 🍃 MongoDB Agent | `mongodb` | NoSQL схемы |
| 🔴 Redis Agent | `redis` | Кеширование |
| 🐬 MySQL Agent | `mysql` | MySQL схемы |
| 🔍 Elasticsearch Agent | `elasticsearch` | Поиск и аналитика |
| 🗄️ Database Agent | `database` | Универсальная работа с БД |
| 🌐 GraphQL Agent | `graphql` | GraphQL схемы |
| 📨 Kafka Agent | `kafka` | Apache Kafka streams |
| 🐇 RabbitMQ Agent | `rabbitmq` | Message queue |

### 🧪 Testing & Monitoring (8 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| 📈 Prometheus Agent | `prometheus` | Метрики |
| 📊 Grafana Agent | `grafana` | Dashboard |
| 🐛 Sentry Agent | `sentry` | Error tracking |
| 🚀 LogRocket Agent | `logrocket` | Session replay |
| 📊 Analytics Agent | `analytics` | Tracking |
| 🧪 Testing Agent | `testing` | Unit/Integration тесты |
| 🧪 Jest Agent | `jest` | JavaScript тесты |
| 🌲 Cypress Agent | `cypress` | E2E тесты |
| 🎭 Playwright Agent | `playwright` | Cross-browser тесты |
| 🎨 Chromatic Agent | `chromatic` | Visual regression |

### 🛠️ Utilities (19 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| 📋 Swagger Agent | `swagger` | OpenAPI спецификации |
| 📮 Postman Agent | `postman` | API коллекции |
| 📖 Storybook Agent | `storybook` | UI документация |
| 🔍 ESLint Agent | `eslint` | JavaScript линтинг |
| ✨ Prettier Agent | `prettier` | Форматирование |
| 🔷 TypeScript Agent | `tsconfig` | TS конфигурация |
| 📦 Webpack Agent | `webpack` | Module bundler |
| ⚡ Vite Agent | `vite` | Fast build tool |
| 📦 Rollup Agent | `rollup` | JS bundler |
| 📦 Parcel Agent | `parcel` | Zero-config bundler |
| 🛠️ Makefile Agent | `makefile` | Build automation |
| 🐚 Bash Agent | `bash` | Shell скрипты |
| 💻 PowerShell Agent | `powershell` | Windows scripting |
| ⏰ Cron Agent | `cron` | Scheduled tasks |
| 🎣 Webhook Agent | `webhook` | Webhook handlers |

### ✨ Special (17 агентов)

| Агент | Тип | Описание |
|-------|-----|----------|
| 🧠 AI/ML Agent | `ai` | Machine learning |
| 💬 Chatbot Agent | `chatbot` | Чат-боты |
| 🎮 GameDev Agent | `gamedev` | Game development |
| 🔍 SEO Agent | `seo` | SEO оптимизация |
| 📝 Content Agent | `content` | Генерация контента |
| 📚 Documentation Agent | `documentation` | Документация |
| 🔒 Security Agent | `security` | Security audit |
| ⚡ Performance Agent | `performance` | Оптимизация |
| ♿ Accessibility Agent | `accessibility` | a11y compliance |
| 🌍 Localization Agent | `localization` | i18n и переводы |
| 📧 Email Agent | `email` | Email сервисы |
| 🔔 Notification Agent | `notifications` | Push notifications |
| 💾 Backup Agent | `backup` | Backup стратегии |
| 🚚 Migration Agent | `migration` | Data migrations |
| ⛓️ Web3 Agent | `web3` | Blockchain |
| 📡 IoT Agent | `iot` | IoT и embedded |
| 🥽 AR/VR Agent | `arvr` | Augmented/Virtual reality |
| 🎤 Voice Agent | `voice` | Voice interfaces |
| 📄 PDF Agent | `pdf` | PDF генерация |
| 📊 Spreadsheet Agent | `spreadsheet` | Excel/CSV |
| 🔲 QR Code Agent | `qrcode` | QR коды |
| 🖼️ Image Processing Agent | `image-processing` | Обработка изображений |
| 🎬 Video Agent | `video` | Видео обработка |
| 🎵 Audio Agent | `audio` | Аудио обработка |
| 🕷️ Web Scraping Agent | `scraping` | Web scraping |

---

## Как использовать агентов

### Через Dashboard

1. Перейдите в раздел **Проекты**
2. Нажмите **Создать проект**
3. Выберите тип агента
4. Опишите задачу
5. Нажмите **▶️ Выполнить**
6. Скачайте ZIP с кодом

### Через API

```bash
# Создать задачу
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj-001",
    "title": "Создать React Dashboard",
    "agent_type": "react"
  }'

# Выполнить задачу
curl -X POST http://localhost:5000/api/tasks/TASK_ID/execute
```

---

## API Reference

### Projects API

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/projects` | GET | Список проектов |
| `/api/projects` | POST | Создать проект |
| `/api/projects/<id>` | GET | Детали проекта |
| `/api/projects/<id>/zip` | GET | Скачать ZIP |

### Tasks API

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/tasks` | GET | Список задач |
| `/api/tasks` | POST | Создать задачу |
| `/api/tasks/<id>/execute` | POST | Выполнить задачу |

### Agents API

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/agents` | GET | Список агентов |
| `/api/agents/catalog` | GET | Каталог агентов |
| `/api/agents/<id>/test` | POST | Тест агента |

---

## Развертывание

### На сервере (Reg.ru)

1. Скачайте ZIP из Dashboard
2. Загрузите на сервер через FTP/SSH
3. Распакуйте: `unzip project.zip`
4. Следуйте README внутри архива

### Автоматически (не рекомендуется)

```bash
cd orchestrator
python deploy_agent.py
```

---

## 🤝 Contributing

Приветствуются PR! Смотрите [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - смотрите [LICENSE](LICENSE)

---

## 👨‍💻 Автор

**Срибный Денис Вячеславович**
- GitHub: [@DenMilenium](https://github.com/DenMilenium)
- Сайт: [sribnyydenis.online](https://sribnyydenis.online)

---

*Создано с ❤️ и 106 агентами*
