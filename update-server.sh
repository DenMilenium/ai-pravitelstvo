#!/bin/bash
# 🔧 ФИНАЛЬНОЕ ОБНОВЛЕНИЕ СЕРВЕРА AI Правительство
# Запускать: sudo bash /tmp/update-server.sh

set -e  # Остановить при ошибке

echo "🚀 Начинаю обновление AI Правительство..."
echo ""

# 1. Переходим в директорию
cd /var/www/ai-pravitelstvo

# 2. Останавливаем сервис
echo "🛑 Останавливаю сервис..."
systemctl stop ai-dashboard

# 3. Получаем последние изменения
echo "📥 Получаю изменения из GitHub..."
git fetch origin
git reset --hard origin/main

# 4. Проверяем последний коммит
echo "✅ Последние изменения:"
git log --oneline -3

# 5. Устанавливаем зависимости
echo "📦 Устанавливаю зависимости..."
source dashboard/venv/bin/activate
pip install requests flask-cors werkzeug -q

# 6. Проверяем и создаём .env файл с секретом (если нет)
if [ ! -f "/var/www/ai-pravitelstvo/.env" ]; then
    echo "🔐 Создаю .env файл..."
    cat > /var/www/ai-pravitelstvo/.env << 'EOF'
FLASK_SECRET_KEY=ai-pravitelstvo-secret-key-2024-fixed
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=DenMilenium/ai-pravitelstvo
EOF
fi

# 7. Обновляем службу systemd
echo "⚙️ Обновляю службу..."
cat > /etc/systemd/system/ai-dashboard.service << 'EOF'
[Unit]
Description=AI Правительство Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/ai-pravitelstvo/dashboard
Environment="PATH=/var/www/ai-pravitelstvo/dashboard/venv/bin"
Environment="PYTHONPATH=/var/www/ai-pravitelstvo"
Environment="FLASK_SECRET_KEY=ai-pravitelstvo-secret-key-2024-fixed"
Environment="GITHUB_TOKEN=INSERT_YOUR_GITHUB_TOKEN_HERE"
Environment="GITHUB_REPO=DenMilenium/ai-pravitelstvo"
ExecStart=/var/www/ai-pravitelstvo/dashboard/venv/bin/gunicorn -w 2 -b 127.0.0.1:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 8. Перезагружаем systemd
systemctl daemon-reload

# 9. Запускаем сервис
echo "🚀 Запускаю сервис..."
systemctl start ai-dashboard

# 10. Проверяем статус
echo ""
echo "📊 Статус сервиса:"
systemctl status ai-dashboard --no-pager

echo ""
echo "✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "🔗 Проверь сайт: http://194.67.66.120"
echo "🔑 Логин: admin / Пароль: admin123"
echo ""
echo "📋 Проверь:"
echo "   1. Вход должен работать и СОХРАНЯТЬСЯ"
echo "   2. Переход в Проекты не должен разлогинивать"
echo "   3. Прогресс должен показывать реальные проценты"
