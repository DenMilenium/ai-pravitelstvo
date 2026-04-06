.PHONY: help install test lint build clean

BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
NC := \033[0m

help: ## Показать справку по командам
	@echo "$(BLUE)╔══════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║   🤖 AI Правительство - Кабинет     ║$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════╝$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Министерства:$(NC)"
	@echo "  $(GREEN)ministry-desktop$(NC)  Работа с Мин. Десктопных Приложений"
	@echo "  $(GREEN)ministry-cloud$(NC)    Работа с Мин. Облачных Решений"
	@echo "  $(GREEN)ministry-research$(NC) Работа с Мин. Научных Исследований"

install: ## Установка всех зависимостей
	@echo "$(GREEN)📦 Установка зависимостей...$(NC)"
	$(MAKE) -C ministries/desktop install
	$(MAKE) -C ministries/cloud install

test: ## Запуск всех тестов
	@echo "$(GREEN)🧪 Запуск всех тестов...$(NC)"
	$(MAKE) -C ministries/desktop test
	$(MAKE) -C ministries/cloud test

lint: ## Проверка кода
	@echo "$(GREEN)🔍 Проверка кода...$(NC)"
	$(MAKE) -C ministries/desktop lint
	$(MAKE) -C ministries/cloud lint

build: ## Сборка всех проектов
	@echo "$(GREEN)🔨 Сборка всех проектов...$(NC)"
	$(MAKE) -C ministries/desktop build
	$(MAKE) -C ministries/cloud build

ministry-desktop: ## Перейти в Министерство Десктопных Приложений
	@echo "$(BLUE)🏛️  Переход в Министерство Десктопных Приложений$(NC)"
	@cd ministries/desktop && exec bash

ministry-cloud: ## Перейти в Министерство Облачных Решений
	@echo "$(BLUE)☁️  Переход в Министерство Облачных Решений$(NC)"
	@cd ministries/cloud && exec bash

ministry-research: ## Перейти в Министерство Научных Исследований
	@echo "$(BLUE)🔬 Переход в Министерство Научных Исследований$(NC)"
	@cd ministries/research && exec bash

docker-build: ## Сборка всех Docker образов
	@echo "$(GREEN)🐳 Сборка Docker образов...$(NC)"
	$(MAKE) -C ministries/cloud docker-build

deploy-staging: ## Деплой в staging
	@echo "$(GREEN)🚀 Деплой в staging...$(NC)"
	$(MAKE) -C ministries/cloud deploy ENV=staging

deploy-production: ## Деплой в production
	@echo "$(GREEN)🚀 Деплой в production...$(NC)"
	$(MAKE) -C ministries/cloud deploy ENV=production

clean: ## Очистка всех артефактов
	@echo "$(GREEN)🗑️  Очистка...$(NC)"
	$(MAKE) -C ministries/desktop clean
	$(MAKE) -C ministries/cloud clean

stats: ## Статистика проекта
	@echo "$(BLUE)📊 Статистика AI Правительства:$(NC)"
	@echo ""
	@echo "$(YELLOW)Код:$(NC)"
	@find . -name "*.py" -o -name "*.go" -o -name "*.ts" -o -name "*.tsx" | wc -l | xargs echo "  Файлов:"
	@find . -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print "  Python строк: " $$1}'
	@find . -name "*.go" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print "  Go строк: " $$1}'
	@echo ""
	@echo "$(YELLOW)Проекты:$(NC)"
	@ls -1 ministries/desktop/projects 2>/dev/null | wc -l | xargs echo "  Десктоп:"
	@ls -1 ministries/cloud/projects 2>/dev/null | wc -l | xargs echo "  Облако:"

credits: ## Список участников
	@echo "$(BLUE)🎖️  Министры AI Правительства:$(NC)"
	@echo ""
	@echo "  🖥️  Министерство Десктопных Приложений"
	@echo "  ☁️  Министерство Облачных Решений"
	@echo "  🔬 Министерство Научных Исследований"
	@echo "  📋 Министерство Проектного Управления"
	@echo "  🔧 Министерство Инфраструктуры"
	@echo "  👥 Министерство Кадров"
