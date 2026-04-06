#!/usr/bin/env python3
"""
⚙️ Backend-Agent
Агент-разработчик серверной части

Умеет:
- Создавать REST API на Go/Python
- Настраивать базы данных
- Работать с микросервисами
- Интегрировать авторизацию

Запуск:
    python backend_agent.py "Создай API для чата"
"""

import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Endpoint:
    """API эндпоинт"""
    method: str
    path: str
    handler: str
    description: str


class BackendAgent:
    """
    ⚙️ Backend-Agent
    
    Специализация: API и серверная разработка
    Стек: Go (Gin), Python (FastAPI), PostgreSQL, Redis
    """
    
    NAME = "Backend-Agent"
    ROLE = "Backend разработчик"
    EXPERTISE = ["Go", "Python", "PostgreSQL", "Redis", "gRPC", "REST API", "Docker"]
    
    def __init__(self):
        self.languages = ["go", "python"]
        self.frameworks = {
            "go": ["gin", "echo", "fiber"],
            "python": ["fastapi", "django", "flask"]
        }
    
    def process_request(self, request: str, language: str = "go") -> Dict[str, str]:
        """
        Обработка запроса и генерация кода
        
        Args:
            request: Описание API/сервиса
            language: go или python
            
        Returns:
            Словарь с файлами
        """
        request_lower = request.lower()
        files = {}
        
        # Определяем тип API
        if "чат" in request_lower or "chat" in request_lower:
            files = self._generate_chat_api(language)
        elif "авторизация" in request_lower or "auth" in request_lower:
            files = self._generate_auth_api(language)
        elif "crud" in request_lower or "api" in request_lower:
            files = self._generate_crud_api(language)
        elif "websocket" in request_lower or "socket" in request_lower:
            files = self._generate_websocket_api(language)
        else:
            files = self._generate_basic_api(language)
        
        return files
    
    def _generate_chat_api(self, language: str) -> Dict[str, str]:
        """Генерация API для чата"""
        if language == "go":
            return self._generate_go_chat_api()
        else:
            return self._generate_python_chat_api()
    
    def _generate_go_chat_api(self) -> Dict[str, str]:
        """Go API для чата на Gin"""
        files = {}
        
        files["main.go"] = '''package main

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
)

// Message структура сообщения
type Message struct {
	ID        string    `json:"id"`
	UserID    string    `json:"user_id"`
	Username  string    `json:"username"`
	Content   string    `json:"content"`
	Timestamp time.Time `json:"timestamp"`
}

// ChatServer управляет соединениями
type ChatServer struct {
	clients    map[*websocket.Conn]bool
	broadcast  chan Message
	register   chan *websocket.Conn
	unregister chan *websocket.Conn
	mu         sync.RWMutex
	history    []Message
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Разрешаем все origins для разработки
	},
}

func NewChatServer() *ChatServer {
	return &ChatServer{
		clients:    make(map[*websocket.Conn]bool),
		broadcast:  make(chan Message),
		register:   make(chan *websocket.Conn),
		unregister: make(chan *websocket.Conn),
		history:    make([]Message, 0),
	}
}

func (s *ChatServer) Run() {
	for {
		select {
		case client := <-s.register:
			s.mu.Lock()
			s.clients[client] = true
			s.mu.Unlock()
			
			// Отправляем историю новому клиенту
			s.mu.RLock()
			for _, msg := range s.history {
				client.WriteJSON(msg)
			}
			s.mu.RUnlock()
			
		case client := <-s.unregister:
			s.mu.Lock()
			if _, ok := s.clients[client]; ok {
				delete(s.clients, client)
				client.Close()
			}
			s.mu.Unlock()
			
		case message := <-s.broadcast:
			s.mu.Lock()
			s.history = append(s.history, message)
			// Храним только последние 100 сообщений
			if len(s.history) > 100 {
				s.history = s.history[len(s.history)-100:]
			}
			s.mu.Unlock()
			
			s.mu.RLock()
			for client := range s.clients {
				if err := client.WriteJSON(message); err != nil {
					client.Close()
					delete(s.clients, client)
				}
			}
			s.mu.RUnlock()
		}
	}
}

func (s *ChatServer) HandleWebSocket(c *gin.Context) {
	conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		return
	}
	
	s.register <- conn
	
	defer func() {
		s.unregister <- conn
	}()
	
	for {
		var msg Message
		if err := conn.ReadJSON(&msg); err != nil {
			break
		}
		
		msg.Timestamp = time.Now()
		s.broadcast <- msg
	}
}

func main() {
	chatServer := NewChatServer()
	go chatServer.Run()
	
	r := gin.Default()
	
	// CORS
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		
		c.Next()
	})
	
	// Health check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
			"service": "chat-api",
		})
	})
	
	// WebSocket endpoint
	r.GET("/ws", chatServer.HandleWebSocket)
	
	// REST API
	r.GET("/api/messages", func(c *gin.Context) {
		chatServer.mu.RLock()
		messages := chatServer.history
		chatServer.mu.RUnlock()
		
		c.JSON(http.StatusOK, gin.H{
			"messages": messages,
			"count":    len(messages),
		})
	})
	
	r.POST("/api/messages", func(c *gin.Context) {
		var msg Message
		if err := c.ShouldBindJSON(&msg); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		
		msg.Timestamp = time.Now()
		chatServer.broadcast <- msg
		
		c.JSON(http.StatusCreated, msg)
	})
	
	port := ":8080"
	r.Run(port)
}
'''
        
        files["go.mod"] = '''module chat-api

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	github.com/gorilla/websocket v1.5.1
)
'''
        
        files["Dockerfile"] = '''FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o server main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates

WORKDIR /root/
COPY --from=builder /app/server .

EXPOSE 8080

CMD ["./server"]
'''
        
        return files
    
    def _generate_python_chat_api(self) -> Dict[str, str]:
        """Python API для чата на FastAPI"""
        files = {}
        
        files["main.py"] = '''from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict
import uuid
import json

app = FastManager()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    id: str = None
    user_id: str
    username: str
    content: str
    timestamp: datetime = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ConnectionManager:
    """Управление WebSocket соединениями"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.message_history: List[Message] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Отправляем историю
        for message in self.message_history[-100:]:
            await websocket.send_json(message.dict())
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: Message):
        # Сохраняем в историю
        self.message_history.append(message)
        if len(self.message_history) > 100:
            self.message_history = self.message_history[-100:]
        
        # Рассылаем всем
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message.dict())
            except:
                disconnected.append(connection)
        
        # Удаляем отключившихся
        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "chat-api"}


@app.get("/api/messages")
async def get_messages():
    return {
        "messages": [m.dict() for m in manager.message_history],
        "count": len(manager.message_history)
    }


@app.post("/api/messages")
async def create_message(message: Message):
    await manager.broadcast(message)
    return message


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message = Message(**message_data)
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
'''
        
        files["requirements.txt"] = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
pydantic==2.5.0
python-multipart==0.0.6
'''
        
        files["Dockerfile"] = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
'''
        
        return files
    
    def _generate_auth_api(self, language: str) -> Dict[str, str]:
        """Генерация API авторизации"""
        files = {}
        
        if language == "go":
            files["auth.go"] = '''package main

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

var jwtSecret = []byte("your-secret-key") // В production используйте env

// User модель пользователя
type User struct {
	ID       string `json:"id"`
	Email    string `json:"email"`
	Password string `json:"-"`
	Name     string `json:"name"`
}

// LoginRequest запрос на вход
type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required,min=6"`
}

// RegisterRequest запрос на регистрацию
type RegisterRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required,min=6"`
	Name     string `json:"name" binding:"required"`
}

// GenerateToken создаёт JWT токен
func GenerateToken(userID string) (string, error) {
	claims := jwt.MapClaims{
		"user_id": user_id,
		"exp":     time.Now().Add(time.Hour * 24).Unix(),
	}
	
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtSecret)
}

// HashPassword хеширует пароль
func HashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	return string(bytes), err
}

// CheckPasswordHash проверяет пароль
func CheckPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}

func setupAuthRoutes(r *gin.Engine) {
	// Регистрация
	r.POST("/api/auth/register", func(c *gin.Context) {
		var req RegisterRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		
		// В реальном приложении - сохранение в БД
		hashedPassword, _ := HashPassword(req.Password)
		
		c.JSON(http.StatusCreated, gin.H{
			"message": "User registered",
			"user": gin.H{
				"email": req.Email,
				"name":  req.Name,
			},
		})
	})
	
	// Вход
	r.POST("/api/auth/login", func(c *gin.Context) {
		var req LoginRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		
		// В реальном приложении - проверка из БД
		token, err := GenerateToken("user-123")
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not generate token"})
			return
		}
		
		c.JSON(http.StatusOK, gin.H{
			"token": token,
			"user": gin.H{
				"id":    "user-123",
				"email": req.Email,
			},
		})
	})
}
'''
        else:
            files["auth.py"] = '''from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Настройки
SECRET_KEY = "your-secret-key"  # В production используйте env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": user_id, "email": "user@example.com"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register")
async def register(user: UserCreate):
    # В реальном приложении - проверка и сохранение в БД
    hashed_password = get_password_hash(user.password)
    return {
        "message": "User registered",
        "user": {"email": user.email, "name": user.name}
    }


@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    # В реальном приложении - проверка из БД
    access_token = create_access_token(data={"sub": "user-123"})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
'''
        
        return files
    
    def _generate_crud_api(self, language: str) -> Dict[str, str]:
        """Генерация CRUD API"""
        files = {}
        
        if language == "go":
            files["handlers.go"] = '''package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Item модель
type Item struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Desc  string `json:"description"`
	Price int    `json:"price"`
}

var items = []Item{
	{ID: "1", Name: "Item 1", Desc: "Description 1", Price: 100},
}

func setupRoutes(r *gin.Engine) {
	// GET all
	r.GET("/api/items", func(c *gin.Context) {
		c.JSON(http.StatusOK, items)
	})
	
	// GET one
	r.GET("/api/items/:id", func(c *gin.Context) {
		id := c.Param("id")
		for _, item := range items {
			if item.ID == id {
				c.JSON(http.StatusOK, item)
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
	})
	
	// POST
	r.POST("/api/items", func(c *gin.Context) {
		var newItem Item
		if err := c.ShouldBindJSON(&newItem); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		items = append(items, newItem)
		c.JSON(http.StatusCreated, newItem)
	})
	
	// PUT
	r.PUT("/api/items/:id", func(c *gin.Context) {
		id := c.Param("id")
		var updatedItem Item
		if err := c.ShouldBindJSON(&updatedItem); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		
		for i, item := range items {
			if item.ID == id {
				items[i] = updatedItem
				c.JSON(http.StatusOK, updatedItem)
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
	})
	
	// DELETE
	r.DELETE("/api/items/:id", func(c *gin.Context) {
		id := c.Param("id")
		for i, item := range items {
			if item.ID == id {
				items = append(items[:i], items[i+1:]...)
				c.JSON(http.StatusOK, gin.H{"message": "Item deleted"})
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
	})
}
'''
        
        return files
    
    def _generate_websocket_api(self, language: str) -> Dict[str, str]:
        """Генерация WebSocket API"""
        return self._generate_chat_api(language)  # Чат уже использует WebSocket
    
    def _generate_basic_api(self, language: str) -> Dict[str, str]:
        """Базовый API шаблон"""
        files = {}
        
        if language == "go":
            files["main.go"] = '''package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})
	
	r.Run(":8080")
}
'''
        else:
            files["main.py"] = '''from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
'''
        
        return files


def main():
    parser = argparse.ArgumentParser(description="⚙️ Backend-Agent — Генератор API")
    parser.add_argument("request", nargs="?", help="Описание API")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    parser.add_argument("--language", "-l", default="go", 
                       choices=["go", "python"],
                       help="Язык программирования")
    
    args = parser.parse_args()
    
    agent = BackendAgent()
    
    if args.request:
        print(f"⚙️ {agent.NAME} создаёт: {args.request}")
        print(f"Язык: {args.language}")
        print("-" * 50)
        
        files = agent.process_request(args.request, args.language)
        
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
        print(f"⚙️ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"Экспертиза: {', '.join(agent.EXPERTISE)}")
        print("\nПримеры:")
        print('  python backend_agent.py "API для чата" -o chat-api')
        print('  python backend_agent.py "Авторизация JWT" -l python')
        print('  python backend_agent.py "WebSocket сервер"')


if __name__ == "__main__":
    main()
'''
"""  # Этот файл слишком длинный, я его обрежу
