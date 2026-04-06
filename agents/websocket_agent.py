#!/usr/bin/env python3
"""
🌐 WebSocket-Agent
WebSocket Specialist агент

Создаёт:
- WebSocket серверы
- Real-time приложения
- Socket.io интеграции
- Live updates
"""

import argparse
from pathlib import Path
from typing import Dict


class WebSocketAgent:
    """
    🌐 WebSocket-Agent
    
    Специализация: Real-time Communication
    Стек: Socket.io, WebSocket, Node.js
    """
    
    NAME = "🌐 WebSocket-Agent"
    ROLE = "WebSocket Specialist"
    EXPERTISE = ["Socket.io", "WebSocket", "Real-time", "Live Updates", "Pub/Sub"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["websocket-server.js"] = """const { Server } = require('socket.io');
const http = require('http');
const express = require('express');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Store connected users
const connectedUsers = new Map();
const rooms = new Map();

// Middleware for authentication
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (token) {
    // Verify token here
    socket.userId = 'user_' + Math.random().toString(36).substr(2, 9);
    socket.username = socket.handshake.auth.username || 'Anonymous';
    next();
  } else {
    next(new Error('Authentication error'));
  }
});

io.on('connection', (socket) => {
  console.log(`🔌 User connected: ${socket.username} (${socket.id})`);
  
  // Store user
  connectedUsers.set(socket.id, {
    id: socket.id,
    userId: socket.userId,
    username: socket.username,
    connectedAt: new Date()
  });
  
  // Broadcast user joined
  socket.broadcast.emit('user:joined', {
    userId: socket.userId,
    username: socket.username,
    onlineCount: connectedUsers.size
  });
  
  // Send current online users to new user
  socket.emit('users:online', Array.from(connectedUsers.values()));
  
  // Join room
  socket.on('room:join', (roomId, callback) => {
    socket.join(roomId);
    
    if (!rooms.has(roomId)) {
      rooms.set(roomId, new Set());
    }
    rooms.get(roomId).add(socket.id);
    
    // Notify room
    socket.to(roomId).emit('room:userJoined', {
      userId: socket.userId,
      username: socket.username,
      roomId
    });
    
    callback({
      success: true,
      roomId,
      usersInRoom: Array.from(rooms.get(roomId))
    });
  });
  
  // Leave room
  socket.on('room:leave', (roomId) => {
    socket.leave(roomId);
    
    if (rooms.has(roomId)) {
      rooms.get(roomId).delete(socket.id);
    }
    
    socket.to(roomId).emit('room:userLeft', {
      userId: socket.userId,
      username: socket.username,
      roomId
    });
  });
  
  // Handle messages
  socket.on('message:send', (data) => {
    const message = {
      id: Date.now().toString(),
      userId: socket.userId,
      username: socket.username,
      content: data.content,
      roomId: data.roomId,
      timestamp: new Date().toISOString()
    };
    
    if (data.roomId) {
      // Send to room
      io.to(data.roomId).emit('message:received', message);
    } else {
      // Broadcast to all
      io.emit('message:received', message);
    }
  });
  
  // Typing indicator
  socket.on('typing:start', (roomId) => {
    socket.to(roomId).emit('typing:update', {
      userId: socket.userId,
      username: socket.username,
      isTyping: true
    });
  });
  
  socket.on('typing:stop', (roomId) => {
    socket.to(roomId).emit('typing:update', {
      userId: socket.userId,
      username: socket.username,
      isTyping: false
    });
  });
  
  // Handle disconnect
  socket.on('disconnect', (reason) => {
    console.log(`❌ User disconnected: ${socket.username} (${reason})`);
    
    connectedUsers.delete(socket.id);
    
    // Leave all rooms
    rooms.forEach((users, roomId) => {
      if (users.has(socket.id)) {
        users.delete(socket.id);
        socket.to(roomId).emit('room:userLeft', {
          userId: socket.userId,
          username: socket.username,
          roomId
        });
      }
    });
    
    // Broadcast user left
    socket.broadcast.emit('user:left', {
      userId: socket.userId,
      username: socket.username,
      onlineCount: connectedUsers.size
    });
  });
});

// HTTP endpoints
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    connections: connectedUsers.size,
    uptime: process.uptime()
  });
});

app.get('/stats', (req, res) => {
  res.json({
    connectedUsers: Array.from(connectedUsers.values()),
    activeRooms: rooms.size,
    usersPerRoom: Object.fromEntries(
      Array.from(rooms.entries()).map(([k, v]) => [k, v.size])
    )
  });
});

const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  console.log(`🚀 WebSocket server running on port ${PORT}`);
});
"""
        
        files["websocket-client.js"] = """class WebSocketClient {
  constructor(url, options = {}) {
    this.url = url;
    this.options = options;
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
    this.reconnectDelay = options.reconnectDelay || 1000;
    this.listeners = new Map();
    this.isConnected = false;
  }
  
  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.socket = io(this.url, {
          auth: {
            token: this.options.token,
            username: this.options.username
          },
          transports: ['websocket', 'polling']
        });
        
        this.socket.on('connect', () => {
          console.log('✅ Connected to server');
          this.isConnected = true;
          this.reconnectAttempts = 0;
          this.emit('connected');
          resolve();
        });
        
        this.socket.on('disconnect', (reason) => {
          console.log('❌ Disconnected:', reason);
          this.isConnected = false;
          this.emit('disconnected', reason);
          
          if (reason === 'io server disconnect') {
            // Server forced disconnect, don't reconnect
            return;
          }
          
          this.attemptReconnect();
        });
        
        this.socket.on('connect_error', (error) => {
          console.error('Connection error:', error);
          this.emit('error', error);
          reject(error);
        });
        
        // Setup event listeners
        this.setupEventListeners();
        
      } catch (error) {
        reject(error);
      }
    });
  }
  
  setupEventListeners() {
    // User events
    this.socket.on('user:joined', (data) => {
      this.emit('userJoined', data);
    });
    
    this.socket.on('user:left', (data) => {
      this.emit('userLeft', data);
    });
    
    this.socket.on('users:online', (users) => {
      this.emit('onlineUsers', users);
    });
    
    // Message events
    this.socket.on('message:received', (message) => {
      this.emit('message', message);
    });
    
    // Room events
    this.socket.on('room:userJoined', (data) => {
      this.emit('roomUserJoined', data);
    });
    
    this.socket.on('room:userLeft', (data) => {
      this.emit('roomUserLeft', data);
    });
    
    // Typing events
    this.socket.on('typing:update', (data) => {
      this.emit('typingUpdate', data);
    });
  }
  
  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.emit('reconnectFailed');
      return;
    }
    
    this.reconnectAttempts++;
    console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
    
    setTimeout(() => {
      this.connect();
    }, this.reconnectDelay * this.reconnectAttempts);
  }
  
  // Join a room
  joinRoom(roomId) {
    return new Promise((resolve) => {
      this.socket.emit('room:join', roomId, (response) => {
        resolve(response);
      });
    });
  }
  
  // Leave a room
  leaveRoom(roomId) {
    this.socket.emit('room:leave', roomId);
  }
  
  // Send message
  sendMessage(content, roomId = null) {
    this.socket.emit('message:send', { content, roomId });
  }
  
  // Typing indicators
  startTyping(roomId) {
    this.socket.emit('typing:start', roomId);
  }
  
  stopTyping(roomId) {
    this.socket.emit('typing:stop', roomId);
  }
  
  // Event emitter pattern
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }
  
  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }
  
  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => callback(data));
    }
  }
  
  // Disconnect
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }
}

// Usage example
// const client = new WebSocketClient('ws://localhost:3001', {
//   token: 'your-token',
//   username: 'John'
// });
// 
// client.on('message', (msg) => console.log('New message:', msg));
// client.connect();
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="🌐 WebSocket-Agent — Real-time")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = WebSocketAgent()
    
    if args.request:
        print(f"🌐 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"🌐 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
