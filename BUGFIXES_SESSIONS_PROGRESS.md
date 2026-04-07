# 🐛 ИСПРАВЛЕНИЯ: Сессии + Прогресс

## Проблема 1: Постоянный разлогин (СЕССИИ)

### Симптомы:
- Вошёл в систему
- Перешёл в "Проекты"
- Снова просит логин!
- При каждой перезагрузке сервера разлогинивает

### Причина:
```python
app.secret_key = os.urandom(24)  # ❌ Новый ключ при каждом запуске!
```

`os.urandom(24)` генерирует **случайный ключ** при каждом старте приложения.  
Fl использует этот ключ для шифрования сессий.  
Если ключ меняется — сессии становятся невалидными!

### Решение:
```python
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'ai-pravitelstvo-secret-key-2024-fixed')
# ✅ Теперь ключ постоянный (или из переменной окружения)
```

---

## Проблема 2: Прогресс не двигается (10%)

### Симптомы:
- Создал проект
- Прогресс показывает 10% (или 0%)
- Нажимаешь "Выполнить задачу" — прогресс не меняется
- Ползунок стоит на месте

### Причина:
```python
# В коде:
task.status = TaskStatus.DONE  # Enum объект

# В шаблоне:
task.status == 'done'  # Сравнение Enum со строкой

# Результат: всегда False!
```

### Решение:
```python
tasks_dict = [task.to_dict() for task in tasks]
# task.to_dict() делает status = 'done' (строка)
# Теперь сравнение работает!
```

---

## ✅ ОБА ИСПРАВЛЕНИЯ В КОДЕ

### Файл: `dashboard/app.py`

**Изменение 1 (сессии):**
```python
# Было:
app.secret_key = os.urandom(24)

# Стало:
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'ai-pravitelstvo-secret-key-2024-fixed')
```

**Изменение 2 (прогресс):**
```python
# Было:
tasks = db.get_tasks_by_project(project_id)

# Стало:
tasks = db.get_tasks_by_project(project_id)
tasks_dict = [task.to_dict() for task in tasks]  # Конвертация в словари

return render_template('project_detail.html', 
                     tasks=tasks_dict,  # Передаём словари
                     ...)
```

---

## 🚀 КАК ОБНОВИТЬ СЕРВЕР

### Вариант A: Автоматический (рекомендую)

```bash
ssh root@194.67.66.120

# Скачать и запустить скрипт обновления
curl -o /tmp/update-server.sh https://raw.githubusercontent.com/DenMilenium/ai-pravitelstvo/main/update-server.sh
bash /tmp/update-server.sh
```

### Вариант B: Ручной

```bash
ssh root@194.67.66.120

cd /var/www/ai-pravitelstvo
systemctl stop ai-dashboard

git pull

source dashboard/venv/bin/activate
pip install requests

# Обновить службу
nano /etc/systemd/system/ai-dashboard.service
```

**Добавить в [Service]:**
```ini
Environment="FLASK_SECRET_KEY=ai-pravitelstvo-secret-key-2024-fixed"
Environment="GITHUB_TOKEN=ghp_ВАШ_ТОКЕН"
Environment="GITHUB_REPO=DenMilenium/ai-pravitelstvo"
```

```bash
systemctl daemon-reload
systemctl start ai-dashboard
systemctl status ai-dashboard
```

---

## 🧪 ПРОВЕРКА ПОСЛЕ ОБНОВЛЕНИЯ

### Тест 1: Сессии
1. Открой `http://194.67.66.120/login`
2. Войди: `admin` / `admin123`
3. Перейди в "Проекты"
4. **Ожидается:** НЕ просит логин снова ✅
5. Перезагрузи страницу (F5)
6. **Ожидается:** Всё ещё авторизован ✅

### Тест 2: Прогресс
1. Создай новый проект
2. Посмотри на ползунок прогресса
3. **Ожидается:** Показывает "0 из N задач (0%)" ✅
4. Нажми "▶️ Выполнить" на задаче
5. Подожди 2-3 секунды
6. **Ожидается:** Статус изменился на "done", прогресс увеличился ✅

---

## 📋 ИТОГО

| Проблема | Причина | Решение | Статус |
|----------|---------|---------|--------|
| Разлогинивает | Динамический secret_key | Статический ключ | ✅ Исправлено |
| Прогресс 10% | Enum vs String | Конвертация to_dict() | ✅ Исправлено |

**Commit:** `43cbb1d` — "🐛 ИСПРАВЛЕНО: Сессии теперь сохраняются!"
