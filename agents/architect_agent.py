#!/usr/bin/env python3
"""
🏗️ Architect-Agent
System Architect агент

Создаёт:
- Архитектурные диаграммы (PlantUML/Mermaid)
- Технические спецификации
- Выбор технологий
- C4 модели
"""

import argparse
from pathlib import Path
from typing import Dict


class ArchitectAgent:
    """
    🏗️ Architect-Agent
    
    Специализация: System Architecture
    Экспертиза: C4 Model, Microservices, Cloud Native, Patterns
    """
    
    NAME = "🏗️ Architect-Agent"
    ROLE = "System Architect"
    EXPERTISE = ["System Design", "Microservices", "Cloud Native", "C4 Model", "Patterns"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        request_lower = request.lower()
        files = {}
        
        if "архитектура" in request_lower or "architecture" in request_lower:
            files = self._generate_c4_model(request)
        elif "технологии" in request_lower or "stack" in request_lower:
            files = self._generate_tech_stack(request)
        elif "diagram" in request_lower or "диаграмма" in request_lower:
            files = self._generate_diagram(request)
        elif "adr" in request_lower or "decision" in request_lower:
            files = self._generate_adr(request)
        else:
            files = self._generate_c4_model(request)
        
        return files
    
    def _generate_c4_model(self, system: str) -> Dict[str, str]:
        files = {}
        
        files["C4_MODEL.md"] = f"""# 🏗️ C4 Architecture Model: {system}

**Created by:** Architect-Agent  
**Notation:** C4 Model (Simon Brown)

---

## Level 1: System Context

```mermaid
C4Context
    title System Context Diagram for {system}
    
    Person(user, "User", "End user of the system")
    Person(admin, "Admin", "System administrator")
    
    System({system.lower().replace(' ', '_')}, "{system}", "Main application")
    
    System_Ext(api, "External API", "Third-party services")
    System_Ext(db, "Database", "Data persistence")
    System_Ext(email, "Email Service", "Notifications")
    
    Rel(user, {system.lower().replace(' ', '_')}, "Uses", "HTTPS")
    Rel(admin, {system.lower().replace(' ', '_')}, "Manages", "HTTPS")
    Rel({system.lower().replace(' ', '_')}, api, "Calls", "REST/JSON")
    Rel({system.lower().replace(' ', '_')}, db, "Reads/Writes", "SQL")
    Rel({system.lower().replace(' ', '_')}, email, "Sends", "SMTP")
```

---

## Level 2: Containers

```mermaid
C4Container
    title Container Diagram for {system}
    
    Person(user, "User", "End user")
    
    Container_Boundary(c1, "{system}") {{
        Container(web_app, "Web Application", "React", "User interface")
        Container(api, "API Application", "Go/Python", "Business logic")
        Container(worker, "Background Worker", "Python", "Async processing")
        ContainerDb(db, "Database", "PostgreSQL", "Stores data")
        Container(cache, "Cache", "Redis", "Caching layer")
    }}
    
    System_Ext(ext_api, "External API", "Third-party")
    
    Rel(user, web_app, "Uses", "HTTPS")
    Rel(web_app, api, "Calls", "REST/JSON")
    Rel(api, db, "Reads/Writes", "SQL")
    Rel(api, cache, "Caches", "Redis protocol")
    Rel(api, worker, "Queues", "Message queue")
    Rel(worker, ext_api, "Calls", "REST")
```

---

## Level 3: Components

```mermaid
C4Component
    title Component Diagram - API Application
    
    Container_Boundary(api, "API Application") {{
        Component(controller, "Controllers", "Gin/FastAPI", "HTTP handlers")
        Component(service, "Services", "Business logic", "Core operations")
        Component(repo, "Repositories", "Data access", "DB abstraction")
        Component(auth, "Auth Service", "JWT/OAuth", "Authentication")
        Component(validator, "Validators", "Validation", "Input validation")
    }}
    
    ContainerDb(db, "Database", "PostgreSQL")
    
    Rel(controller, validator, "Validates")
    Rel(controller, auth, "Authenticates")
    Rel(controller, service, "Uses")
    Rel(service, repo, "Uses")
    Rel(repo, db, "Reads/Writes")
```

---

## Level 4: Code

See source code in:
- `/internal/handlers/` - Controllers
- `/internal/services/` - Business logic
- `/internal/repositories/` - Data access

---

## Deployment Diagram

```mermaid
C4Deployment
    title Deployment Diagram
    
    Deployment_Node(client, "Client Device", "Browser/Mobile") {{
        Container(web, "Web App", "React")
    }}
    
    Deployment_Node(cloud, "Cloud Provider", "AWS/GCP/Azure") {{
        Deployment_Node(k8s, "Kubernetes Cluster") {{
            Deployment_Node(services, "Services") {{
                Container(api1, "API Pod 1", "Go")
                Container(api2, "API Pod 2", "Go")
                Container(worker1, "Worker Pod", "Python")
            }}
        }}
        
        Deployment_Node(data, "Data Layer") {{
            ContainerDb(db, "RDS/Cloud SQL", "PostgreSQL")
            Container(cache, "MemoryStore", "Redis")
        }}
        
        Deployment_Node(lb, "Load Balancer", "ALB/Nginx") {{
        }}
    }}
    
    Rel(client, lb, "HTTPS")
    Rel(lb, api1, "Routes")
    Rel(lb, api2, "Routes")
    Rel(api1, db, "SQL")
    Rel(api1, cache, "Redis")
```
"""
        
        return files
    
    def _generate_tech_stack(self, project: str) -> Dict[str, str]:
        files = {}
        
        files["TECH_STACK.md"] = f"""# 🛠️ Technology Stack: {project}

**Architect:** Architect-Agent  
**Date:** 2024

---

## Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React 18 + TypeScript | UI |
| Backend | Go 1.21 (Gin) | API |
| Database | PostgreSQL 15 | Primary storage |
| Cache | Redis 7 | Caching |
| Queue | RabbitMQ | Async processing |
| Search | Elasticsearch | Full-text search |
| Monitoring | Prometheus + Grafana | Metrics |
| Logging | ELK Stack | Centralized logs |
| CI/CD | GitHub Actions | Automation |
| Infrastructure | Kubernetes | Orchestration |
| Cloud | AWS/GCP | Hosting |

---

## Frontend

### Core
- **Framework:** React 18
- **Language:** TypeScript 5
- **Build:** Vite 5
- **State:** Zustand / Redux Toolkit
- **Query:** TanStack Query (React Query)

### UI
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui + Radix
- **Icons:** Lucide React
- **Charts:** Recharts

### Testing
- **Unit:** Vitest
- **E2E:** Playwright
- **Visual:** Storybook

---

## Backend

### Core
- **Language:** Go 1.21
- **Framework:** Gin
- **ORM:** GORM
- **Validation:** go-playground/validator

### Services
- **Auth:** JWT + OAuth2
- **API:** REST + GraphQL
- **Documentation:** Swagger/OpenAPI
- **Rate Limiting:** Tollbooth

### Testing
- **Unit:** testing + testify
- **Integration:** dockertest
- **Mock:** mockery

---

## Database

### Primary
- **Engine:** PostgreSQL 15
- **Migrations:** golang-migrate
- **Backup:** pg_dump + WAL archiving

### Cache
- **Engine:** Redis 7
- **Client:** go-redis
- **Use cases:** Sessions, Rate limiting, Hot data

### Search
- **Engine:** Elasticsearch 8
- **Client:** olivere/elastic

---

## Infrastructure

### Containers
- **Runtime:** Docker
- **Orchestration:** Kubernetes
- **Registry:** ECR/GCR

### Cloud
- **Provider:** AWS/GCP
- **Compute:** EKS/GKE
- **Database:** RDS/Cloud SQL
- **Cache:** ElastiCache/Memorystore
- **Storage:** S3/Cloud Storage
- **CDN:** CloudFront/Cloud CDN

### Networking
- **Ingress:** Nginx Ingress
- **Service Mesh:** Istio (optional)
- **DNS:** Route53/Cloud DNS

---

## DevOps

### CI/CD
- **Platform:** GitHub Actions
- **Build:** Docker multi-stage
- **Deploy:** ArgoCD
- **Testing:** Automated in pipeline

### Monitoring
- **Metrics:** Prometheus
- **Visualization:** Grafana
- **Alerting:** Alertmanager → PagerDuty
- **Tracing:** Jaeger

### Logging
- **Collection:** Fluentd
- **Storage:** Elasticsearch
- **Visualization:** Kibana

---

## Security

- **Secrets:** AWS Secrets Manager / Vault
- **Scanning:** Trivy, Snyk
- **WAF:** AWS WAF / Cloud Armor
- **DDoS:** CloudFlare / AWS Shield

---

## Decision Log

| Decision | Alternatives | Rationale | Date |
|----------|--------------|-----------|------|
| Go vs Python | Python, Node.js | Performance, type safety | 2024-01 |
| PostgreSQL | MySQL, MongoDB | ACID, JSON support | 2024-01 |
| Kubernetes | ECS, VMs | Portability, ecosystem | 2024-01 |
"""
        
        return files
    
    def _generate_adr(self, decision: str) -> Dict[str, str]:
        files = {}
        
        files["ADR-001-architecture.md"] = f"""# ADR-001: Architecture Decision for {decision}

**Status:** Accepted  
**Date:** 2024-01-01  
**Deciders:** Architect-Agent

---

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing or have agreed to implement?

## Consequences

What becomes easier or more difficult to do because of this change?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2

### Risks
- Risk 1
- Mitigation: [how we'll handle it]

## Alternatives Considered

### Alternative 1: [Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

### Alternative 2: [Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

## References
- [Link 1]
- [Link 2]
"""
        
        return files
    
    def _generate_diagram(self, system: str) -> Dict[str, str]:
        return self._generate_c4_model(system)


def main():
    parser = argparse.ArgumentParser(description="🏗️ Architect-Agent — System Architect")
    parser.add_argument("request", nargs="?", help="Что спроектировать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = ArchitectAgent()
    
    if args.request:
        print(f"🏗️ {agent.NAME} проектирует: {args.request}")
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
                print(content)
    else:
        print(f"🏗️ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
