"""
🟢 Node.js Agent
Создаёт Express.js API и серверы
"""

from orchestrator.core.task_executor import BaseAgentExecutor
from orchestrator.core.database import Task
from typing import Dict


class NodeJSAgentExecutor(BaseAgentExecutor):
    """
    🟢 Node.js/Express Developer Agent
    
    Генерирует:
    - Express.js API
    - REST endpoints
    - Middleware
    - MongoDB/Mongoose models
    """
    
    AGENT_TYPE = 'nodejs'
    NAME = 'Node.js Agent'
    EMOJI = '🟢'
    
    def can_execute(self, task: Task) -> bool:
        return task.agent_type in ['nodejs', 'node', 'express', 'backend', 'js']
    
    def execute(self, task: Task) -> Dict:
        title = task.title.lower()
        
        if 'api' in title or 'rest' in title:
            return self._create_api(task)
        elif 'websocket' in title or 'socket' in title or 'realtime' in title:
            return self._create_websocket(task)
        else:
            return self._create_default_app(task)
    
    def _create_api(self, task: Task) -> Dict:
        server_js = '''const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Логирование
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Фейковая БД
let items = [
    { id: 1, name: 'Item 1', description: 'First item' },
    { id: 2, name: 'Item 2', description: 'Second item' }
];
let nextId = 3;

// Routes
app.get('/', (req, res) => {
    res.json({ 
        message: 'Express API is running',
        version: '1.0.0',
        endpoints: ['/api/items']
    });
});

// GET all items
app.get('/api/items', (req, res) => {
    res.json(items);
});

// GET single item
app.get('/api/items/:id', (req, res) => {
    const item = items.find(i => i.id === parseInt(req.params.id));
    if (!item) {
        return res.status(404).json({ error: 'Item not found' });
    }
    res.json(item);
});

// POST create item
app.post('/api/items', (req, res) => {
    const { name, description } = req.body;
    
    if (!name) {
        return res.status(400).json({ error: 'Name is required' });
    }
    
    const newItem = {
        id: nextId++,
        name,
        description: description || '',
        createdAt: new Date().toISOString()
    };
    
    items.push(newItem);
    res.status(201).json(newItem);
});

// PUT update item
app.put('/api/items/:id', (req, res) => {
    const item = items.find(i => i.id === parseInt(req.params.id));
    if (!item) {
        return res.status(404).json({ error: 'Item not found' });
    }
    
    const { name, description } = req.body;
    if (name) item.name = name;
    if (description !== undefined) item.description = description;
    item.updatedAt = new Date().toISOString();
    
    res.json(item);
});

// DELETE item
app.delete('/api/items/:id', (req, res) => {
    const index = items.findIndex(i => i.id === parseInt(req.params.id));
    if (index === -1) {
        return res.status(404).json({ error: 'Item not found' });
    }
    
    items.splice(index, 1);
    res.json({ message: 'Item deleted' });
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// 404
app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
'''

        package_json = '''{
  "name": "express-api",
  "version": "1.0.0",
  "description": "Express.js REST API",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "nodemon": "^3.0.0"
  }
}
'''

        return {
            'success': True,
            'message': f'✅ Express.js API создан!',
            'artifacts': {
                'server.js': server_js,
                'package.json': package_json,
                'README.md': '# Express API\n\nREST API на Node.js + Express'
            }
        }
    
    def _create_websocket(self, task: Task) -> Dict:
        server_js = '''const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

const PORT = process.env.PORT || 3000;

// Статические файлы
app.use(express.static('public'));

// Подключения
let connectedUsers = 0;

io.on('connection', (socket) => {
    connectedUsers++;
    console.log(`👤 User connected. Total: ${connectedUsers}`);
    
    // Отправляем приветствие
    socket.emit('message', {
        type: 'system',
        text: 'Добро пожаловать в чат!',
        time: new Date().toLocaleTimeString()
    });
    
    // Уведомляем всех о новом пользователе
    socket.broadcast.emit('message', {
        type: 'system',
        text: 'Новый пользователь присоединился',
        time: new Date().toLocaleTimeString()
    });
    
    // Обработка сообщений
    socket.on('chat message', (msg) => {
        io.emit('message', {
            type: 'user',
            text: msg,
            time: new Date().toLocaleTimeString(),
            id: socket.id
        });
    });
    
    // Отключение
    socket.on('disconnect', () => {
        connectedUsers--;
        console.log(`👤 User disconnected. Total: ${connectedUsers}`);
        io.emit('message', {
            type: 'system',
            text: 'Пользователь вышел',
            time: new Date().toLocaleTimeString()
        });
    });
});

server.listen(PORT, () => {
    console.log(`🚀 WebSocket server running on http://localhost:${PORT}`);
});
'''

        html = '''<!DOCTYPE html>
<html>
<head>
    <title>💬 WebSocket Chat</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 0 auto; padding: 20px; }
        #messages { height: 400px; border: 1px solid #ddd; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
        .message { padding: 8px; margin: 5px 0; border-radius: 5px; }
        .message.system { background: #f0f0f0; color: #666; font-style: italic; }
        .message.user { background: #e3f2fd; }
        #form { display: flex; gap: 10px; }
        #input { flex: 1; padding: 10px; }
        button { padding: 10px 20px; background: #2196f3; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>💬 WebSocket Chat</h1>
    <div id="messages"></div>
    <form id="form">
        <input id="input" placeholder="Введите сообщение..." />
        <button>Отправить</button>
    </form>
    
    <script src="/socket.io/socket.io.js"></script>
    <script>
        const socket = io();
        const form = document.getElementById('form');
        const input = document.getElementById('input');
        const messages = document.getElementById('messages');
        
        socket.on('message', (msg) => {
            const div = document.createElement('div');
            div.className = `message ${msg.type}`;
            div.innerHTML = `<strong>${msg.time}</strong>: ${msg.text}`;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        });
        
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (input.value) {
                socket.emit('chat message', input.value);
                input.value = '';
            }
        });
    </script>
</body>
</html>
'''

        package_json = '''{
  "name": "websocket-server",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "socket.io": "^4.7.0"
  }
}
'''

        return {
            'success': True,
            'message': f'✅ WebSocket сервер создан!',
            'artifacts': {
                'server.js': server_js,
                'public/index.html': html,
                'package.json': package_json
            }
        }
    
    def _create_default_app(self, task: Task) -> Dict:
        return {
            'success': True,
            'message': f'✅ Node.js приложение создано!',
            'artifacts': {
                'server.js': '''const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({ message: 'Hello from Express!' });
});

app.listen(3000, () => console.log('Server running on port 3000'));
''',
                'package.json': '{"dependencies":{"express":"^4.18.2"}}'
            }
        }
