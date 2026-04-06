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
app.secret_key = os.urandom(24)
CORS(app)

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

if __name__ == '__main__':
    init_db()
    print("🎛️ Dashboard API запущен!")
    print("URL: http://localhost:5000")
    print("Логин: admin / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)
