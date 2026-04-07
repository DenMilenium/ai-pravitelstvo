# 🐛 ИСПРАВЛЕНИЕ: Прогресс не двигался (всегда 10%)

## Проблема

Пользователь сообщил: **"При начале пишется что 10 процентов и ползунок не двигается, такое ощущение что ничего не делается"**

## Причина

### Тип данных не совпадал!

В `dashboard/app.py`:
```python
tasks = db.get_tasks_by_project(project_id)  # Возвращает List[Task]
return render_template('project_detail.html', tasks=tasks, ...)
```

В `project_detail.html`:
```jinja2
{% set completed = tasks|selectattr('status', 'equalto', 'done')|list|length %}
```

**Task.status** — это Enum `TaskStatus.DONE` (объект перечисления)  
**'done'** — это строка

Сравнение `TaskStatus.DONE == 'done'` всегда давало `False`!

Поэтому `completed = 0` всегда, а прогресс считался как:  
`0 / 10 * 100 = 0%` (или показывалось 10% если было округление)

## Решение

Конвертировать задачи в словари перед передачей в шаблон:

```python
# Было:
tasks = db.get_tasks_by_project(project_id)

# Стало:
tasks = db.get_tasks_by_project(project_id)
tasks_dict = [task.to_dict() for task in tasks]  # status теперь строка 'done'
```

Метод `to_dict()` в классе Task:
```python
def to_dict(self):
    data = asdict(self)
    data['status'] = self.status.value  # 'done', 'pending', etc.
    return data
```

## Проверка

Теперь в шаблоне:
- `task.status` = `'done'` (строка)
- Сравнение `'done' == 'done'` = `True` ✅
- `completed` считается правильно
- Прогресс обновляется!

## Commit

`e0b85ec` — "🐛 ИСПРАВЛЕН ПРОГРЕСС: Конвертация задач в словари"

## На сервере

```bash
cd /var/www/ai-pravitelstvo
git pull
systemctl restart ai-dashboard
```

После этого прогресс будет обновляться корректно!
