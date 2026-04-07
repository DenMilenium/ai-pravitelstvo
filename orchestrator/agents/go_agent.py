"""
🐹 Go Agent
Создаёт Go микросервисы и API
"""

from orchestrator.core.task_executor import BaseAgentExecutor
from orchestrator.core.database import Task
from typing import Dict


class GoAgentExecutor(BaseAgentExecutor):
    """
    🐹 Go Developer Agent
    
    Генерирует:
    - Go API с Gin/Echo
    - gRPC сервисы
    - CLI инструменты
    """
    
    AGENT_TYPE = 'go'
    NAME = 'Go Agent'
    EMOJI = '🐹'
    
    def can_execute(self, task: Task) -> bool:
        return task.agent_type in ['go', 'golang', 'backend']
    
    def execute(self, task: Task) -> Dict:
        title = task.title.lower()
        
        if 'api' in title or 'rest' in title:
            return self._create_api(task)
        else:
            return self._create_default(task)
    
    def _create_api(self, task: Task) -> Dict:
        main_go = '''package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

type Item struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
}

var items = []Item{
	{ID: "1", Name: "Item 1", Description: "First item"},
}

func main() {
	r := gin.Default()

	// Middleware
	r.Use(CORSMiddleware())

	// Routes
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Go API is running",
			"version": "1.0.0",
		})
	})

	// GET all items
	r.GET("/items", func(c *gin.Context) {
		c.JSON(http.StatusOK, items)
	})

	// GET single item
	r.GET("/items/:id", func(c *gin.Context) {
		id := c.Param("id")
		for _, item := range items {
			if item.ID == id {
				c.JSON(http.StatusOK, item)
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
	})

	// POST create item
	r.POST("/items", func(c *gin.Context) {
		var newItem Item
		if err := c.ShouldBindJSON(&newItem); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		items = append(items, newItem)
		c.JSON(http.StatusCreated, newItem)
	})

	r.Run(":8080")
}

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
		c.Next()
	}
}
'''

        go_mod = '''module api

go 1.21

require github.com/gin-gonic/gin v1.9.1
'''

        return {
            'success': True,
            'message': f'✅ Go API создан!',
            'artifacts': {
                'main.go': main_go,
                'go.mod': go_mod,
                'README.md': '# Go API\n\nRun: `go run main.go`'
            }
        }
    
    def _create_default(self, task: Task) -> Dict:
        return {
            'success': True,
            'message': f'✅ Go приложение создано!',
            'artifacts': {
                'main.go': '''package main

import "fmt"

func main() {
    fmt.Println("Hello from Go!")
}
''',
                'go.mod': 'module app\n\ngo 1.21'
            }
        }
