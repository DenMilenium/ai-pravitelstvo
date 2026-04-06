package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
)

// Config конфигурация сервиса
type Config struct {
	Port        string        `json:"port"`
	Environment string        `json:"environment"`
	Timeout     time.Duration `json:"timeout"`
}

func main() {
	log.Println("☁️  CloudMind API Gateway запускается...")

	config := Config{
		Port:        getEnv("PORT", "8080"),
		Environment: getEnv("ENV", "development"),
		Timeout:     30 * time.Second,
	}

	// Настройка Gin
	if config.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	router := gin.New()
	router.Use(gin.Recovery())
	router.Use(corsMiddleware())
	router.Use(requestLogger())

	// Health check
	router.GET("/health", healthHandler)
	router.GET("/ready", readinessHandler)

	// API v1
	v1 := router.Group("/api/v1")
	{
		v1.GET("/models", listModelsHandler)
		v1.POST("/models/:id/deploy", deployModelHandler)
		v1.POST("/inference", inferenceHandler)
		v1.GET("/jobs/:id", getJobStatusHandler)
	}

	// Создание HTTP сервера
	srv := &http.Server{
		Addr:         ":" + config.Port,
		Handler:      router,
		ReadTimeout:  config.Timeout,
		WriteTimeout: config.Timeout,
	}

	// Graceful shutdown
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Ошибка сервера: %v", err)
		}
	}()

	log.Printf("🚀 API Gateway запущен на порту %s", config.Port)

	// Ожидание сигнала завершения
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("🛑 Завершение работы...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("Ошибка при завершении: %v", err)
	}

	log.Println("👋 До свидания!")
}

// Middleware
func corsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}

func requestLogger() gin.HandlerFunc {
	return gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
		return log.Printf("[%s] %s %s %d %s",
			param.TimeStamp.Format("2006-01-02 15:04:05"),
			param.Method,
			param.Path,
			param.StatusCode,
			param.Latency,
		)
		return ""
	})
}

// Handlers
func healthHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":    "healthy",
		"service":   "cloudmind-api",
		"timestamp": time.Now().UTC(),
	})
}

func readinessHandler(c *gin.Context) {
	// Проверка подключения к зависимостям
	c.JSON(http.StatusOK, gin.H{
		"status":  "ready",
		"checks":  gin.H{
			"database": "ok",
			"cache":    "ok",
			"queue":    "ok",
		},
	})
}

type Model struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Version     string    `json:"version"`
	Status      string    `json:"status"`
	CreatedAt   time.Time `json:"created_at"`
}

var mockModels = []Model{
	{
		ID:          "gpt-local-7b",
		Name:        "GPT Local 7B",
		Description: "Локальная языковая модель 7B параметров",
		Version:     "1.0.0",
		Status:      "available",
		CreatedAt:   time.Now(),
	},
	{
		ID:          "llama-2-13b",
		Name:        "Llama 2 13B",
		Description: "Модель Llama 2 от Meta",
		Version:     "2.0.0",
		Status:      "available",
		CreatedAt:   time.Now(),
	},
}

func listModelsHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"models": mockModels,
		"total":  len(mockModels),
	})
}

type DeployRequest struct {
	InstanceType string `json:"instance_type" binding:"required"`
	Replicas     int    `json:"replicas" binding:"min=1,max=10"`
}

func deployModelHandler(c *gin.Context) {
	modelID := c.Param("id")

	var req DeployRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Имитация деплоя
	deployment := gin.H{
		"id":            "dep_" + generateID(),
		"model_id":      modelID,
		"status":        "deploying",
		"instance_type": req.InstanceType,
		"replicas":      req.Replicas,
		"endpoint":      "https://api.cloudmind.ai/v1/inference/" + modelID,
		"created_at":    time.Now().UTC(),
	}

	c.JSON(http.StatusAccepted, deployment)
}

type InferenceRequest struct {
	ModelID string `json:"model_id" binding:"required"`
	Prompt  string `json:"prompt" binding:"required"`
	MaxTokens int  `json:"max_tokens"`
}

type InferenceResponse struct {
	ID       string `json:"id"`
	ModelID  string `json:"model_id"`
	Output   string `json:"output"`
	Tokens   int    `json:"tokens"`
	Duration int    `json:"duration_ms"`
}

func inferenceHandler(c *gin.Context) {
	var req InferenceRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Имитация инференса
	start := time.Now()
	output := generateMockResponse(req.Prompt)
	duration := time.Since(start)

	resp := InferenceResponse{
		ID:       "inf_" + generateID(),
		ModelID:  req.ModelID,
		Output:   output,
		Tokens:   len(output) / 4, // Примерная оценка
		Duration: int(duration.Milliseconds()),
	}

	c.JSON(http.StatusOK, resp)
}

func getJobStatusHandler(c *gin.Context) {
	jobID := c.Param("id")

	c.JSON(http.StatusOK, gin.H{
		"id":     jobID,
		"status": "completed",
		"result": gin.H{
			"url": "https://storage.cloudmind.ai/results/" + jobID,
		},
	})
}

// Helpers
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func generateID() string {
	// Упрощённая генерация ID
	return time.Now().Format("20060102150405")
}

func generateMockResponse(prompt string) string {
	responses := []string{
		"На основе вашего запроса, я могу предложить следующее решение...",
		"Интересный вопрос! Вот что я думаю по этому поводу...",
		"Анализируя ваш запрос, прихожу к выводу...",
		"Вот ответ на ваш вопрос:",
	}
	
	// Простая логика выбора ответа
	idx := len(prompt) % len(responses)
	return responses[idx] + "\n\n[Это тестовый ответ от CloudMind API]"
}
