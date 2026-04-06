.PHONY: help install dev build test clean lint

# Цвета для вывода
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
NC := \033[0m

help: ## Показать справку
	@echo "$(BLUE)AI Правительство - Министерство Десктопных Приложений$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Установка зависимостей
	@echo "$(GREEN)📦 Установка зависимостей...$(NC)"
	pip install -r requirements.txt

dev: ## Запуск в режиме разработки
	@echo "$(GREEN)🚀 Запуск в режиме разработки...$(NC)"
	cd projects/ai-assistant && python src/main.py --debug

build: ## Сборка приложений
	@echo "$(GREEN)🔨 Сборка приложений...$(NC)"
	cd projects/ai-assistant && pyinstaller --onefile src/main.py

test: ## Запуск тестов
	@echo "$(GREEN)🧪 Запуск тестов...$(NC)"
	pytest projects/ -v

test-coverage: ## Запуск тестов с покрытием
	@echo "$(GREEN)📊 Запуск тестов с покрытием...$(NC)"
	pytest projects/ --cov=src --cov-report=html

lint: ## Проверка кода
	@echo "$(GREEN)🔍 Проверка кода...$(NC)"
	flake8 projects/
	black --check projects/

format: ## Форматирование кода
	@echo "$(GREEN)✨ Форматирование кода...$(NC)"
	black projects/
	isort projects/

clean: ## Очистка временных файлов
	@echo "$(GREEN)🗑️  Очистка...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true

template: ## Создать проект из шаблона
	@echo "$(BLUE)Шаблоны: electron-react, tauri-rust, flutter-desktop$(NC)"
	@read -p "Название проекта: " name; \
	read -p "Шаблон (electron-react): " template; \
	mkdir -p projects/$$name && \
	cp -r templates/$${template:-electron-react}/* projects/$$name/ && \
	echo "$(GREEN)✅ Проект $$name создан из шаблона $${template:-electron-react}$(NC)"

.PHONY: new-project
new-project: ## Создать новый проект вручную
	@read -p "Название проекта: " name; \
	mkdir -p projects/$$name/{src,tests,docs,assets} && \
	echo "# $$name" > projects/$$name/README.md && \
	echo "$(GREEN)✅ Проект $$name создан$(NC)"
