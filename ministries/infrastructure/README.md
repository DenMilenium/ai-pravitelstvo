# 🔧 Министерство Инфраструктуры

> *"Надёжный фундамент для всего"*

## 🎯 Миссия

Поддержание и развитие инфраструктуры: CI/CD, мониторинг, безопасность, DevOps практики.

## 🛠️ Зоны ответственности

### CI/CD
- GitHub Actions workflows
- Автоматическое тестирование
- Автоматические релизы

### Мониторинг
- Prometheus + Grafana
- Логирование (ELK/Loki)
- Алертинг

### Безопасность
- Security scanning
- Secret management
- Аудит зависимостей

### Облако
- Terraform конфигурации
- Kubernetes кластеры
- Базы данных

## 📁 Структура

```
ministries/infrastructure/
├── 📁 terraform/          # IaC
│   ├── modules/
│   ├── staging/
│   └── production/
├── 📁 kubernetes/         # K8s манифесты
│   ├── base/
│   └── overlays/
├── 📁 ci-cd/              # CI/CD конфиги
│   ├── github-actions/
│   └── gitlab-ci/
├── 📁 monitoring/         # Мониторинг
│   ├── prometheus/
│   └── grafana/
└── 📁 security/           # Безопасность
    ├── policies/
    └── scans/
```

---

**🏛️ Возврат в [Кабинет Министров](../../README.md)**
