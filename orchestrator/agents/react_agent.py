"""
⚛️ React Agent
Создаёт React приложения с компонентами, hooks, и стилями
"""

from orchestrator.core.task_executor import BaseAgentExecutor
from orchestrator.core.database import Task
from typing import Dict


class ReactAgentExecutor(BaseAgentExecutor):
    """
    ⚛️ React Developer Agent
    
    Генерирует:
    - React компоненты (функциональные, с hooks)
    - Custom hooks
    - CSS Modules / Styled Components
    - React Router конфигурацию
    - package.json с зависимостями
    """
    
    AGENT_TYPE = 'react'
    NAME = 'React Agent'
    EMOJI = '⚛️'
    
    def can_execute(self, task: Task) -> bool:
        return task.agent_type in ['react', 'frontend', 'web']
    
    def execute(self, task: Task) -> Dict:
        """Генерирует React приложение"""
        
        title = task.title.lower()
        
        # Определяем тип компонента
        if 'dashboard' in title or 'дашборд' in title:
            return self._create_dashboard(task)
        elif 'form' in title or 'форма' in title:
            return self._create_form(task)
        elif 'landing' in title or 'лендинг' in title:
            return self._create_landing(task)
        else:
            return self._create_default_app(task)
    
    def _create_dashboard(self, task: Task) -> Dict:
        """Создаёт React Dashboard"""
        
        component_code = '''import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    users: 0,
    revenue: 0,
    orders: 0,
    growth: 0
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Симуляция загрузки данных
    setTimeout(() => {
      setStats({
        users: 1234,
        revenue: 45600,
        orders: 89,
        growth: 23.5
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Загрузка данных...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>📊 Dashboard</h1>
        <div className="header-actions">
          <button className="btn btn-primary">+ Новый проект</button>
          <div className="user-avatar">👤</div>
        </div>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-info">
            <h3>Пользователи</h3>
            <p className="stat-value">{stats.users.toLocaleString()}</p>
            <span className="stat-change positive">+12% ↑</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💰</div>
          <div className="stat-info">
            <h3>Доход</h3>
            <p className="stat-value">${stats.revenue.toLocaleString()}</p>
            <span className="stat-change positive">+8% ↑</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📦</div>
          <div className="stat-info">
            <h3>Заказы</h3>
            <p className="stat-value">{stats.orders}</p>
            <span className="stat-change positive">+24% ↑</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-info">
            <h3>Рост</h3>
            <p className="stat-value">{stats.growth}%</p>
            <span className="stat-change positive">+5% ↑</span>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="content-section">
          <h2>Последние активности</h2>
          <ul className="activity-list">
            <li>🎉 Новый пользователь зарегистрировался</li>
            <li>💳 Оплата получена - $299</li>
            <li>🚀 Проект "AI App" завершён</li>
            <li>⭐ Новый отзыв 5 звёзд</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
'''

        css_code = '''.dashboard {
  min-height: 100vh;
  background: #f5f7fa;
}

.dashboard-header {
  background: white;
  padding: 20px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dashboard-header h1 {
  margin: 0;
  font-size: 28px;
  color: #1a1a2e;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-primary {
  background: #e94560;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary:hover {
  background: #d63d56;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #16213e;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  padding: 40px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #6c757d;
}

.stat-value {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
}

.stat-change {
  font-size: 13px;
  font-weight: 600;
}

.stat-change.positive {
  color: #10b981;
}

.dashboard-content {
  padding: 0 40px 40px;
}

.content-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
}

.content-section h2 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #1a1a2e;
}

.activity-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.activity-list li {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #495057;
}

.activity-list li:last-child {
  border-bottom: none;
}

.dashboard-loading {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f0f0f0;
  border-top-color: #e94560;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
'''

        package_json = '''{
  "name": "react-dashboard",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  },
  "eslintConfig": {
    "extends": ["react-app"]
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
'''

        readme = '''# React Dashboard

⚛️ React Dashboard создан с помощью AI Правительство

## Установка

```bash
npm install
npm start
```

## Структура

- `Dashboard.js` - Главный компонент дашборда
- `Dashboard.css` - Стили

## Функции

- 📊 Статистика в реальном времени
- 📈 Прогресс-бары
- 🔔 Активности
- 📱 Адаптивный дизайн
'''

        return {
            'success': True,
            'message': f'✅ React Dashboard создан!',
            'artifacts': {
                'Dashboard.js': component_code,
                'Dashboard.css': css_code,
                'package.json': package_json,
                'README.md': readme
            }
        }
    
    def _create_form(self, task: Task) -> Dict:
        """Создаёт React форму"""
        
        component_code = '''import React, { useState } from 'react';
import './Form.css';

const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Имя обязательно';
    if (!formData.email.trim()) newErrors.email = 'Email обязателен';
    else if (!/\\S+@\\S+\\.\\S+/.test(formData.email)) {
      newErrors.email = 'Неверный email';
    }
    if (!formData.message.trim()) newErrors.message = 'Сообщение обязательно';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      setSubmitted(true);
      // Здесь отправка на сервер
      console.log('Form submitted:', formData);
    }
  };

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  if (submitted) {
    return (
      <div className="form-success">
        <h2>✅ Спасибо!</h2>
        <p>Ваше сообщение отправлено.</p>
        <button onClick={() => setSubmitted(false)}>Отправить ещё</button>
      </div>
    );
  }

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
      <h2>📧 Свяжитесь с нами</h2>
      
      <div className="form-group">
        <label>Имя</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className={errors.name ? 'error' : ''}
        />
        {errors.name && <span className="error-text">{errors.name}</span>}
      </div>

      <div className="form-group">
        <label>Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className={errors.email ? 'error' : ''}
        />
        {errors.email && <span className="error-text">{errors.email}</span>}
      </div>

      <div className="form-group">
        <label>Сообщение</label>
        <textarea
          name="message"
          rows="4"
          value={formData.message}
          onChange={handleChange}
          className={errors.message ? 'error' : ''}
        />
        {errors.message && <span className="error-text">{errors.message}</span>}
      </div>

      <button type="submit" className="btn-submit">
        Отправить
      </button>
    </form>
  );
};

export default ContactForm;
'''

        css_code = '''.contact-form {
  max-width: 500px;
  margin: 40px auto;
  padding: 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.contact-form h2 {
  margin: 0 0 24px 0;
  text-align: center;
  color: #1a1a2e;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #495057;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #e94560;
}

.form-group input.error,
.form-group textarea.error {
  border-color: #ef4444;
}

.error-text {
  color: #ef4444;
  font-size: 13px;
  margin-top: 6px;
  display: block;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background: #e94560;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover {
  background: #d63d56;
}

.form-success {
  max-width: 500px;
  margin: 40px auto;
  padding: 40px;
  text-align: center;
  background: white;
  border-radius: 16px;
}

.form-success h2 {
  color: #10b981;
  margin: 0 0 16px 0;
}

.form-success button {
  margin-top: 20px;
  padding: 12px 24px;
  background: #e94560;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
'''

        return {
            'success': True,
            'message': f'✅ React форма создана!',
            'artifacts': {
                'ContactForm.js': component_code,
                'Form.css': css_code,
                'package.json': '{\n  "name": "react-form",\n  "dependencies": {\n    "react": "^18.2.0",\n    "react-dom": "^18.2.0"\n  }\n}'
            }
        }
    
    def _create_landing(self, task: Task) -> Dict:
        """Создаёт Landing Page"""
        
        html_code = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Правительство - Landing</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">🏛️ AI Правительство</div>
        <div class="nav-links">
            <a href="#features">Возможности</a>
            <a href="#about">О нас</a>
            <a href="#contact">Контакты</a>
        </div>
    </nav>

    <header class="hero">
        <div class="hero-content">
            <h1>🤖 Создавайте с AI</h1>
            <p>80+ агентов готовы реализовать ваши проекты</p>
            <div class="hero-buttons">
                <button class="btn btn-primary">Начать проект</button>
                <button class="btn btn-secondary">Узнать больше</button>
            </div>
        </div>
    </header>

    <section id="features" class="features">
        <h2>Возможности</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <h3>Frontend</h3>
                <p>React, Vue, Angular приложения</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚙️</div>
                <h3>Backend</h3>
                <p>API, микросервисы, базы данных</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3>Mobile</h3>
                <p>iOS, Android, Flutter</p>
            </div>
        </div>
    </section>

    <footer class="footer">
        <p>© 2024 AI Правительство. Все права защищены.</p>
    </footer>
</body>
</html>
'''

        css_code = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

/* Navbar */
.navbar {
    background: #16213e;
    color: white;
    padding: 1rem 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 100;
}

.nav-brand {
    font-size: 1.5rem;
    font-weight: 700;
}

.nav-links a {
    color: white;
    text-decoration: none;
    margin-left: 2rem;
    opacity: 0.8;
    transition: opacity 0.3s;
}

.nav-links a:hover {
    opacity: 1;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
    color: white;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}

.hero-content h1 {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.hero-content p {
    font-size: 1.5rem;
    opacity: 0.9;
    margin-bottom: 2rem;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.btn {
    padding: 1rem 2rem;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: transform 0.3s;
}

.btn:hover {
    transform: translateY(-2px);
}

.btn-primary {
    background: #e94560;
    color: white;
}

.btn-secondary {
    background: transparent;
    color: white;
    border: 2px solid white;
}

/* Features */
.features {
    padding: 6rem 5%;
    background: #f8f9fa;
}

.features h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.feature-card {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.feature-card h3 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.feature-card p {
    color: #6c757d;
}

/* Footer */
.footer {
    background: #16213e;
    color: white;
    text-align: center;
    padding: 2rem;
}
'''

        return {
            'success': True,
            'message': f'✅ Landing Page создан!',
            'artifacts': {
                'index.html': html_code,
                'styles.css': css_code
            }
        }
    
    def _create_default_app(self, task: Task) -> Dict:
        """Создаёт базовое React приложение"""
        
        app_code = '''import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>⚛️ React App</h1>
        <p>Создано с помощью AI Правительство</p>
        <a
          className="App-link"
          href="https://github.com/DenMilenium/ai-pravitelstvo"
          target="_blank"
          rel="noopener noreferrer"
        >
          🏛️ AI Правительство на GitHub
        </a>
      </header>
    </div>
  );
}

export default App;
'''

        css_code = '''.App {
  text-align: center;
}

.App-header {
  background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}

.App-header h1 {
  margin: 0 0 16px 0;
  font-size: 48px;
}

.App-header p {
  margin: 0 0 32px 0;
  opacity: 0.8;
}

.App-link {
  color: #e94560;
  text-decoration: none;
  padding: 12px 24px;
  border: 2px solid #e94560;
  border-radius: 8px;
  transition: all 0.3s;
}

.App-link:hover {
  background: #e94560;
  color: white;
}
'''

        return {
            'success': True,
            'message': f'✅ Базовое React приложение создано!',
            'artifacts': {
                'App.js': app_code,
                'App.css': css_code,
                'package.json': '{\n  "name": "react-app",\n  "version": "0.1.0",\n  "dependencies": {\n    "react": "^18.2.0",\n    "react-dom": "^18.2.0"\n  },\n  "scripts": {\n    "start": "react-scripts start",\n    "build": "react-scripts build"\n  }\n}'
            }
        }
