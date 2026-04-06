# CloudMind

Облачная AI-платформа для развёртывания и управления ML-моделями.

## 🚀 Архитектура

```
CloudMind/
├── api/                   # API Gateway (Go)
├── web/                   # Web UI (React + TS)
├── core/                  # Core Services (Go)
├── worker/                # ML Workers (Python)
├── infra/                 # Инфраструктура
└── docs/                  # Документация
```

## ⚡ Быстрый старт

```bash
# Локальный запуск
docker-compose up

# Деплой
make deploy ENV=production
```

## 📚 Документация API

[OpenAPI Spec](./api/openapi.yaml)
