"""
🪟 Electron Agent
Создаёт десктопные приложения на Electron (JS/HTML/CSS)
"""

from orchestrator.core.task_executor import BaseAgentExecutor
from orchestrator.core.database import Task
from typing import Dict


class ElectronAgentExecutor(BaseAgentExecutor):
    """
    🪟 Electron Developer Agent
    
    Генерирует:
    - Electron приложения
    - IPC Communication
    - Auto-updater
    - Tray/Menu
    - Window management
    """
    
    AGENT_TYPE = 'electron'
    NAME = 'Electron Agent'
    EMOJI = '🪟'
    
    def can_execute(self, task: Task) -> bool:
        return task.agent_type in ['electron', 'desktop', 'crossplatform']
    
    def execute(self, task: Task) -> Dict:
        title = task.title.lower()
        
        if 'notes' in title or 'note' in title or 'заметки' in title:
            return self._create_notes_app(task)
        elif 'todo' in title or 'tasks' in title or 'задачи' in title:
            return self._create_todo_app(task)
        elif 'chat' in title or 'messenger' in title or 'чат' in title:
            return self._create_chat_app(task)
        else:
            return self._create_default_app(task)
    
    def _create_notes_app(self, task: Task) -> Dict:
        """Создаёт приложение для заметок"""
        
        main_js = '''const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

const NOTES_FILE = path.join(app.getPath('userData'), 'notes.json');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        titleBarStyle: 'hiddenInset',
        show: false
    });

    mainWindow.loadFile('index.html');
    
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });
}

// Загрузка заметок
ipcMain.handle('load-notes', async () => {
    try {
        if (fs.existsSync(NOTES_FILE)) {
            const data = fs.readFileSync(NOTES_FILE, 'utf8');
            return JSON.parse(data);
        }
        return [];
    } catch (error) {
        console.error('Error loading notes:', error);
        return [];
    }
});

// Сохранение заметок
ipcMain.handle('save-notes', async (event, notes) => {
    try {
        fs.writeFileSync(NOTES_FILE, JSON.stringify(notes, null, 2));
        return { success: true };
    } catch (error) {
        console.error('Error saving notes:', error);
        return { success: false, error: error.message };
    }
});

// Экспорт
ipcMain.handle('export-notes', async (event, notes) => {
    const { filePath } = await dialog.showSaveDialog(mainWindow, {
        defaultPath: 'my-notes.json',
        filters: [
            { name: 'JSON', extensions: ['json'] },
            { name: 'All Files', extensions: ['*'] }
        ]
    });
    
    if (filePath) {
        fs.writeFileSync(filePath, JSON.stringify(notes, null, 2));
        return { success: true };
    }
    return { success: false };
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
'''

        preload_js = '''const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    loadNotes: () => ipcRenderer.invoke('load-notes'),
    saveNotes: (notes) => ipcRenderer.invoke('save-notes', notes),
    exportNotes: (notes) => ipcRenderer.invoke('export-notes', notes)
});
'''

        html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📝 Notes App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>📝 Notes</h1>
                <button id="newNoteBtn" class="btn btn-primary">+ Новая</button>
            </div>
            <div id="notesList" class="notes-list"></div>
        </aside>
        
        <main class="editor">
            <div class="editor-header">
                <input type="text" id="noteTitle" placeholder="Заголовок...">
                <div class="editor-actions">
                    <button id="saveBtn" class="btn btn-success">💾 Сохранить</button>
                    <button id="deleteBtn" class="btn btn-danger">🗑️ Удалить</button>
                    <button id="exportBtn" class="btn btn-secondary">📤 Экспорт</button>
                </div>
            </div>
            <textarea id="noteContent" placeholder="Начните писать..."></textarea>
        </main>
    </div>
    
    <script src="renderer.js"></script>
</body>
</html>
'''

        css = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f5f5f5;
    overflow: hidden;
}

.app {
    display: flex;
    height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 300px;
    background: #1e1e1e;
    color: white;
    display: flex;
    flex-direction: column;
}

.sidebar-header {
    padding: 20px;
    border-bottom: 1px solid #333;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sidebar-header h1 {
    font-size: 18px;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    transition: opacity 0.2s;
}

.btn:hover {
    opacity: 0.9;
}

.btn-primary {
    background: #0a84ff;
    color: white;
}

.btn-success {
    background: #30d158;
    color: white;
}

.btn-danger {
    background: #ff453a;
    color: white;
}

.btn-secondary {
    background: #3a3a3c;
    color: white;
}

.notes-list {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
}

.note-item {
    padding: 12px;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 8px;
    transition: background 0.2s;
}

.note-item:hover {
    background: #2c2c2e;
}

.note-item.active {
    background: #0a84ff;
}

.note-item h3 {
    font-size: 14px;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.note-item p {
    font-size: 12px;
    color: #8e8e93;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.note-item.active p {
    color: rgba(255,255,255,0.7);
}

/* Editor */
.editor {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: white;
}

.editor-header {
    padding: 20px;
    border-bottom: 1px solid #e5e5e5;
    display: flex;
    gap: 12px;
    align-items: center;
}

#noteTitle {
    flex: 1;
    font-size: 24px;
    border: none;
    outline: none;
    font-weight: 600;
}

.editor-actions {
    display: flex;
    gap: 8px;
}

#noteContent {
    flex: 1;
    padding: 20px;
    border: none;
    outline: none;
    font-size: 16px;
    line-height: 1.6;
    resize: none;
    font-family: inherit;
}
'''

        renderer_js = '''let notes = [];
let currentNoteId = null;

const notesList = document.getElementById('notesList');
const noteTitle = document.getElementById('noteTitle');
const noteContent = document.getElementById('noteContent');
const newNoteBtn = document.getElementById('newNoteBtn');
const saveBtn = document.getElementById('saveBtn');
const deleteBtn = document.getElementById('deleteBtn');
const exportBtn = document.getElementById('exportBtn');

// Загрузка заметок
async function loadNotes() {
    notes = await window.electronAPI.loadNotes();
    renderNotesList();
    
    if (notes.length > 0 && !currentNoteId) {
        selectNote(notes[0].id);
    }
}

// Отрисовка списка
function renderNotesList() {
    notesList.innerHTML = notes.map(note => `
        <div class="note-item ${note.id === currentNoteId ? 'active' : ''}" data-id="${note.id}">
            <h3>${note.title || 'Без названия'}</h3>
            <p>${note.content.substring(0, 50) || 'Нет содержания'}...</p>
        </div>
    `).join('');
    
    // Обработчики клика
    document.querySelectorAll('.note-item').forEach(item => {
        item.addEventListener('click', () => {
            selectNote(item.dataset.id);
        });
    });
}

// Выбор заметки
function selectNote(id) {
    currentNoteId = id;
    const note = notes.find(n => n.id === id);
    if (note) {
        noteTitle.value = note.title;
        noteContent.value = note.content;
    }
    renderNotesList();
}

// Новая заметка
newNoteBtn.addEventListener('click', () => {
    const newNote = {
        id: Date.now().toString(),
        title: '',
        content: '',
        created: new Date().toISOString()
    };
    notes.unshift(newNote);
    selectNote(newNote.id);
    saveNotes();
});

// Сохранение
async function saveNotes() {
    if (currentNoteId) {
        const note = notes.find(n => n.id === currentNoteId);
        if (note) {
            note.title = noteTitle.value;
            note.content = noteContent.value;
            note.updated = new Date().toISOString();
        }
    }
    
    await window.electronAPI.saveNotes(notes);
    renderNotesList();
}

saveBtn.addEventListener('click', saveNotes);
noteTitle.addEventListener('input', saveNotes);
noteContent.addEventListener('input', saveNotes);

// Удаление
deleteBtn.addEventListener('click', async () => {
    if (currentNoteId && confirm('Удалить заметку?')) {
        notes = notes.filter(n => n.id !== currentNoteId);
        currentNoteId = null;
        noteTitle.value = '';
        noteContent.value = '';
        await window.electronAPI.saveNotes(notes);
        renderNotesList();
    }
});

// Экспорт
exportBtn.addEventListener('click', async () => {
    await window.electronAPI.exportNotes(notes);
    alert('Заметки экспортированы!');
});

// Загрузка при старте
loadNotes();
'''

        package_json = '''{
  "name": "notes-app",
  "version": "1.0.0",
  "description": "Приложение для заметок на Electron",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder",
    "build:win": "electron-builder --win",
    "build:mac": "electron-builder --mac",
    "build:linux": "electron-builder --linux"
  },
  "devDependencies": {
    "electron": "^28.0.0",
    "electron-builder": "^24.0.0"
  },
  "build": {
    "appId": "com.ai-gov.notes",
    "productName": "Notes App",
    "directories": {
      "output": "dist"
    },
    "files": [
      "main.js",
      "preload.js",
      "renderer.js",
      "index.html",
      "styles.css"
    ]
  }
}
'''

        return {
            'success': True,
            'message': f'✅ Electron Notes App создан!',
            'artifacts': {
                'main.js': main_js,
                'preload.js': preload_js,
                'index.html': html,
                'styles.css': css,
                'renderer.js': renderer_js,
                'package.json': package_json
            }
        }
    
    def _create_todo_app(self, task: Task) -> Dict:
        """Создаёт TODO приложение"""
        
        main_js = '''const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

const TODOS_FILE = path.join(app.getPath('userData'), 'todos.json');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 500,
        height: 700,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        resizable: false
    });

    mainWindow.loadFile('index.html');
}

ipcMain.handle('load-todos', async () => {
    try {
        if (fs.existsSync(TODOS_FILE)) {
            return JSON.parse(fs.readFileSync(TODOS_FILE, 'utf8'));
        }
        return [];
    } catch (error) {
        return [];
    }
});

ipcMain.handle('save-todos', async (event, todos) => {
    fs.writeFileSync(TODOS_FILE, JSON.stringify(todos, null, 2));
    return { success: true };
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
'''

        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>✅ Todo App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app">
        <h1>✅ Мои задачи</h1>
        <div class="input-group">
            <input type="text" id="todoInput" placeholder="Новая задача...">
            <button id="addBtn">+</button>
        </div>
        <ul id="todoList"></ul>
        <div class="stats">
            <span id="completedCount">0 выполнено</span>
            <button id="clearBtn">Очистить выполненные</button>
        </div>
    </div>
    <script src="renderer.js"></script>
</body>
</html>
'''

        css = '''body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    margin: 0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.app {
    background: white;
    border-radius: 20px;
    padding: 30px;
    width: 400px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
}

.input-group {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

#todoInput {
    flex: 1;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 16px;
    outline: none;
}

#todoInput:focus {
    border-color: #667eea;
}

#addBtn {
    width: 44px;
    height: 44px;
    border: none;
    border-radius: 10px;
    background: #667eea;
    color: white;
    font-size: 24px;
    cursor: pointer;
    transition: transform 0.2s;
}

#addBtn:hover {
    transform: scale(1.1);
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 400px;
    overflow-y: auto;
}

li {
    display: flex;
    align-items: center;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 10px;
    margin-bottom: 8px;
    transition: all 0.3s;
}

li.completed span {
    text-decoration: line-through;
    opacity: 0.5;
}

li input[type="checkbox"] {
    width: 20px;
    height: 20px;
    margin-right: 12px;
    cursor: pointer;
}

li span {
    flex: 1;
    font-size: 16px;
}

li button {
    background: #ff6b6b;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    cursor: pointer;
    font-size: 12px;
}

.stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #e0e0e0;
}

#clearBtn {
    background: transparent;
    border: 1px solid #ddd;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
}

#clearBtn:hover {
    background: #f0f0f0;
}
'''

        renderer_js = '''let todos = [];

const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const completedCount = document.getElementById('completedCount');
const clearBtn = document.getElementById('clearBtn');

async function loadTodos() {
    todos = await window.electronAPI.loadTodos();
    renderTodos();
}

function renderTodos() {
    todoList.innerHTML = todos.map(todo => `
        <li class="${todo.completed ? 'completed' : ''}">
            <input type="checkbox" ${todo.completed ? 'checked' : ''} 
                   onchange="toggleTodo('${todo.id}')">
            <span>${todo.text}</span>
            <button onclick="deleteTodo('${todo.id}')">Удалить</button>
        </li>
    `).join('');
    
    const completed = todos.filter(t => t.completed).length;
    completedCount.textContent = `${completed} выполнено из ${todos.length}`;
}

async function addTodo() {
    const text = todoInput.value.trim();
    if (!text) return;
    
    todos.push({
        id: Date.now().toString(),
        text: text,
        completed: false,
        created: new Date().toISOString()
    });
    
    todoInput.value = '';
    await window.electronAPI.saveTodos(todos);
    renderTodos();
}

async function toggleTodo(id) {
    const todo = todos.find(t => t.id === id);
    if (todo) {
        todo.completed = !todo.completed;
        await window.electronAPI.saveTodos(todos);
        renderTodos();
    }
}

async function deleteTodo(id) {
    todos = todos.filter(t => t.id !== id);
    await window.electronAPI.saveTodos(todos);
    renderTodos();
}

async function clearCompleted() {
    todos = todos.filter(t => !t.completed);
    await window.electronAPI.saveTodos(todos);
    renderTodos();
}

addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
});
clearBtn.addEventListener('click', clearCompleted);

loadTodos();
'''

        preload_js = '''const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    loadTodos: () => ipcRenderer.invoke('load-todos'),
    saveTodos: (todos) => ipcRenderer.invoke('save-todos', todos)
});
'''

        package_json = '''{
  "name": "todo-app",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "devDependencies": {
    "electron": "^28.0.0"
  }
}
'''

        return {
            'success': True,
            'message': f'✅ Electron Todo App создан!',
            'artifacts': {
                'main.js': main_js,
                'preload.js': preload_js,
                'index.html': html,
                'styles.css': css,
                'renderer.js': renderer_js,
                'package.json': package_json
            }
        }
    
    def _create_chat_app(self, task: Task) -> Dict:
        """Создаёт простое чат-приложение"""
        
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>💬 Chat App</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #0084ff;
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f0f2f5;
        }
        .message {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 18px;
            margin-bottom: 10px;
            word-wrap: break-word;
        }
        .message.sent {
            background: #0084ff;
            color: white;
            margin-left: auto;
        }
        .message.received {
            background: white;
            margin-right: auto;
        }
        .input-area {
            padding: 15px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }
        #messageInput {
            flex: 1;
            padding: 12px;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            outline: none;
        }
        #sendBtn {
            padding: 12px 24px;
            background: #0084ff;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <span style="font-size: 24px;">💬</span>
        <span>Локальный Чат</span>
    </div>
    <div class="messages" id="messages"></div>
    <div class="input-area">
        <input type="text" id="messageInput" placeholder="Введите сообщение...">
        <button id="sendBtn">Отправить</button>
    </div>
    <script src="chat.js"></script>
</body>
</html>
'''

        chat_js = '''const messages = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

function addMessage(text, sent = true) {
    const div = document.createElement('div');
    div.className = `message ${sent ? 'sent' : 'received'}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    
    addMessage(text, true);
    messageInput.value = '';
    
    // Имитация ответа
    setTimeout(() => {
        const responses = [
            'Интересно!',
            'Понял вас',
            'Согласен',
            'Расскажите подробнее',
            'Отлично!'
        ];
        const response = responses[Math.floor(Math.random() * responses.length)];
        addMessage(response, false);
    }, 1000);
}

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Приветственное сообщение
setTimeout(() => {
    addMessage('Привет! 👋 Чем могу помочь?', false);
}, 500);
'''

        return {
            'success': True,
            'message': f'✅ Electron Chat App создан!',
            'artifacts': {
                'index.html': html,
                'chat.js': chat_js,
                'main.js': 'const { app, BrowserWindow } = require("electron");\nfunction createWindow() {\n  new BrowserWindow({width: 500, height: 700}).loadFile("index.html");\n}\napp.whenReady().then(createWindow);',
                'package.json': '{"name": "chat-app", "main": "main.js", "scripts": {"start": "electron ."}}'
            }
        }
    
    def _create_default_app(self, task: Task) -> Dict:
        """Создаёт базовое Electron приложение"""
        
        return {
            'success': True,
            'message': f'✅ Базовое Electron приложение создано!',
            'artifacts': {
                'main.js': '''const { app, BrowserWindow } = require('electron');

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);
''',
                'index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Electron App</title>
</head>
<body>
    <h1>🪟 Hello from Electron!</h1>
    <p>Создано с помощью AI Правительство</p>
</body>
</html>
''',
                'package.json': '''{
  "name": "electron-app",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  }
}'''
            }
        }
