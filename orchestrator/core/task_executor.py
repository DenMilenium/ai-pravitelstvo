"""
⚡ Task Executor
Система выполнения задач агентами
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from orchestrator.core.database import Database, Task, TaskStatus


class BaseAgentExecutor:
    """
    Базовый класс для исполнителя задач
    """
    
    AGENT_TYPE = "base"
    
    def __init__(self, db: Database = None):
        self.db = db or Database()
        self.artifacts_dir = Path("orchestrator/projects/artifacts")
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    def can_execute(self, task: Task) -> bool:
        """Проверяет, может ли этот исполнитель выполнить задачу"""
        return task.agent_type == self.AGENT_TYPE
    
    def execute(self, task: Task) -> Dict:
        """
        Выполняет задачу и возвращает артефакты
        
        Returns:
            {
                'success': bool,
                'artifacts': {filename: content},
                'message': str
            }
        """
        raise NotImplementedError("Subclasses must implement execute()")


class FrontendAgentExecutor(BaseAgentExecutor):
    """
    🎨 Frontend-Agent Executor
    Генерирует HTML/CSS/JS код
    """
    
    AGENT_TYPE = "frontend"
    
    def execute(self, task: Task) -> Dict:
        """Генерирует frontend код"""
        
        # Анализируем ТЗ задачи
        description = task.description.lower()
        
        # Определяем тип сайта
        if 'лендинг' in description or 'landing' in description:
            return self._generate_landing(task)
        elif 'корпоративный' in description or 'сайт' in description:
            return self._generate_corporate(task)
        elif 'магазин' in description or 'shop' in description:
            return self._generate_shop(task)
        else:
            return self._generate_basic(task)
    
    def _generate_landing(self, task: Task) -> Dict:
        """Генерирует лендинг"""
        
        html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        
        /* Header */
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 0; text-align: center; }
        header h1 { font-size: 3rem; margin-bottom: 20px; }
        header p { font-size: 1.3rem; opacity: 0.9; }
        
        /* Sections */
        section { padding: 80px 0; }
        .section-title { text-align: center; font-size: 2.5rem; margin-bottom: 50px; }
        
        /* Features */
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        .feature { background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center; }
        .feature-icon { font-size: 3rem; margin-bottom: 20px; }
        .feature h3 { margin-bottom: 15px; }
        
        /* CTA */
        .cta { background: #667eea; color: white; text-align: center; }
        .btn { display: inline-block; padding: 15px 40px; background: white; color: #667eea; text-decoration: none; border-radius: 30px; font-weight: bold; margin-top: 20px; }
        
        /* Footer */
        footer { background: #333; color: white; text-align: center; padding: 30px 0; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{{ project_name }}</h1>
            <p>{{ project_description }}</p>
        </div>
    </header>

    <section id="about">
        <div class="container">
            <h2 class="section-title">О нас</h2>
            <p style="text-align: center; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
                Мы предоставляем лучшие решения для вашего бизнеса. 
                Качество, надёжность, профессионализм.
            </p>
        </div>
    </section>

    <section id="features" style="background: #f8f9fa;">
        <div class="container">
            <h2 class="section-title">Наши преимущества</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🚀</div>
                    <h3>Быстрота</h3>
                    <p>Мгновенный результат без задержек</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">💎</div>
                    <h3>Качество</h3>
                    <p>Только лучшие материалы и решения</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🛡️</div>
                    <h3>Надёжность</h3>
                    <p>Гарантия на все наши услуги</p>
                </div>
            </div>
        </div>
    </section>

    <section class="cta">
        <div class="container">
            <h2 class="section-title" style="color: white;">Готовы начать?</h2>
            <p style="font-size: 1.3rem;">Свяжитесь с нами прямо сейчас</p>
            <a href="#contact" class="btn">Связаться</a>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2024 {{ project_name }}. Все права защищены.</p>
        </div>
    </footer>
</body>
</html>'''
        
        return {
            'success': True,
            'artifacts': {
                'index.html': html,
                'README.md': f'''# {task.title}

Сгенерирован лендинг для проекта.

## Структура
- `index.html` - Главная страница

## Запуск
Откройте `index.html` в браузере.
'''
            },
            'message': '✅ Лендинг успешно сгенерирован'
        }
    
    def _generate_corporate(self, task: Task) -> Dict:
        """Генерирует корпоративный сайт"""
        return self._generate_landing(task)  # Пока тот же шаблон
    
    def _generate_shop(self, task: Task) -> Dict:
        """Генерирует интернет-магазин"""
        html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Магазин</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        header { background: #333; color: white; padding: 20px 0; }
        header h1 { text-align: center; }
        
        .products { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
        .product { background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .product-img { height: 200px; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 4rem; }
        .product-info { padding: 20px; }
        .product-title { font-size: 1.2rem; margin-bottom: 10px; }
        .product-price { font-size: 1.5rem; color: #667eea; font-weight: bold; }
        .btn { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 15px; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🛍️ Наш Магазин</h1>
        </div>
    </header>
    
    <div class="container">
        <div class="products">
            <div class="product">
                <div class="product-img">📱</div>
                <div class="product-info">
                    <h3 class="product-title">Товар 1</h3>
                    <p class="product-price">9 990 ₽</p>
                    <button class="btn">В корзину</button>
                </div>
            </div>
            <div class="product">
                <div class="product-img">💻</div>
                <div class="product-info">
                    <h3 class="product-title">Товар 2</h3>
                    <p class="product-price">49 990 ₽</p>
                    <button class="btn">В корзину</button>
                </div>
            </div>
            <div class="product">
                <div class="product-img">🎧</div>
                <div class="product-info">
                    <h3 class="product-title">Товар 3</h3>
                    <p class="product-price">4 990 ₽</p>
                    <button class="btn">В корзину</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
        
        return {
            'success': True,
            'artifacts': {
                'index.html': html,
                'README.md': '# Интернет-магазин\n\nСгенерирован шаблон магазина.\n'
            },
            'message': '✅ Интернет-магазин сгенерирован'
        }
    
    def _generate_basic(self, task: Task) -> Dict:
        """Генерирует базовый сайт"""
        return self._generate_landing(task)


class DevOpsAgentExecutor(BaseAgentExecutor):
    """
    🚀 DevOps-Agent Executor
    Генерирует Dockerfile, docker-compose, nginx конфиг
    """
    
    AGENT_TYPE = "devops"
    
    def execute(self, task: Task) -> Dict:
        """Генерирует DevOps конфигурацию"""
        
        dockerfile = '''FROM nginx:alpine

# Копируем файлы сайта
COPY . /usr/share/nginx/html

# Открываем порт
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]'''
        
        docker_compose = '''version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    restart: always'''
        
        nginx_conf = '''server {
    listen 80;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ =404;
    }
    
    # Сжатие
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
}'''
        
        github_actions = '''name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t myapp .
    
    - name: Deploy to server
      run: |
        # Добавьте команды деплоя
        echo "Deploying..."'''
        
        return {
            'success': True,
            'artifacts': {
                'Dockerfile': dockerfile,
                'docker-compose.yml': docker_compose,
                'nginx.conf': nginx_conf,
                '.github/workflows/deploy.yml': github_actions,
                'README.md': '''# DevOps Configuration

## Файлы
- `Dockerfile` - Контейнер для приложения
- `docker-compose.yml` - Оркестрация контейнеров
- `nginx.conf` - Конфигурация веб-сервера
- `.github/workflows/deploy.yml` - CI/CD pipeline

## Запуск
```bash
# Сборка и запуск
docker-compose up -d

# Или только Docker
docker build -t myapp .
docker run -p 80:80 myapp
```
'''
            },
            'message': '✅ DevOps конфигурация сгенерирована'
        }


class ContentAgentExecutor(BaseAgentExecutor):
    """
    📝 Content-Agent Executor
    Генерирует документацию
    """
    
    AGENT_TYPE = "content"
    
    def execute(self, task: Task) -> Dict:
        """Генерирует документацию"""
        
        readme = f'''# Проект

## Описание
{task.description}

## Структура проекта
```
/
├── index.html          # Главная страница
├── Dockerfile          # Конфигурация Docker
├── docker-compose.yml  # Docker Compose
├── nginx.conf          # Nginx конфигурация
└── README.md           # Документация
```

## Установка

### Требования
- Docker
- Docker Compose (опционально)

### Быстрый старт
```bash
# Клонирование
git clone <repo>
cd project

# Запуск
docker-compose up -d
```

## Развёртывание

### Docker
```bash
docker build -t myapp .
docker run -p 80:80 myapp
```

### Ручная установка
Просто откройте `index.html` в браузере.

## Лицензия
MIT

---
Сгенерировано с помощью AI Правительство 🤖🏛️
'''
        
        contributing = '''# Contributing Guide

## Как внести вклад

1. Fork репозитория
2. Создайте ветку (`git checkout -b feature/amazing`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing`)
5. Откройте Pull Request

## Code Style
- Используйте 2 пробела для отступов
- Следуйте принципам чистого кода
- Документируйте сложные участки
'''
        
        return {
            'success': True,
            'artifacts': {
                'README.md': readme,
                'CONTRIBUTING.md': contributing,
                'LICENSE': '''MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
'''
            },
            'message': '✅ Документация сгенерирована'
        }


class TaskExecutor:
    """
    🎯 Главный диспетчер задач
    Запускает соответствующего исполнителя для задачи
    """
    
    def __init__(self, db: Database = None):
        self.db = db or Database()
        self.executors = [
            FrontendAgentExecutor(self.db),
            DevOpsAgentExecutor(self.db),
            ContentAgentExecutor(self.db),
        ]
    
    def execute_task(self, task_id: str) -> Dict:
        """
        Выполняет задачу по ID
        
        Returns:
            {
                'success': bool,
                'message': str,
                'artifacts': dict
            }
        """
        # Получаем задачу
        task = self.db.get_task(task_id)
        if not task:
            return {'success': False, 'message': 'Задача не найдена'}
        
        # Находим исполнителя
        executor = None
        for ex in self.executors:
            if ex.can_execute(task):
                executor = ex
                break
        
        if not executor:
            return {'success': False, 'message': f'Нет исполнителя для типа {task.agent_type}'}
        
        # Обновляем статус
        self.db.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        
        try:
            # Выполняем
            result = executor.execute(task)
            
            if result['success']:
                # Сохраняем артефакты
                self._save_artifacts(task, result['artifacts'])
                
                # Обновляем статус
                self.db.update_task_status(
                    task_id, 
                    TaskStatus.DONE,
                    artifacts=result['artifacts']
                )
                
                # 🚀 АВТОПУШ в GitHub (если есть артефакты)
                autopush_result = None
                if result.get('artifacts'):
                    try:
                        from orchestrator.core.autopush_agent import AutoPushAgent
                        autopush = AutoPushAgent()
                        
                        # Получаем название проекта
                        project = self.db.get_project(task.project_id)
                        project_name = project.name if project else None
                        
                        autopush_result = autopush.auto_push_task(
                            task_id=task.id,
                            task_title=task.title,
                            task_description=task.description,
                            agent_type=task.agent_type,
                            artifacts=result['artifacts'],
                            project_name=project_name
                        )
                        
                    except Exception as e:
                        # Автопуш не критичен — логируем ошибку но не падаем
                        print(f"⚠️ Автопуш не удался: {e}")
                        autopush_result = {'error': str(e)}
                
                return {
                    'success': True,
                    'message': result['message'],
                    'artifacts_count': len(result['artifacts']),
                    'autopush': autopush_result
                }
            else:
                self.db.update_task_status(task_id, TaskStatus.FAILED)
                return result
                
        except Exception as e:
            self.db.update_task_status(task_id, TaskStatus.FAILED)
            return {'success': False, 'message': f'Ошибка: {str(e)}'}
    
    def _save_artifacts(self, task: Task, artifacts: Dict[str, str]):
        """Сохраняет артефакты в базу данных"""
        for filename, content in artifacts.items():
            artifact_id = str(uuid.uuid4())[:8]
            file_type = filename.split('.')[-1] if '.' in filename else 'txt'
            
            self.db.save_artifact(
                artifact_id=artifact_id,
                task_id=task.id,
                project_id=task.project_id,
                file_name=filename,
                file_path=filename,
                file_type=file_type,
                content=content
            )
    
    def execute_pending_tasks(self, agent_type: str = None) -> List[Dict]:
        """
        Выполняет все ожидающие задачи
        
        Returns:
            Список результатов
        """
        pending_tasks = self.db.get_pending_tasks(agent_type)
        results = []
        
        for task in pending_tasks:
            result = self.execute_task(task.id)
            results.append({
                'task_id': task.id,
                'task_title': task.title,
                **result
            })
        
        return results


if __name__ == "__main__":
    # Тест
    executor = TaskExecutor()
    
    # Найдём первую ожидающую задачу
    db = Database()
    tasks = db.get_pending_tasks()
    
    if tasks:
        print(f"Выполняем задачу: {tasks[0].title}")
        result = executor.execute_task(tasks[0].id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Нет ожидающих задач")
