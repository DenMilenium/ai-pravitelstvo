#!/usr/bin/env python3
"""
🌐 Frontend-Agent
Агент-разработчик веб-интерфейсов

Умеет:
- Создавать React компоненты
- Генерировать CSS/Tailwind
- Собирать полноценные страницы
- Создавать адаптивный дизайн

Запуск:
    python frontend_agent.py "Создай дашборд для AI"
"""

import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class WebComponent:
    """Веб-компонент"""
    name: str
    jsx: str
    css: str
    imports: List[str]


class FrontendAgent:
    """
    🌐 Frontend-Agent
    
    Специализация: Веб-интерфейсы
    Стек: React, TypeScript, Tailwind CSS
    """
    
    NAME = "Frontend-Agent"
    ROLE = "Frontend разработчик"
    EXPERTISE = ["React", "TypeScript", "Tailwind CSS", "Vite", "Responsive Design"]
    
    def __init__(self):
        self.frameworks = ["react", "vue", "vanilla"]
        self.styling = ["tailwind", "css-modules", "styled-components"]
    
    def process_request(self, request: str, framework: str = "react") -> Dict[str, str]:
        """
        Обработка запроса и генерация кода
        
        Args:
            request: Описание компонента/страницы
            framework: react/vue/vanilla
            
        Returns:
            Словарь с файлами: {filename: content}
        """
        request_lower = request.lower()
        files = {}
        
        # Определяем тип компонента
        if "дашборд" in request_lower or "dashboard" in request_lower:
            files = self._generate_dashboard(framework)
        elif "лендинг" in request_lower or "landing" in request_lower:
            files = self._generate_landing(framework)
        elif "форма" in request_lower or "form" in request_lower:
            files = self._generate_form(framework)
        elif "чат" in request_lower or "chat" in request_lower:
            files = self._generate_chat(framework)
        elif "админ" in request_lower or "admin" in request_lower:
            files = self._generate_admin_panel(framework)
        else:
            files = self._generate_component(request, framework)
        
        return files
    
    def _generate_dashboard(self, framework: str) -> Dict[str, str]:
        """Генерация дашборда"""
        files = {}
        
        # Компонент дашборда
        files["Dashboard.jsx"] = '''import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, BarChart, Bar 
} from 'recharts';
import { 
  Activity, Users, DollarSign, TrendingUp,
  Menu, Bell, Search, User
} from 'lucide-react';

const Dashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  const stats = [
    { title: 'Всего пользователей', value: '12,345', icon: Users, change: '+12%' },
    { title: 'Выручка', value: '$45,678', icon: DollarSign, change: '+8%' },
    { title: 'Активность', value: '89%', icon: Activity, change: '+5%' },
    { title: 'Рост', value: '+23%', icon: TrendingUp, change: '+15%' },
  ];
  
  const chartData = [
    { name: 'Янв', users: 4000, revenue: 2400 },
    { name: 'Фев', users: 3000, revenue: 1398 },
    { name: 'Мар', users: 2000, revenue: 9800 },
    { name: 'Апр', users: 2780, revenue: 3908 },
    { name: 'Май', users: 1890, revenue: 4800 },
    { name: 'Июн', users: 2390, revenue: 3800 },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <Menu className="w-6 h-6" />
            </button>
            <h1 className="text-xl font-bold text-gray-800">🤖 AI Dashboard</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input 
                type="text"
                placeholder="Поиск..."
                className="pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button className="relative p-2 hover:bg-gray-100 rounded-lg">
              <Bell className="w-6 h-6" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            
            <button className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-lg">
              <User className="w-6 h-6" />
              <span className="hidden md:block">Админ</span>
            </button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        {sidebarOpen && (
          <aside className="w-64 bg-white shadow-md min-h-screen">
            <nav className="p-4">
              <ul className="space-y-2">
                {['📊 Дашборд', '👥 Пользователи', '📈 Аналитика', '⚙️ Настройки'].map((item) => (
                  <li key={item}>
                    <a 
                      href="#" 
                      className="block px-4 py-2 rounded-lg hover:bg-blue-50 hover:text-blue-600 transition-colors"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </aside>
        )}

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <div key={index} className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                    <span className="text-green-500 text-sm">{stat.change}</span>
                  </div>
                  <stat.icon className="w-8 h-8 text-blue-500" />
                </div>
              </div>
            ))}
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4">👥 Пользователи</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="users" stroke="#3B82F6" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4">💰 Выручка</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="revenue" fill="#10B981" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
'''
        
        # package.json
        files["package.json"] = '''{
  "name": "ai-dashboard",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.8"
  }
}
'''
        
        # tailwind.config.js
        files["tailwind.config.js"] = '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
'''
        
        # index.html
        files["index.html"] = '''<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
'''
        
        # main.jsx
        files["main.jsx"] = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import Dashboard from './Dashboard.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Dashboard />
  </React.StrictMode>,
)
'''
        
        # index.css
        files["index.css"] = '''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
'''
        
        return files
    
    def _generate_landing(self, framework: str) -> Dict[str, str]:
        """Генерация лендинга"""
        files = {}
        
        files["Landing.jsx"] = '''import React from 'react';
import { ArrowRight, Check, Star, Zap, Shield } from 'lucide-react';

const Landing = () => {
  const features = [
    { icon: Zap, title: 'Быстро', desc: 'Мгновенная обработка данных' },
    { icon: Shield, title: 'Безопасно', desc: 'Шифрование на уровне банков' },
    { icon: Star, title: 'Надёжно', desc: '99.9% uptime гарантия' },
  ];

  const plans = [
    { name: 'Старт', price: '0₽', features: ['1 проект', 'Базовая поддержка', '5GB хранилища'] },
    { name: 'Про', price: '999₽', features: ['10 проектов', 'Приоритетная поддержка', '100GB хранилища'] },
    { name: 'Бизнес', price: '2999₽', features: ['Безлимит', '24/7 поддержка', '1TB хранилища'] },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero */}
      <section className="bg-gradient-to-br from-blue-600 to-purple-700 text-white py-20">
        <div className="container mx-auto px-6 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            🤖 AI Правительство
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100">
            Цифровое государство будущего. Управляем искусственным интеллектом.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 px-8 py-4 rounded-full font-bold hover:bg-blue-50 transition">
              Начать бесплатно →
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-full font-bold hover:bg-white/10 transition">
              Узнать больше
            </button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Почему мы?</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-6 rounded-xl hover:shadow-lg transition">
                <feature.icon className="w-12 h-12 mx-auto mb-4 text-blue-600" />
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-gray-50 py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Тарифы</h2>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {plans.map((plan, index) => (
              <div key={index} className={`bg-white p-8 rounded-2xl shadow-sm ${
                index === 1 ? 'ring-2 ring-blue-500 scale-105' : ''
              }`}>
                <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                <p className="text-4xl font-bold mb-6">{plan.price}</p>
                
                <ul className="space-y-3 mb-8">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <Check className="w-5 h-5 text-green-500" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                
                <button className={`w-full py-3 rounded-lg font-bold transition ${
                  index === 1 
                    ? 'bg-blue-600 text-white hover:bg-blue-700' 
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                }`}>
                  Выбрать
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-4">Готовы начать?</h2>
          <p className="text-gray-600 mb-8">Присоединяйтесь к тысячам пользователей уже сегодня</p>
          
          <button className="bg-blue-600 text-white px-8 py-4 rounded-full font-bold hover:bg-blue-700 transition inline-flex items-center gap-2">
            Создать аккаунт
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </section>
    </div>
  );
};

export default Landing;
'''
        
        return files
    
    def _generate_form(self, framework: str) -> Dict[str, str]:
        """Генерация формы"""
        files = {}
        
        files["ContactForm.jsx"] = '''import React, { useState } from 'react';
import { Send, Loader } from 'lucide-react';

const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Имитация отправки
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setIsSubmitting(false);
    setIsSubmitted(true);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  if (isSubmitted) {
    return (
      <div className="max-w-md mx-auto p-8 bg-green-50 rounded-xl text-center">
        <h3 className="text-2xl font-bold text-green-800 mb-2">✅ Отправлено!</h3>
        <p className="text-green-700">Спасибо за сообщение. Мы ответим в ближайшее время.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Имя</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Ваше имя"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Сообщение</label>
        <textarea
          name="message"
          value={formData.message}
          onChange={handleChange}
          required
          rows={4}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Ваше сообщение..."
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
      >
        {isSubmitting ? (
          <>
            <Loader className="w-5 h-5 animate-spin" />
            Отправка...
          </>
        ) : (
          <>
            <Send className="w-5 h-5" />
            Отправить
          </>
        )}
      </button>
    </form>
  );
};

export default ContactForm;
'''
        
        return files
    
    def _generate_chat(self, framework: str) -> Dict[str, str]:
        """Генерация чата"""
        files = {}
        
        files["Chat.jsx"] = '''import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Smile } from 'lucide-react';

const Chat = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Привет! Чем могу помочь?', isUser: false, time: '10:00' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (!inputValue.trim()) return;

    const newMessage = {
      id: messages.length + 1,
      text: inputValue,
      isUser: true,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages([...messages, newMessage]);
    setInputValue('');

    // Имитация ответа
    setTimeout(() => {
      const reply = {
        id: messages.length + 2,
        text: 'Спасибо за сообщение! Я обрабатываю ваш запрос...',
        isUser: false,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, reply]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-white">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 flex items-center gap-3">
        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
          🤖
        </div>
        <div>
          <h3 className="font-bold">AI Ассистент</h3>
          <span className="text-sm text-blue-200">🟢 Онлайн</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs md:max-w-md px-4 py-2 rounded-2xl ${
                msg.isUser
                  ? 'bg-blue-600 text-white rounded-br-md'
                  : 'bg-white shadow-sm rounded-bl-md'
              }`}
            >
              <p>{msg.text}</p>
              <span className={`text-xs ${msg.isUser ? 'text-blue-200' : 'text-gray-400'}`}>
                {msg.time}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-white border-t">
        <div className="flex items-center gap-2">
          <button className="p-2 text-gray-400 hover:text-gray-600">
            <Paperclip className="w-5 h-5" />
          </button>
          
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Введите сообщение..."
            className="flex-1 px-4 py-2 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          
          <button className="p-2 text-gray-400 hover:text-gray-600">
            <Smile className="w-5 h-5" />
          </button>
          
          <button
            onClick={handleSend}
            disabled={!inputValue.trim()}
            className="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:opacity-50 transition"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
'''
        
        return files
    
    def _generate_admin_panel(self, framework: str) -> Dict[str, str]:
        """Генерация админ-панели"""
        return self._generate_dashboard(framework)  # Используем дашборд как основу
    
    def _generate_component(self, request: str, framework: str) -> Dict[str, str]:
        """Генерация произвольного компонента"""
        files = {}
        component_name = request.replace(" ", "") + "Component"
        
        files[f"{component_name}.jsx"] = f'''import React from 'react';

const {component_name} = () => {{
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">{request}</h2>
      <p className="text-gray-600">Компонент создан Frontend-Agent</p>
    </div>
  );
}};

export default {component_name};
'''
        return files


def main():
    parser = argparse.ArgumentParser(description="🌐 Frontend-Agent — Генератор веб-интерфейсов")
    parser.add_argument("request", nargs="?", help="Описание компонента")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    parser.add_argument("--framework", "-f", default="react", 
                       choices=["react", "vue", "vanilla"],
                       help="Фреймворк")
    
    args = parser.parse_args()
    
    agent = FrontendAgent()
    
    if args.request:
        print(f"🌐 {agent.NAME} создаёт: {args.request}")
        print(f"Фреймворк: {args.framework}")
        print("-" * 50)
        
        files = agent.process_request(args.request, args.framework)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
            
            print(f"\n📁 Все файлы сохранены в: {output_dir}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"🌐 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"Экспертиза: {', '.join(agent.EXPERTISE)}")
        print("\nПримеры:")
        print('  python frontend_agent.py "Создай дашборд" -o my-dashboard')
        print('  python frontend_agent.py "Лендинг для продукта"')
        print('  python frontend_agent.py "Форма обратной связи"')


if __name__ == "__main__":
    main()
