#!/usr/bin/env python3
"""
🎛️ AI Правительство - Dashboard API
Backend для управления агентами
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
# Статический secret_key (или из переменной окружения) - важно для сохранения сессий!
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'ai-pravitelstvo-secret-key-2024-fixed')
CORS(app)

# 🔌 Подключаем WebSocket (SocketIO)
try:
    from dashboard.websocket import init_socketio, socketio
    socketio = init_socketio(app)
    print("✅ WebSocket (SocketIO) подключен")
except Exception as e:
    print(f"⚠️ WebSocket не подключен: {e}")
    socketio = None

# Подключаем Orchestrator API
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from orchestrator.api import orchestrator_bp
    app.register_blueprint(orchestrator_bp)
    print("✅ Orchestrator API подключен")
except Exception as e:
    print(f"⚠️ Orchestrator API не подключен: {e}")

DATABASE = 'dashboard.db'
AGENTS_DIR = Path(__file__).parent.parent / 'agents'

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Таблица пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Таблица логов активности агентов
    c.execute('''
        CREATE TABLE IF NOT EXISTS agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            action TEXT NOT NULL,
            status TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица настроек
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Создаем дефолтного пользователя если нет
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        default_hash = generate_password_hash('admin123')
        c.execute('''
            INSERT INTO users (username, password_hash, email)
            VALUES (?, ?, ?)
        ''', ('admin', default_hash, 'admin@ai-pravitelstvo.ru'))
    
    conn.commit()
    conn.close()

# Декоратор для проверки авторизации
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Получить список всех агентов
def get_agents():
    agents = []
    if AGENTS_DIR.exists():
        for file in sorted(AGENTS_DIR.glob('*_agent.py')):
            name = file.stem.replace('_agent', '')
            agents.append({
                'id': name,
                'name': name.replace('_', ' ').title(),
                'file': file.name,
                'status': 'active',
                'last_run': None
            })
    return agents

# ============ ROUTES ============

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            
            # Обновляем last_login
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
            conn.commit()
            conn.close()
            
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Неверный логин или пароль')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/projects')
@login_required
def projects():
    """Страница управления проектами"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    return render_template('projects.html', user={'username': user[0]})

@app.route('/project/<project_id>')
@login_required
def project_detail(project_id):
    """Детальная страница проекта"""
    from orchestrator.core.database import Database
    db = Database()
    
    project = db.get_project(project_id)
    if not project:
        return "Проект не найден", 404
    
    tasks = db.get_tasks_by_project(project_id)
    # Конвертируем задачи в словари для корректного отображения статуса
    tasks_dict = [task.to_dict() for task in tasks]
    
    return render_template('project_detail.html', 
                         project=project,
                         tasks=tasks_dict,
                         user={'username': session.get('username')})

@app.route('/profile')
@login_required
def profile():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT username, email, created_at, last_login FROM users WHERE id = ?', 
              (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'success': False, 'error': 'Все поля обязательны'})
    
    if len(new_password) < 6:
        return jsonify({'success': False, 'error': 'Пароль должен быть минимум 6 символов'})
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Проверяем текущий пароль
    c.execute('SELECT password_hash FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    
    if not user or not check_password_hash(user[0], current_password):
        conn.close()
        return jsonify({'success': False, 'error': 'Текущий пароль неверный'})
    
    # Меняем пароль
    new_hash = generate_password_hash(new_password)
    c.execute('UPDATE users SET password_hash = ? WHERE id = ?', 
              (new_hash, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Пароль успешно изменён'})

# ============ API ROUTES ============

@app.route('/api/agents')
@login_required
def api_agents():
    agents = get_agents()
    return jsonify({'agents': agents, 'total': len(agents)})

@app.route('/api/agents/stats')
@login_required
def api_agents_stats():
    agents = get_agents()
    
    # Группируем по категориям
    categories = {
        'desktop': ['pyqt', 'tauri', 'electron', 'system', 'wpf', 'cocoa', 'gtk', 'winforms'],
        'web': ['frontend', 'backend', 'fullstack', 'ui', 'ux', 'nocode', 'analytics', 
                'plugin', 'graphql', 'websocket', 'pwa', 'cms'],
        'mobile': ['mobile', 'ios', 'android'],
        'cloud': ['cloud', 'aws', 'azure', 'gcp', 'serverless', 'architect'],
        'ai': ['ml', 'data'],
        'infrastructure': ['database', 'docker', 'k8s', 'redis', 'rabbitmq', 
                          'elasticsearch', 'monitoring', 'nginx', 'backup', 
                          'performance', 'securityscanner', 'apitesting', 'docsgenerator'],
        'security': ['secops', 'test'],
        'backend_fw': ['django', 'laravel'],
        'marketing': ['seo', 'ad', 'marketer', 'yandex_ads'],
        'pm': ['pm', 'agile', 'roadmap'],
        'hr': ['recruiter', 'onboarding', 'training'],
        'research': ['rnd', 'mirofish']
    }
    
    stats = {}
    for cat, keywords in categories.items():
        count = sum(1 for a in agents if any(k in a['id'].lower() for k in keywords))
        stats[cat] = count
    
    stats['other'] = len(agents) - sum(stats.values())
    stats['total'] = len(agents)
    
    return jsonify(stats)

@app.route('/api/agent/<agent_id>/run', methods=['POST'])
@login_required
def run_agent(agent_id):
    # Логируем запуск
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO agent_logs (agent_name, action, status, details)
        VALUES (?, ?, ?, ?)
    ''', (agent_id, 'run', 'started', f'Запущен пользователем {session.get("username")}'))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Агент {agent_id} запущен'})

@app.route('/api/logs')
@login_required
def api_logs():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        SELECT agent_name, action, status, details, created_at
        FROM agent_logs
        ORDER BY created_at DESC
        LIMIT 50
    ''')
    logs = c.fetchall()
    conn.close()
    
    return jsonify([{
        'agent': l[0],
        'action': l[1],
        'status': l[2],
        'details': l[3],
        'time': l[4]
    } for l in logs])

@app.route('/agent/<agent_type>')
@login_required
def agent_chat(agent_type):
    """Страница чата с агентом"""
    
    # Информация об агентах
    agents_info = {
        'frontend': {
            'name': 'Frontend Agent',
            'role': 'Frontend Developer',
            'icon': '🎨',
            'description': 'Создаёт HTML, CSS, JavaScript код'
        },
        'backend': {
            'name': 'Backend Agent',
            'role': 'Backend Developer',
            'icon': '⚙️',
            'description': 'Создаёт серверный код, API'
        },
        'devops': {
            'name': 'DevOps Agent',
            'role': 'DevOps Engineer',
            'icon': '🚀',
            'description': 'Настраивает Docker, CI/CD'
        },
        'content': {
            'name': 'Content Agent',
            'role': 'Content Manager',
            'icon': '📝',
            'description': 'Создаёт документацию'
        },
        'design': {
            'name': 'Design Agent',
            'role': 'UI/UX Designer',
            'icon': '✨',
            'description': 'Создаёт дизайн и макеты'
        }
    }
    
    info = agents_info.get(agent_type, {
        'name': f'{agent_type.title()} Agent',
        'role': 'AI Agent',
        'icon': '🤖',
        'description': 'AI агент'
    })
    
    return render_template('agent_chat.html',
        agent_type=agent_type,
        agent_name=info['name'],
        agent_role=info['role'],
        agent_icon=info['icon'],
        agent_description=info['description'],
        current_time=datetime.now().strftime('%H:%M'),
        github_repo='DenMilenium/ai-pravitelstvo'
    )


@app.route('/api/user')
@login_required
def api_user():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT username, email, created_at, last_login FROM users WHERE id = ?',
              (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    return jsonify({
        'username': user[0],
        'email': user[1],
        'created_at': user[2],
        'last_login': user[3]
    })


# ========== Agents Management ==========

@app.route('/agents')
@login_required
def agents_management():
    """Страница управления агентами"""
    
    # Загружаем всех агентов
    agents = load_all_agents()
    
    # Группируем по министерствам
    agents_by_ministry = {}
    for agent in agents:
        ministry = agent.get('ministry', 'other')
        if ministry not in agents_by_ministry:
            agents_by_ministry[ministry] = []
        agents_by_ministry[ministry].append(agent)
    
    # Иконки министерств
    ministry_icons = {
        'frontend': '🎨',
        'backend': '⚙️',
        'mobile': '📱',
        'desktop': '💻',
        'devops': '🚀',
        'cloud': '☁️',
        'ai': '🧠',
        'security': '🔒',
        'marketing': '📈',
        'other': '🤖'
    }
    
    # Названия министерств
    ministry_names = {
        'frontend': 'Frontend разработка',
        'backend': 'Backend разработка',
        'mobile': 'Мобильная разработка',
        'desktop': 'Desktop приложения',
        'devops': 'DevOps',
        'cloud': 'Облачные технологии',
        'ai': 'AI / Machine Learning',
        'security': 'Безопасность',
        'marketing': 'Маркетинг',
        'other': 'Другие агенты'
    }
    
    # Считаем общую статистику
    total_tasks_completed = sum(a.get('tasks_completed', 0) for a in agents)
    
    return render_template('agents_management.html',
                         agents=agents,
                         agents_by_ministry=agents_by_ministry,
                         ministry_icons=ministry_icons,
                         ministry_names=ministry_names,
                         total_tasks_completed=total_tasks_completed,
                         user={'username': session.get('username')})


def load_all_agents():
    """Загружает информацию обо всех агентах"""
    agents = []
    
    # Сканируем директорию агентов
    if AGENTS_DIR.exists():
        for file in sorted(AGENTS_DIR.glob('*_agent.py')):
            agent_id = file.stem.replace('_agent', '')
            
            # Пытаемся загрузить метаданные агента
            try:
                # Заглушка - в реальности парсим файл или берем из БД
                agent_info = get_agent_info(agent_id)
                agents.append(agent_info)
            except Exception as e:
                # Если не удалось загрузить - базовая информация
                agents.append({
                    'id': agent_id,
                    'name': agent_id.replace('_', ' ').title() + ' Agent',
                    'role': 'AI Agent',
                    'emoji': '🤖',
                    'ministry': 'other',
                    'status': 'idle',
                    'enabled': True,
                    'tasks_completed': 0,
                    'success_rate': 100,
                    'avg_time': 0,
                    'expertise': ['AI', 'Automation']
                })
    
    return agents


def get_agent_info(agent_id):
    """Получает информацию об агенте из БД или файла"""
    # Заглушка - возвращаем моковые данные
    # В реальности здесь парсинг файла агента или запрос к БД
    
    ministries_map = {
        'frontend': 'frontend',
        'react': 'frontend',
        'vue': 'frontend',
        'angular': 'frontend',
        'backend': 'backend',
        'django': 'backend',
        'laravel': 'backend',
        'node': 'backend',
        'mobile': 'mobile',
        'ios': 'mobile',
        'android': 'mobile',
        'flutter': 'mobile',
        'desktop': 'desktop',
        'pyqt': 'desktop',
        'electron': 'desktop',
        'devops': 'devops',
        'docker': 'devops',
        'k8s': 'devops',
        'cloud': 'cloud',
        'aws': 'cloud',
        'azure': 'cloud',
        'ml': 'ai',
        'ai': 'ai',
        'security': 'security',
        'seo': 'marketing',
        'marketer': 'marketing',
    }
    
    ministry = ministries_map.get(agent_id, 'other')
    
    # Иконки по министерствам
    emojis = {
        'frontend': '🎨', 'backend': '⚙️', 'mobile': '📱',
        'desktop': '💻', 'devops': '🚀', 'cloud': '☁️',
        'ai': '🧠', 'security': '🔒', 'marketing': '📈',
        'other': '🤖'
    }
    
    return {
        'id': agent_id,
        'name': agent_id.replace('_', ' ').title() + ' Agent',
        'role': agent_id.replace('_', ' ').title() + ' Developer',
        'emoji': emojis.get(ministry, '🤖'),
        'ministry': ministry,
        'status': 'idle',
        'enabled': True,
        'tasks_completed': 0,
        'success_rate': 100,
        'avg_time': 5,
        'expertise': [agent_id.replace('_', ' ').title(), 'AI', 'Automation']
    }


@app.route('/api/agents')
@login_required
def api_agents_list():
    """API: Список всех агентов"""
    agents = load_all_agents()
    return jsonify({
        'agents': agents,
        'count': len(agents)
    })


@app.route('/api/agents/<agent_id>/toggle', methods=['POST'])
@login_required
def api_agent_toggle(agent_id):
    """API: Включить/выключить агента"""
    data = request.get_json() or {}
    enabled = data.get('enabled', True)
    
    # TODO: Сохранить в БД
    # Сейчас просто логируем
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO agent_logs (agent_name, action, status, details)
        VALUES (?, ?, ?, ?)
    ''', (agent_id, 'toggle', 'success', f'Enabled: {enabled}'))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'enabled': enabled,
        'message': f'Агент {agent_id} {"включен" if enabled else "выключен"}'
    })


@app.route('/api/agents/<agent_id>/test', methods=['POST'])
@login_required
def api_agent_test(agent_id):
    """API: Тестировать агента"""
    # TODO: Запустить тестовую задачу
    return jsonify({
        'success': True,
        'agent_id': agent_id,
        'message': f'Тест агента {agent_id} запущен'
    })


# 📋 Каталог всех 106 агентов с описаниями
AGENTS_CATALOG = [
    # Frontend Core
    {'name': 'React Agent', 'emoji': '⚛️', 'type': 'react', 'category': 'frontend', 'description': 'Создает React приложения: Dashboard, Form, Landing, App', 'tags': ['frontend', 'javascript', 'jsx']},
    {'name': 'Vue Agent', 'emoji': '⚡', 'type': 'vue', 'category': 'frontend', 'description': 'Создает Vue 3 приложения с Composition API', 'tags': ['frontend', 'javascript', 'vue']},
    {'name': 'Angular Agent', 'emoji': '🅰️', 'type': 'angular', 'category': 'frontend', 'description': 'Создает Angular приложения с TypeScript', 'tags': ['frontend', 'typescript', 'google']},
    {'name': 'Svelte Agent', 'emoji': '🟥', 'type': 'svelte', 'category': 'frontend', 'description': 'Создает Svelte приложения', 'tags': ['frontend', 'javascript', 'compiler']},
    {'name': 'Next.js Agent', 'emoji': '▲', 'type': 'nextjs', 'category': 'frontend', 'description': 'Full-stack React фреймворк с SSR', 'tags': ['frontend', 'react', 'ssr']},
    {'name': 'Nuxt Agent', 'emoji': '⛰️', 'type': 'nuxt', 'category': 'frontend', 'description': 'Vue фреймворк с SSR', 'tags': ['frontend', 'vue', 'ssr']},
    {'name': 'Remix Agent', 'emoji': '🎸', 'type': 'remix', 'category': 'frontend', 'description': 'Full-stack React фреймворк', 'tags': ['frontend', 'react', 'fullstack']},
    
    # Backend
    {'name': 'Django Agent', 'emoji': '🐍', 'type': 'django', 'category': 'backend', 'description': 'Создает Django/DRF бэкенд', 'tags': ['backend', 'python', 'api']},
    {'name': 'FastAPI Agent', 'emoji': '🔥', 'type': 'fastapi', 'category': 'backend', 'description': 'Современный async Python API', 'tags': ['backend', 'python', 'async']},
    {'name': 'Node.js Agent', 'emoji': '🟢', 'type': 'nodejs', 'category': 'backend', 'description': 'Express/NestJS приложения', 'tags': ['backend', 'javascript', 'api']},
    {'name': 'Go Agent', 'emoji': '🐹', 'type': 'go', 'category': 'backend', 'description': 'Go/Gin бэкенд с высокой производительностью', 'tags': ['backend', 'golang', 'fast']},
    {'name': 'Ruby Agent', 'emoji': '💎', 'type': 'ruby', 'category': 'backend', 'description': 'Ruby on Rails приложения', 'tags': ['backend', 'ruby', 'mvc']},
    {'name': 'Laravel Agent', 'emoji': '🐘', 'type': 'laravel', 'category': 'backend', 'description': 'PHP Laravel приложения', 'tags': ['backend', 'php', 'mvc']},
    {'name': 'Java Agent', 'emoji': '☕', 'type': 'java', 'category': 'backend', 'description': 'Spring Boot приложения', 'tags': ['backend', 'java', 'enterprise']},
    {'name': 'C# Agent', 'emoji': '#️⃣', 'type': 'csharp', 'category': 'backend', 'description': '.NET Core приложения', 'tags': ['backend', 'dotnet', 'microsoft']},
    {'name': 'Rust Agent', 'emoji': '🦀', 'type': 'rust', 'category': 'backend', 'description': 'Actix-web приложения на Rust', 'tags': ['backend', 'rust', 'fast']},
    
    # Mobile
    {'name': 'Flutter Agent', 'emoji': '📱', 'type': 'flutter', 'category': 'mobile', 'description': 'Кросс-платформенные мобильные приложения', 'tags': ['mobile', 'dart', 'cross-platform']},
    {'name': 'iOS Agent', 'emoji': '🍎', 'type': 'ios', 'category': 'mobile', 'description': 'Swift/SwiftUI приложения для iOS', 'tags': ['mobile', 'swift', 'apple']},
    {'name': 'Android Agent', 'emoji': '🤖', 'type': 'android', 'category': 'mobile', 'description': 'Kotlin/Jetpack Compose приложения', 'tags': ['mobile', 'kotlin', 'google']},
    {'name': 'React Native Agent', 'emoji': '⚛️', 'type': 'react-native', 'category': 'mobile', 'description': 'React для мобильных устройств', 'tags': ['mobile', 'react', 'cross-platform']},
    {'name': 'PWA Agent', 'emoji': '📱', 'type': 'pwa', 'category': 'mobile', 'description': 'Progressive Web Apps', 'tags': ['mobile', 'web', 'offline']},
    
    # Cloud & DevOps
    {'name': 'AWS Agent', 'emoji': '☁️', 'type': 'aws', 'category': 'cloud', 'description': 'Terraform конфигурация для AWS', 'tags': ['cloud', 'aws', 'iac']},
    {'name': 'Azure Agent', 'emoji': '🔷', 'type': 'azure', 'category': 'cloud', 'description': 'Terraform для Microsoft Azure', 'tags': ['cloud', 'azure', 'microsoft']},
    {'name': 'GCP Agent', 'emoji': '🔵', 'type': 'gcp', 'category': 'cloud', 'description': 'Google Cloud Platform конфигурация', 'tags': ['cloud', 'gcp', 'google']},
    {'name': 'Docker Agent', 'emoji': '🐳', 'type': 'docker', 'category': 'cloud', 'description': 'Dockerfile и docker-compose', 'tags': ['devops', 'containers', 'docker']},
    {'name': 'Kubernetes Agent', 'emoji': '☸️', 'type': 'kubernetes', 'category': 'cloud', 'description': 'K8s манифесты и Helm чарты', 'tags': ['devops', 'k8s', 'orchestration']},
    {'name': 'Terraform Agent', 'emoji': '🏗️', 'type': 'terraform', 'category': 'cloud', 'description': 'Infrastructure as Code', 'tags': ['devops', 'iac', 'hashicorp']},
    {'name': 'GitHub Actions Agent', 'emoji': '🔄', 'type': 'github-actions', 'category': 'cloud', 'description': 'CI/CD пайплайны для GitHub', 'tags': ['devops', 'ci', 'github']},
    {'name': 'GitLab CI Agent', 'emoji': '🦊', 'type': 'gitlab-ci', 'category': 'cloud', 'description': 'GitLab CI/CD конфигурация', 'tags': ['devops', 'ci', 'gitlab']},
    {'name': 'Jenkins Agent', 'emoji': '🏗️', 'type': 'jenkins', 'category': 'cloud', 'description': 'Jenkins pipelines', 'tags': ['devops', 'ci', 'jenkins']},
    {'name': 'Nginx Agent', 'emoji': '🌐', 'type': 'nginx', 'category': 'cloud', 'description': 'Nginx конфигурация', 'tags': ['devops', 'webserver', 'proxy']},
    {'name': 'Apache Agent', 'emoji': '🪶', 'type': 'apache', 'category': 'cloud', 'description': 'Apache HTTP Server конфигурация', 'tags': ['devops', 'webserver', 'httpd']},
    {'name': 'CDN Agent', 'emoji': '🌎', 'type': 'cdn', 'category': 'cloud', 'description': 'Cloudflare/AWS CloudFront конфигурация', 'tags': ['cloud', 'cdn', 'performance']},
    {'name': 'SSL Agent', 'emoji': '🔐', 'type': 'ssl', 'category': 'cloud', 'description': 'SSL/TLS и HTTPS настройки', 'tags': ['security', 'ssl', 'https']},
    
    # Database
    {'name': 'PostgreSQL Agent', 'emoji': '🐘', 'type': 'postgres', 'category': 'database', 'description': 'PostgreSQL схемы и миграции', 'tags': ['database', 'sql', 'postgres']},
    {'name': 'MongoDB Agent', 'emoji': '🍃', 'type': 'mongodb', 'category': 'database', 'description': 'NoSQL схемы для MongoDB', 'tags': ['database', 'nosql', 'mongo']},
    {'name': 'Redis Agent', 'emoji': '🔴', 'type': 'redis', 'category': 'database', 'description': 'Redis конфигурация и кеширование', 'tags': ['database', 'cache', 'redis']},
    {'name': 'MySQL Agent', 'emoji': '🐬', 'type': 'mysql', 'category': 'database', 'description': 'MySQL схемы и запросы', 'tags': ['database', 'sql', 'mysql']},
    {'name': 'Elasticsearch Agent', 'emoji': '🔍', 'type': 'elasticsearch', 'category': 'database', 'description': 'Поиск и аналитика', 'tags': ['database', 'search', 'elastic']},
    {'name': 'Database Agent', 'emoji': '🗄️', 'type': 'database', 'category': 'database', 'description': 'Универсальная работа с БД', 'tags': ['database', 'sql', 'schema']},
    {'name': 'GraphQL Agent', 'emoji': '🌐', 'type': 'graphql', 'category': 'database', 'description': 'GraphQL схемы и resolvers', 'tags': ['api', 'graphql', 'schema']},
    {'name': 'Kafka Agent', 'emoji': '📨', 'type': 'kafka', 'category': 'database', 'description': 'Apache Kafka streams', 'tags': ['streaming', 'kafka', 'events']},
    {'name': 'RabbitMQ Agent', 'emoji': '🐇', 'type': 'rabbitmq', 'category': 'database', 'description': 'Message queue конфигурация', 'tags': ['queue', 'messaging', 'amqp']},
    
    # Monitoring
    {'name': 'Prometheus Agent', 'emoji': '📈', 'type': 'prometheus', 'category': 'testing', 'description': 'Метрики и мониторинг', 'tags': ['monitoring', 'metrics', 'observability']},
    {'name': 'Grafana Agent', 'emoji': '📊', 'type': 'grafana', 'category': 'testing', 'description': 'Dashboard для метрик', 'tags': ['monitoring', 'dashboard', 'visualization']},
    {'name': 'Sentry Agent', 'emoji': '🐛', 'type': 'sentry', 'category': 'testing', 'description': 'Error tracking', 'tags': ['monitoring', 'errors', 'tracking']},
    {'name': 'LogRocket Agent', 'emoji': '🚀', 'type': 'logrocket', 'category': 'testing', 'description': 'Session replay', 'tags': ['monitoring', 'replay', 'analytics']},
    {'name': 'Analytics Agent', 'emoji': '📊', 'type': 'analytics', 'category': 'testing', 'description': 'Tracking и аналитика', 'tags': ['analytics', 'metrics', 'tracking']},
    
    # Testing
    {'name': 'Testing Agent', 'emoji': '🧪', 'type': 'testing', 'category': 'testing', 'description': 'Unit и integration тесты', 'tags': ['testing', 'qa', 'automation']},
    {'name': 'Jest Agent', 'emoji': '🧪', 'type': 'jest', 'category': 'testing', 'description': 'JavaScript тестирование', 'tags': ['testing', 'javascript', 'unit']},
    {'name': 'Cypress Agent', 'emoji': '🌲', 'type': 'cypress', 'category': 'testing', 'description': 'E2E тестирование', 'tags': ['testing', 'e2e', 'browser']},
    {'name': 'Playwright Agent', 'emoji': '🎭', 'type': 'playwright', 'category': 'testing', 'description': 'Cross-browser тестирование', 'tags': ['testing', 'e2e', 'microsoft']},
    {'name': 'Chromatic Agent', 'emoji': '🎨', 'type': 'chromatic', 'category': 'testing', 'description': 'Visual regression testing', 'tags': ['testing', 'visual', 'storybook']},
    
    # CMS
    {'name': 'WordPress Agent', 'emoji': '📝', 'type': 'wordpress', 'category': 'frontend', 'description': 'WordPress темы и плагины', 'tags': ['cms', 'php', 'wordpress']},
    {'name': 'Shopify Agent', 'emoji': '🛍️', 'type': 'shopify', 'category': 'frontend', 'description': 'Shopify темы и Liquid', 'tags': ['cms', 'ecommerce', 'shopify']},
    {'name': 'Gatsby Agent', 'emoji': '⚡', 'type': 'gatsby', 'category': 'frontend', 'description': 'Static site generator', 'tags': ['ssg', 'react', 'static']},
    {'name': 'Hugo Agent', 'emoji': '🤗', 'type': 'hugo', 'category': 'frontend', 'description': 'Go-based static generator', 'tags': ['ssg', 'go', 'static']},
    {'name': 'Jekyll Agent', 'emoji': '💎', 'type': 'jekyll', 'category': 'frontend', 'description': 'Ruby static generator', 'tags': ['ssg', 'ruby', 'github']},
    {'name': 'Astro Agent', 'emoji': '🚀', 'type': 'astro', 'category': 'frontend', 'description': 'Fast static site generator', 'tags': ['ssg', 'javascript', 'fast']},
    
    # Micro Frontend
    {'name': 'Preact Agent', 'emoji': '⚛️', 'type': 'preact', 'category': 'frontend', 'description': 'Легкий React альтернатива', 'tags': ['frontend', 'javascript', 'lightweight']},
    {'name': 'Alpine.js Agent', 'emoji': '🏔️', 'type': 'alpine', 'category': 'frontend', 'description': 'Легкий JS фреймворк', 'tags': ['frontend', 'javascript', 'lightweight']},
    {'name': 'Lit Agent', 'emoji': '🔥', 'type': 'lit', 'category': 'frontend', 'description': 'Web Components', 'tags': ['frontend', 'webcomponents', 'google']},
    {'name': 'Stimulus Agent', 'emoji': '🎮', 'type': 'stimulus', 'category': 'frontend', 'description': 'Hotwire Stimulus', 'tags': ['frontend', 'ruby', 'hotwire']},
    {'name': 'Solid Agent', 'emoji': '💠', 'type': 'solid', 'category': 'frontend', 'description': 'Реактивный фреймворк', 'tags': ['frontend', 'javascript', 'reactive']},
    {'name': 'Qwik Agent', 'emoji': '⚡', 'type': 'qwik', 'category': 'frontend', 'description': 'Resumable фреймворк', 'tags': ['frontend', 'javascript', 'fast']},
    {'name': 'Electron Agent', 'emoji': '🪟', 'type': 'electron', 'category': 'frontend', 'description': 'Desktop приложения', 'tags': ['desktop', 'javascript', 'cross-platform']},
    
    # Config & Utils
    {'name': 'Swagger Agent', 'emoji': '📋', 'type': 'swagger', 'category': 'utility', 'description': 'OpenAPI спецификации', 'tags': ['api', 'docs', 'openapi']},
    {'name': 'Postman Agent', 'emoji': '📮', 'type': 'postman', 'category': 'utility', 'description': 'API коллекции', 'tags': ['api', 'testing', 'collections']},
    {'name': 'Storybook Agent', 'emoji': '📖', 'type': 'storybook', 'category': 'utility', 'description': 'UI компоненты документация', 'tags': ['frontend', 'docs', 'ui']},
    {'name': 'ESLint Agent', 'emoji': '🔍', 'type': 'eslint', 'category': 'utility', 'description': 'JavaScript линтинг', 'tags': ['tooling', 'javascript', 'quality']},
    {'name': 'Prettier Agent', 'emoji': '✨', 'type': 'prettier', 'category': 'utility', 'description': 'Код форматирование', 'tags': ['tooling', 'formatting', 'quality']},
    {'name': 'TypeScript Agent', 'emoji': '🔷', 'type': 'tsconfig', 'category': 'utility', 'description': 'TS конфигурация', 'tags': ['tooling', 'typescript', 'config']},
    {'name': 'Webpack Agent', 'emoji': '📦', 'type': 'webpack', 'category': 'utility', 'description': 'Module bundler', 'tags': ['tooling', 'javascript', 'build']},
    {'name': 'Vite Agent', 'emoji': '⚡', 'type': 'vite', 'category': 'utility', 'description': 'Fast build tool', 'tags': ['tooling', 'javascript', 'fast']},
    {'name': 'Rollup Agent', 'emoji': '📦', 'type': 'rollup', 'category': 'utility', 'description': 'JS module bundler', 'tags': ['tooling', 'javascript', 'build']},
    {'name': 'Parcel Agent', 'emoji': '📦', 'type': 'parcel', 'category': 'utility', 'description': 'Zero-config bundler', 'tags': ['tooling', 'javascript', 'build']},
    {'name': 'Makefile Agent', 'emoji': '🛠️', 'type': 'makefile', 'category': 'utility', 'description': 'Build automation', 'tags': ['tooling', 'automation', 'build']},
    {'name': 'Bash Agent', 'emoji': '🐚', 'type': 'bash', 'category': 'utility', 'description': 'Shell скрипты', 'tags': ['scripting', 'shell', 'automation']},
    {'name': 'PowerShell Agent', 'emoji': '💻', 'type': 'powershell', 'category': 'utility', 'description': 'Windows scripting', 'tags': ['scripting', 'windows', 'automation']},
    {'name': 'Cron Agent', 'emoji': '⏰', 'type': 'cron', 'category': 'utility', 'description': 'Scheduled tasks', 'tags': ['scheduling', 'automation', 'linux']},
    {'name': 'Webhook Agent', 'emoji': '🎣', 'type': 'webhook', 'category': 'utility', 'description': 'Webhook handlers', 'tags': ['api', 'integration', 'events']},
    
    # Special
    {'name': 'AI/ML Agent', 'emoji': '🧠', 'type': 'ai', 'category': 'special', 'description': 'Machine learning модели', 'tags': ['ai', 'ml', 'python']},
    {'name': 'Chatbot Agent', 'emoji': '💬', 'type': 'chatbot', 'category': 'special', 'description': 'Создание чат-ботов', 'tags': ['ai', 'nlp', 'bot']},
    {'name': 'GameDev Agent', 'emoji': '🎮', 'type': 'gamedev', 'category': 'special', 'description': 'Game development', 'tags': ['gaming', 'canvas', 'interactive']},
    {'name': 'SEO Agent', 'emoji': '🔍', 'type': 'seo', 'category': 'special', 'description': 'SEO оптимизация', 'tags': ['marketing', 'seo', 'search']},
    {'name': 'Content Agent', 'emoji': '📝', 'type': 'content', 'category': 'special', 'description': 'Генерация контента', 'tags': ['content', 'marketing', 'text']},
    {'name': 'Documentation Agent', 'emoji': '📚', 'type': 'documentation', 'category': 'special', 'description': 'Документация и README', 'tags': ['docs', 'markdown', 'wiki']},
    {'name': 'Security Agent', 'emoji': '🔒', 'type': 'security', 'category': 'special', 'description': 'Security audit и fixes', 'tags': ['security', 'audit', 'protection']},
    {'name': 'Performance Agent', 'emoji': '⚡', 'type': 'performance', 'category': 'special', 'description': 'Performance optimization', 'tags': ['optimization', 'speed', 'metrics']},
    {'name': 'Accessibility Agent', 'emoji': '♿', 'type': 'accessibility', 'category': 'special', 'description': 'a11y compliance', 'tags': ['accessibility', 'a11y', 'inclusive']},
    {'name': 'Localization Agent', 'emoji': '🌍', 'type': 'localization', 'category': 'special', 'description': 'i18n и переводы', 'tags': ['i18n', 'l10n', 'translation']},
    {'name': 'Email Agent', 'emoji': '📧', 'type': 'email', 'category': 'special', 'description': 'Email сервисы', 'tags': ['email', 'smtp', 'notifications']},
    {'name': 'Notification Agent', 'emoji': '🔔', 'type': 'notifications', 'category': 'special', 'description': 'Push notifications', 'tags': ['notifications', 'push', 'mobile']},
    {'name': 'Backup Agent', 'emoji': '💾', 'type': 'backup', 'category': 'special', 'description': 'Backup стратегии', 'tags': ['backup', 'recovery', 'data']},
    {'name': 'Migration Agent', 'emoji': '🚚', 'type': 'migration', 'category': 'special', 'description': 'Data migrations', 'tags': ['migration', 'database', 'transfer']},
    {'name': 'Web3 Agent', 'emoji': '⛓️', 'type': 'web3', 'category': 'special', 'description': 'Blockchain и smart contracts', 'tags': ['blockchain', 'ethereum', 'solidity']},
    {'name': 'IoT Agent', 'emoji': '📡', 'type': 'iot', 'category': 'special', 'description': 'IoT и embedded', 'tags': ['iot', 'embedded', 'arduino']},
    {'name': 'AR/VR Agent', 'emoji': '🥽', 'type': 'arvr', 'category': 'special', 'description': 'Augmented/Virtual reality', 'tags': ['ar', 'vr', '3d']},
    {'name': 'Voice Agent', 'emoji': '🎤', 'type': 'voice', 'category': 'special', 'description': 'Voice interfaces', 'tags': ['voice', 'alexa', 'assistant']},
    {'name': 'PDF Agent', 'emoji': '📄', 'type': 'pdf', 'category': 'special', 'description': 'PDF генерация', 'tags': ['pdf', 'documents', 'reports']},
    {'name': 'Spreadsheet Agent', 'emoji': '📊', 'type': 'spreadsheet', 'category': 'special', 'description': 'Excel/CSV обработка', 'tags': ['excel', 'csv', 'data']},
    {'name': 'QR Code Agent', 'emoji': '🔲', 'type': 'qrcode', 'category': 'special', 'description': 'QR код генерация', 'tags': ['qr', 'barcode', 'scanning']},
    {'name': 'Image Processing Agent', 'emoji': '🖼️', 'type': 'image-processing', 'category': 'special', 'description': 'Обработка изображений', 'tags': ['images', 'processing', 'graphics']},
    {'name': 'Video Agent', 'emoji': '🎬', 'type': 'video', 'category': 'special', 'description': 'Видео обработка', 'tags': ['video', 'ffmpeg', 'media']},
    {'name': 'Audio Agent', 'emoji': '🎵', 'type': 'audio', 'category': 'special', 'description': 'Аудио обработка', 'tags': ['audio', 'sound', 'media']},
    {'name': 'Web Scraping Agent', 'emoji': '🕷️', 'type': 'scraping', 'category': 'special', 'description': 'Web scraping', 'tags': ['scraping', 'crawler', 'data']},
]

@app.route('/agents')
@login_required
def agents_catalog():
    """Каталог всех агентов"""
    categories = list(set(a['category'] for a in AGENTS_CATALOG))
    return render_template('agents_catalog.html', 
                          agents=AGENTS_CATALOG, 
                          categories=categories)


@app.route('/api/agents/catalog')
@login_required
def api_agents_catalog():
    """API: Полный каталог агентов"""
    return jsonify({
        'agents': AGENTS_CATALOG,
        'count': len(AGENTS_CATALOG),
        'categories': list(set(a['category'] for a in AGENTS_CATALOG))
    })
@login_required
def api_agents_start_all():
    """API: Запустить всех агентов"""
    agents = load_all_agents()
    started = 0
    
    for agent in agents:
        if not agent.get('enabled'):
            # Включаем
            started += 1
    
    return jsonify({
        'success': True,
        'started': started,
        'message': f'Запущено {started} агентов'
    })


@app.route('/api/agents/stop-all', methods=['POST'])
@login_required
def api_agents_stop_all():
    """API: Остановить всех агентов"""
    agents = load_all_agents()
    stopped = len(agents)
    
    return jsonify({
        'success': True,
        'stopped': stopped,
        'message': f'Остановлено {stopped} агентов'
    })


if __name__ == '__main__':
    init_db()
    print("🎛️ Dashboard API запущен!")
    print("URL: http://localhost:5000")
    print("Логин: admin / admin123")
    
    # Запускаем с WebSocket если доступен
    if socketio:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
