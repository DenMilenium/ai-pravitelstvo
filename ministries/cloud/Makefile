.PHONY: help local-up local-down deploy monitoring

BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
NC := \033[0m

help: ## Показать справку
	@echo "$(BLUE)AI Правительство - Министерство Облачных Решений$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

local-up: ## Запуск локально с Docker Compose
	@echo "$(GREEN)🐳 Запуск локального окружения...$(NC)"
	docker-compose -f infrastructure/docker-compose.dev.yml up -d

local-down: ## Остановка локального окружения
	@echo "$(GREEN)🛑 Остановка локального окружения...$(NC)"
	docker-compose -f infrastructure/docker-compose.dev.yml down

local-logs: ## Логи локального окружения
	docker-compose -f infrastructure/docker-compose.dev.yml logs -f

dev-api: ## Запуск API в режиме разработки
	@echo "$(GREEN)🚀 Запуск API...$(NC)"
	cd projects/cloudmind/api && go run main.go

dev-web: ## Запуск Web UI в режиме разработки
	@echo "$(GREEN)🌐 Запуск Web UI...$(NC)"
	cd projects/cloudmind/web && npm run dev

build: ## Сборка всех сервисов
	@echo "$(GREEN)🔨 Сборка сервисов...$(NC)"
	cd projects/cloudmind/api && go build -o ../../../bin/api main.go

docker-build: ## Сборка Docker образов
	@echo "$(GREEN)🐳 Сборка Docker образов...$(NC)"
	docker build -t ai-gov/cloudmind-api:latest -f projects/cloudmind/api/Dockerfile .

docker-push: ## Пуш образов в registry
	@echo "$(GREEN)📤 Пуш образов...$(NC)"
	docker push ai-gov/cloudmind-api:latest

deploy: ## Деплой в кластер
	@echo "$(GREEN)🚀 Деплой в $(ENV)...$(NC)"
	kubectl apply -k infrastructure/kubernetes/overlays/$(ENV)

monitoring: ## Запуск мониторинга
	@echo "$(GREEN)📊 Запуск мониторинга...$(NC)"
	kubectl port-forward svc/grafana 3000:3000 -n monitoring

test: ## Запуск тестов
	@echo "$(GREEN)🧪 Запуск тестов...$(NC)"
	cd projects/cloudmind/api && go test ./...

test-e2e: ## E2E тесты
	@echo "$(GREEN)🧪 E2E тесты...$(NC)"
	cd tests/e2e && go test -v

tf-plan: ## Terraform plan
	@echo "$(GREEN)📋 Terraform plan...$(NC)"
	cd infrastructure/terraform && terraform plan

tf-apply: ## Terraform apply
	@echo "$(GREEN)🚀 Terraform apply...$(NC)"
	cd infrastructure/terraform && terraform apply

lint: ## Линтинг кода
	@echo "$(GREEN)🔍 Линтинг...$(NC)"
	cd projects/cloudmind/api && golangci-lint run

clean: ## Очистка
	@echo "$(GREEN)🗑️  Очистка...$(NC)"
	rm -rf bin/
	docker system prune -f
