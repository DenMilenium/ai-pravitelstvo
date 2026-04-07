# 🚀 ДЕПЛОЙ НА VPS - ИНСТРУКЦИЯ

## ⚡ Быстрый старт (автоматический деплой)

```bash
# На вашей локальной машине
chmod +x deploy.sh
./deploy.sh 194.67.66.120 court.gov.ru
```

Скрипт автоматически:
- ✅ Установит Docker и Docker Compose
- ✅ Настроит файрвол
- ✅ Клонирует репозиторий
- ✅ Создаст `.env` с секретами
- ✅ Запустит всё в Docker
- ✅ Получит SSL сертификаты
- ✅ Заполнит тестовыми данными

---

## 📋 Предварительные требования

### 1. VPS Сервер
- **OS:** Ubuntu 20.04+ или Debian 11+
- **RAM:** минимум 2GB (рекомендуется 4GB)
- **CPU:** 2 ядра
- **Disk:** 20GB SSD
- **IP:** 194.67.66.120 (или ваш)

### 2. Доменное имя
- **A-запись:** `court.gov.ru` → `194.67.66.120`
- **A-запись:** `api.court.gov.ru` → `194.67.66.120`
- **A-запись:** `traefik.court.gov.ru` → `194.67.66.120`

### 3. SSH доступ
```bash
# Проверка доступа
ssh root@194.67.66.120
```

---

## 🔧 Ручной деплой (если автоматический не сработал)

### Шаг 1: Подключение к серверу
```bash
ssh root@194.67.66.120
```

### Шаг 2: Установка Docker
```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверка
docker --version
docker-compose --version
```

### Шаг 3: Настройка файрвола
```bash
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp      # SSH
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw --force enable
ufw status
```

### Шаг 4: Клонирование проекта
```bash
mkdir -p /opt/court-department
cd /opt/court-department
git clone https://github.com/DenMilenium/ai-pravitelstvo.git .
cd orchestrator/projects/791bcf6f
```

### Шаг 5: Создание .env файла
```bash
cat > .env << 'EOF'
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.court.gov.ru

# Database
DATABASE_URL=postgresql://court_user:STRONG_PASSWORD@db:5432/court_db
DB_PASSWORD=STRONG_PASSWORD

# Backend
SECRET_KEY=YOUR_SECRET_KEY_HERE
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=ADMIN_PASSWORD_HERE

# Logging
LOG_LEVEL=INFO
EOF
```

**⚠️ Важно:** Замените `STRONG_PASSWORD` и `YOUR_SECRET_KEY_HERE` на реальные значения!

### Шаг 6: Запуск
```bash
# Создаём директории
mkdir -p letsencrypt backups uploads

# Запуск
docker-compose -f docker-compose.prod.yml up -d --build

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

### Шаг 7: Инициализация данных
```bash
# Ждём готовности API (30 секунд)
sleep 30

# Заполняем тестовыми данными
curl -X POST http://localhost:8000/api/seed
```

---

## 🌐 Доступ к сервисам

После успешного деплоя:

| Сервис | URL | Описание |
|--------|-----|----------|
| Frontend | https://court.gov.ru | Основной сайт |
| API | https://api.court.gov.ru | REST API |
| Traefik | https://traefik.court.gov.ru | Панель управления |
| Adminer | http://194.67.66.120:8080 | Управление БД |

---

## 📊 Полезные команды

```bash
# Подключение к серверу
ssh root@194.67.66.120

cd /opt/court-department/orchestrator/projects/791bcf6f

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Остановка
docker-compose -f docker-compose.prod.yml down

# Полное удаление с данными
docker-compose -f docker-compose.prod.yml down -v

# Обновление кода и перезапуск
git pull
docker-compose -f docker-compose.prod.yml up -d --build

# Бэкап базы данных
docker exec court-department-db-1 pg_dump -U court_user court_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление из бэкапа
docker exec -i court-department-db-1 psql -U court_user court_db < backup.sql

# Проверка использования ресурсов
docker stats

# Очистка неиспользуемых образов
docker system prune -a
```

---

## 🔒 SSL Сертификаты

SSL сертификаты от Let's Encrypt получаются **автоматически** при первом запуске.

### Ручное обновление
```bash
docker-compose -f docker-compose.prod.yml restart traefik
```

### Проверка сертификата
```bash
curl -vI https://court.gov.ru 2>&1 | grep -i ssl
```

---

## 🗄️ Управление базой данных

### Через Adminer (веб-интерфейс)
1. Откройте http://194.67.66.120:8080
2. Система: PostgreSQL
3. Сервер: db
4. Пользователь: court_user
5. Пароль: (из .env файла)
6. База: court_db

### Через CLI
```bash
# Подключение к контейнеру БД
docker exec -it court-department-db-1 psql -U court_user court_db

# SQL запросы
SELECT * FROM news;
SELECT * FROM appeals WHERE status = 'new';
```

---

## 🐛 Отладка

### API не отвечает
```bash
# Проверка контейнера
docker ps | grep backend

# Логи ошибок
docker-compose -f docker-compose.prod.yml logs backend | tail -50

# Проверка внутри контейнера
docker exec -it court-department-backend-1 /bin/sh
```

### Frontend не загружается
```bash
# Проверка сборки
docker-compose -f docker-compose.prod.yml logs frontend

# Пересборка
docker-compose -f docker-compose.prod.yml up -d --build frontend
```

### Проблемы с SSL
```bash
# Проверка сертификатов
docker-compose -f docker-compose.prod.yml logs traefik

# Удаление и повторное получение
rm -rf letsencrypt/*
docker-compose -f docker-compose.prod.yml restart traefik
```

---

## 📈 Мониторинг

### Health Check
```bash
curl https://api.court.gov.ru/api/health
```

### Traefik Dashboard
- URL: https://traefik.court.gov.ru
- Логин/пароль: admin/admin (измените в docker-compose.prod.yml!)

---

## 🔄 CI/CD (GitHub Actions)

Для автоматического деплоя при пуше в main:

1. Создайте файл `.github/workflows/deploy.yml`
2. Добавьте секреты в GitHub: `VPS_HOST`, `VPS_USER`, `VPS_KEY`

Пример workflow:
```yaml
name: Deploy to VPS
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_KEY }}
          script: |
            cd /opt/court-department/orchestrator/projects/791bcf6f
            git pull
            docker-compose -f docker-compose.prod.yml up -d --build
```

---

## 💾 Резервное копирование

### Автоматическое (уже настроено)
Бэкапы создаются каждый день в 2:00 в папку `./backups/`

### Ручное
```bash
# Бэкап БД
docker exec court-department-db-1 pg_dump -U court_user court_db > backup.sql

# Бэкап uploads
rsync -avz uploads/ backup/uploads/

# Бэкап всего проекта
cd /opt
tar -czvf court-department-backup-$(date +%Y%m%d).tar.gz court-department/
```

---

## 📞 Поддержка

При проблемах:
1. Проверьте логи: `docker-compose logs -f`
2. Проверьте статус: `docker-compose ps`
3. Проверьте ресурсы: `docker stats`
4. Перезапустите: `docker-compose restart`

---

## ✅ Чеклист

- [ ] VPS сервер с Ubuntu 20.04+
- [ ] SSH доступ настроен
- [ ] Доменное имя (court.gov.ru)
- [ ] DNS A-записи настроены
- [ ] Порты 80, 443 открыты
- [ ] Минимум 2GB RAM
- [ ] .env файл создан
- [ ] SSL автоматически получен
- [ ] Сайт доступен по HTTPS
- [ ] API отвечает на /api/health

---

**🎉 Готово! Ваш сайт Судебного департамента запущен!**
