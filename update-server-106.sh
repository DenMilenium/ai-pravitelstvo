#!/bin/bash
# update-server-106.sh - Обновление до 106 агентов

echo "🚀 AI Правительство - Обновление сервера"
echo "========================================="

cd /var/www/ai-pravitelstvo

echo ""
echo "📥 Получение обновлений..."
git pull origin main

echo ""
echo "📊 Текущий статус:"
git log --oneline -3

echo ""
echo "🔄 Перезапуск сервиса..."
systemctl daemon-reload
systemctl restart ai-dashboard

echo ""
echo "✅ Проверка статуса..."
sleep 2
systemctl status ai-dashboard --no-pager

echo ""
echo "🎯 Обновление завершено!"
echo "Откройте: http://194.67.66.120"
