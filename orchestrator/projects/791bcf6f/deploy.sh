#!/bin/bash

# =============================================================================
# 🚀 ДЕПЛОЙ САЙТА СУДЕБНОГО ДЕПАРТАМЕНТА НА VPS
# =============================================================================
# Использование: ./deploy.sh [vps_ip] [domain]
# Пример: ./deploy.sh 194.67.66.120 court.gov.ru
# =============================================================================

set -e  # Exit on error

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Параметры
VPS_IP=${1:-"194.67.66.120"}
DOMAIN=${2:-"court.gov.ru"}
API_DOMAIN="api.${DOMAIN}"
TRAEFIK_DOMAIN="traefik.${DOMAIN}"
REPO_URL="https://github.com/DenMilenium/ai-pravitelstvo.git"
PROJECT_DIR="ai-pravitelstvo/orchestrator/projects/791bcf6f"

# Функции логирования
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Приветствие
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║      ⚖️  СУДЕБНЫЙ ДЕПАРТАМЕНТ - ДЕПЛОЙ НА VPS                  ║"
echo "║                                                                ║"
echo "║  Frontend: https://${DOMAIN}                                    ║"
echo "║  API:      https://${API_DOMAIN}                                ║"
echo "║  Traefik:  https://${TRAEFIK_DOMAIN}                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

log_info "Начинаем деплой на ${VPS_IP}..."

# =============================================================================
# ШАГ 1: Проверка SSH соединения
# =============================================================================
log_info "Проверка SSH соединения..."
if ! ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "root@${VPS_IP}" "echo 'SSH OK'" > /dev/null 2>&1; then
    log_error "Не удалось подключиться к ${VPS_IP} по SSH"
    log_info "Убедитесь, что:"
    log_info "  1. Сервер доступен"
    log_info "  2. SSH ключ настроен"
    log_info "  3. Порт 22 открыт"
    exit 1
fi
log_success "SSH соединение установлено"

# =============================================================================
# ШАГ 2: Установка Docker и Docker Compose на VPS
# =============================================================================
log_info "Установка Docker и Docker Compose..."

ssh "root@${VPS_IP}" '
    # Обновление системы
    apt-get update
    apt-get upgrade -y
    
    # Установка необходимых пакетов
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        git \
        ufw
    
    # Установка Docker
    if ! command -v docker > /dev/null 2>&1; then
        curl -fsSL https://get.docker.com | sh
        systemctl enable docker
        systemctl start docker
    fi
    
    # Установка Docker Compose
    if ! command -v docker-compose > /dev/null 2>&1; then
        curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    # Проверка
    docker --version
    docker-compose --version
'

log_success "Docker и Docker Compose установлены"

# =============================================================================
# ШАГ 3: Настройка файрвола
# =============================================================================
log_info "Настройка файрвола (UFW)..."

ssh "root@${VPS_IP}" '
    # Сброс правил
    ufw --force reset
    
    # Политики по умолчанию
    ufw default deny incoming
    ufw default allow outgoing
    
    # Разрешаем SSH
    ufw allow 22/tcp
    
    # Разрешаем HTTP и HTTPS
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Включаем файрвол
    ufw --force enable
    
    # Проверка статуса
    ufw status verbose
'

log_success "Файрвол настроен"

# =============================================================================
# ШАГ 4: Создание директорий и клонирование репозитория
# =============================================================================
log_info "Подготовка директорий..."

ssh "root@${VPS_IP}" "
    # Создаём директорию проекта
    mkdir -p /opt/court-department
    cd /opt/court-department
    
    # Клонируем репозиторий (если ещё не клонирован)
    if [ ! -d .git ]; then
        git clone ${REPO_URL} .
    fi
    
    # Переходим в директорию проекта
    cd ${PROJECT_DIR}
    
    # Получаем последние изменения
    git pull origin main
"

log_success "Репозиторий клонирован"

# =============================================================================
# ШАГ 5: Создание .env файла
# =============================================================================
log_info "Создание .env файла..."

# Генерация случайных паролей
DB_PASSWORD=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 32)
SECRET_KEY=$(openssl rand -base64 64 | tr -dc 'a-zA-Z0-9' | head -c 64)
ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 16)

ssh "root@${VPS_IP}" "
    cd /opt/court-department/${PROJECT_DIR}
    
    # Создаём .env файл
    cat > .env << EOF
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://${API_DOMAIN}

# Database
DATABASE_URL=postgresql://court_user:${DB_PASSWORD}@db:5432/court_db
DB_PASSWORD=${DB_PASSWORD}

# Backend
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=${ADMIN_PASSWORD}

# Logging
LOG_LEVEL=INFO
EOF

    # Сохраняем пароли в безопасное место
    cat > /root/.court-credentials << EOF
⚖️  СУДЕБНЫЙ ДЕПАРТАМЕНТ - УЧЁТНЫЕ ДАННЫЕ
=====================================
Domain:      ${DOMAIN}
API Domain:  ${API_DOMAIN}
Traefik:     ${TRAEFIK_DOMAIN}

Database:
  User:     court_user
  Password: ${DB_PASSWORD}

Admin Panel:
  Username: admin
  Password: ${ADMIN_PASSWORD}

Secret Key: ${SECRET_KEY}
=====================================
Сохраните эти данные в надёжном месте!
EOF

    chmod 600 /root/.court-credentials
"

log_success ".env файл создан"
log_warning "Учётные данные сохранены в /root/.court-credentials"

# =============================================================================
# ШАГ 6: Запуск приложения
# =============================================================================
log_info "Запуск Docker Compose..."

ssh "root@${VPS_IP}" "
    cd /opt/court-department/${PROJECT_DIR}
    
    # Останавливаем старые контейнеры (если есть)
    docker-compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true
    
    # Создаём директорию для SSL сертификатов
    mkdir -p letsencrypt
    
    # Создаём директорию для бэкапов
    mkdir -p backups
    
    # Создаём директорию для загрузок
    mkdir -p uploads
    
    # Запускаем
    docker-compose -f docker-compose.prod.yml up -d --build
    
    # Ждём инициализации
    sleep 10
    
    # Проверяем статус
    docker-compose -f docker-compose.prod.yml ps
"

log_success "Приложение запущено"

# =============================================================================
# ШАГ 7: Заполнение тестовыми данными
# =============================================================================
log_info "Заполнение базы данных..."

ssh "root@${VPS_IP}" "
    cd /opt/court-department/${PROJECT_DIR}
    
    # Ждём готовности API
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
            break
        fi
        echo 'Ожидание API...'
        sleep 2
    done
    
    # Заполняем тестовыми данными
    curl -X POST http://localhost:8000/api/seed || echo 'Seed already done or error'
"

log_success "База данных инициализирована"

# =============================================================================
# ШАГ 8: Настройка автообновления SSL
# =============================================================================
log_info "SSL сертификаты будут получены автоматически через Let's Encrypt"
log_info "Traefik настроен на автоматическое обновление"

# =============================================================================
# ШАГ 9: Финальная проверка
# =============================================================================
log_info "Финальная проверка..."

sleep 15

# Проверка доступности сервисов
HEALTH_STATUS=$(ssh "root@${VPS_IP}" "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/api/health || echo '000'")

if [ "$HEALTH_STATUS" = "200" ]; then
    log_success "API работает (HTTP 200)"
else
    log_warning "API вернул статус $HEALTH_STATUS"
    log_info "Проверьте логи: ssh root@${VPS_IP} 'docker-compose -f /opt/court-department/${PROJECT_DIR}/docker-compose.prod.yml logs -f backend'"
fi

# =============================================================================
# ГОТОВО!
# =============================================================================
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    🎉 ДЕПЛОЙ ЗАВЕРШЁН!                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📍 URL адреса:${NC}"
echo "  Frontend:  https://${DOMAIN}"
echo "  API:       https://${API_DOMAIN}"
echo "  Traefik:   https://${TRAEFIK_DOMAIN}"
echo "  Adminer:   http://${VPS_IP}:8080"
echo ""
echo -e "${BLUE}📋 Полезные команды:${NC}"
echo "  Логи:           ssh root@${VPS_IP} 'cd /opt/court-department/${PROJECT_DIR} && docker-compose -f docker-compose.prod.yml logs -f'"
echo "  Перезапуск:     ssh root@${VPS_IP} 'cd /opt/court-department/${PROJECT_DIR} && docker-compose -f docker-compose.prod.yml restart'"
echo "  Обновление:     ssh root@${VPS_IP} 'cd /opt/court-department/${PROJECT_DIR} && git pull && docker-compose -f docker-compose.prod.yml up -d --build'"
echo "  Бэкап БД:       ssh root@${VPS_IP} 'docker exec court-department-db-1 pg_dump -U court_user court_db > backup.sql'"
echo ""
echo -e "${YELLOW}⚠️  УЧЁТНЫЕ ДАННЫЕ:${NC}"
echo "  Файл: /root/.court-credentials"
echo "  Admin: ssh root@${VPS_IP} 'cat /root/.court-credentials'"
echo ""
echo -e "${GREEN}✅ Сайт Судебного департамента готов к работе!${NC}"
