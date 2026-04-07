# 🚀 Инструкция по обновлению сервера

## Подключение к серверу

```bash
ssh root@194.67.66.120
# Введите пароль при запросе
```

## Обновление (выполнить на сервере)

```bash
# Перейти в директорию
cd /var/www/ai-pravitelstvo

# Получить обновления
git pull origin main

# Проверить статус
git log --oneline -3
```

Вы должны увидеть:
```
75063c3 📚 ЭТАП D: Полная документация
ef8d9b3 🎨 ЭТАП C: Каталог агентов
ad71566 ✅ Добавлены Go и Angular агенты
```

## Перезапуск сервиса

```bash
# Перезагрузить systemd
systemctl daemon-reload

# Перезапустить Dashboard
systemctl restart ai-dashboard

# Проверить статус
systemctl status ai-dashboard
```

Должно показать: `Active: active (running)`

## Проверка

Откройте в браузере: http://194.67.66.120

### Что проверить:
1. ✅ Вход в Dashboard (admin / admin123)
2. ✅ Переход в раздел "🤖 Агенты" - должно показывать 106 агентов
3. ✅ Поиск агентов работает
4. ✅ Фильтры по категориям работают

## В случае ошибок

```bash
# Посмотреть логи
journalctl -u ai-dashboard -n 50 --no-pager

# Перезапуск если что-то не так
systemctl restart ai-dashboard
```
