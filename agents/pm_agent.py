#!/usr/bin/env python3
"""
📊 PM-Agent
Product Manager агент

Создаёт:
- Product Requirements Document (PRD)
- User Stories
- Roadmap
- Приоритизацию фич
"""

import argparse
from pathlib import Path
from typing import Dict, List
from datetime import datetime, timedelta


class PMAgent:
    """
    📊 PM-Agent
    
    Специализация: Product Management
    Инструменты: PRD, User Stories, Roadmap, Prioritization
    """
    
    NAME = "📊 PM-Agent"
    ROLE = "Product Manager"
    EXPERTISE = ["Product Strategy", "User Stories", "Roadmapping", "Prioritization", "Metrics"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        """Обработка запроса продакт менеджера"""
        request_lower = request.lower()
        files = {}
        
        if "prd" in request_lower or "тз" in request_lower or "требования" in request_lower:
            files = self._generate_prd(request)
        elif "story" in request_lower or "истори" in request_lower:
            files = self._generate_user_stories(request)
        elif "roadmap" in request_lower or "дорожная" in request_lower:
            files = self._generate_roadmap(request)
        elif "mvp" in request_lower:
            files = self._generate_mvp(request)
        elif "приоритет" in request_lower or "priority" in request_lower:
            files = self._generate_prioritization(request)
        else:
            files = self._generate_prd(request)
        
        return files
    
    def _generate_prd(self, feature: str) -> Dict[str, str]:
        """Генерация Product Requirements Document"""
        files = {}
        
        files["PRD.md"] = f"""# 📋 Product Requirements Document

## {feature}

**Version:** 1.0  
**Author:** PM-Agent  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** Draft

---

## 1. Overview

### 1.1 Background
[Контекст и обоснование фичи]

### 1.2 Goals
- Цель 1: [Основная цель]
- Цель 2: [Вторичная цель]
- Цель 3: [Метрика успеха]

### 1.3 Non-Goals
- [Что НЕ входит в scope]
- [Что отложено на потом]

---

## 2. User Stories

### 2.1 User Personas

**Primary User:** [Кто основной пользователь]
- Демография: [Возраст, профессия]
- Проблема: [Какая боль]
- Цель: [Что хочет достичь]

### 2.2 User Stories

#### US-001: Базовая функциональность
```
Как [роль],
Я хочу [действие],
Чтобы [ценность/результат]
```

**Acceptance Criteria:**
- [ ] Критерий 1
- [ ] Критерий 2
- [ ] Критерий 3

**Priority:** P0 (Critical)  
**Estimate:** 3 story points

#### US-002: Расширенная функциональность
```
Как [роль],
Я хочу [действие],
Чтобы [ценность/результат]
```

**Acceptance Criteria:**
- [ ] Критерий 1
- [ ] Критерий 2

**Priority:** P1 (High)  
**Estimate:** 5 story points

#### US-003: Дополнительно
```
Как [роль],
Я хочу [действие],
Чтобы [ценность/результат]
```

**Priority:** P2 (Medium)  
**Estimate:** 2 story points

---

## 3. Functional Requirements

### FR-001: [Название функции]
**Priority:** P0

**Description:** [Описание]

**Inputs:**
- [Входные данные]

**Outputs:**
- [Выходные данные]

**Validation:**
- [Правила валидации]

### FR-002: [Название функции]
**Priority:** P1

[...]

---

## 4. Non-Functional Requirements

### 4.1 Performance
- Response time: < 200ms (p95)
- Throughput: > 1000 RPS
- Availability: 99.9%

### 4.2 Security
- Authentication: JWT
- Authorization: RBAC
- Data encryption: AES-256

### 4.3 Scalability
- Horizontal scaling supported
- Stateless design
- Caching strategy

### 4.4 Monitoring
- Metrics: Prometheus
- Logging: Structured JSON
- Alerting: PagerDuty

---

## 5. UI/UX Requirements

### 5.1 Wireframes
[Ссылки на макеты]

### 5.2 Design System
- Theme: [Dark/Light]
- Components: [Библиотека]
- Responsive: [Breakpoints]

### 5.3 Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support

---

## 6. API Requirements

### 6.1 Endpoints

#### POST /api/v1/resource
**Description:** [Описание]

**Request:**
```json
{{
  "field1": "value1",
  "field2": "value2"
}}
```

**Response:**
```json
{{
  "id": "uuid",
  "status": "success",
  "data": {{}}
}}
```

**Errors:**
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found

---

## 7. Success Metrics

### 7.1 Primary Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Adoption | 50% | Users using feature |
| Retention | 80% | Users returning |
| Error Rate | < 1% | Failed operations |

### 7.2 Secondary Metrics
- NPS score
- Time to complete task
- Support tickets

---

## 8. Open Questions

1. [Вопрос 1]
2. [Вопрос 2]
3. [Вопрос 3]

---

## 9. Appendix

### 9.1 References
- [Документ 1]
- [Документ 2]

### 9.2 Changelog
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | {datetime.now().strftime('%Y-%m-%d')} | Initial draft | PM-Agent |

---

**Approvals:**
- [ ] Product Manager
- [ ] Tech Lead
- [ ] Design Lead
- [ ] Stakeholder
"""
        return files
    
    def _generate_user_stories(self, feature: str) -> Dict[str, str]:
        """Генерация User Stories"""
        files = {}
        
        files["USER_STORIES.md"] = f"""# 📝 User Stories: {feature}

**Created by:** PM-Agent  
**Date:** {datetime.now().strftime('%Y-%m-%d')}

---

## Story Mapping

```
RELEASE 1 (MVP)                    RELEASE 2                  RELEASE 3
┌─────────────┐                   ┌─────────────┐           ┌─────────────┐
│   Epic 1    │                   │   Epic 3    │           │   Epic 5    │
├─────────────┤                   ├─────────────┤           ├─────────────┤
│ Story 1.1   │  ───────────────> │ Story 3.1   │  ─────>   │ Story 5.1   │
│ Story 1.2   │                   │ Story 3.2   │           │ Story 5.2   │
│ Story 1.3   │                   └─────────────┘           └─────────────┘
└─────────────┘
       │
       ▼
┌─────────────┐
│   Epic 2    │
├─────────────┤
│ Story 2.1   │
│ Story 2.2   │
└─────────────┘
```

---

## Detailed Stories

### Epic 1: [Название эпика]

#### Story 1.1: [Название истории]
```
Как [пользователь],
Я хочу [действие],
Чтобы [результат]
```

**Acceptance Criteria:**
```gherkin
Given [контекст]
When [действие]
Then [результат]
```

**Priority:** P0  
**Estimate:** 3 SP  
**Dependencies:** None

---

#### Story 1.2: [Название истории]
```
Как [пользователь],
Я хочу [действие],
Чтобы [результат]
```

**Acceptance Criteria:**
- [ ] Критерий 1
- [ ] Критерий 2

**Priority:** P1  
**Estimate:** 5 SP

---

## Definition of Ready

- [ ] Story has clear acceptance criteria
- [ ] Story is estimated
- [ ] Story has no unresolved dependencies
- [ ] Story is small enough (max 8 SP)
- [ ] UX/UI designs attached (if needed)

## Definition of Done

- [ ] Code implemented
- [ ] Unit tests written (coverage > 80%)
- [ ] Integration tests pass
- [ ] Code reviewed
- [ ] QA approved
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PO acceptance

---

## Sprint Planning

### Sprint 1
| Story | Points | Assignee | Status |
|-------|--------|----------|--------|
| US-001 | 3 | Dev 1 | ⬜ |
| US-002 | 5 | Dev 2 | ⬜ |
| **Total** | **8** | | |

### Sprint 2
| Story | Points | Assignee | Status |
|-------|--------|----------|--------|
| US-003 | 3 | Dev 1 | ⬜ |
| US-004 | 2 | Dev 3 | ⬜ |
| **Total** | **5** | | |
"""
        return files
    
    def _generate_roadmap(self, product: str) -> Dict[str, str]:
        """Генерация Roadmap"""
        files = {}
        
        now = datetime.now()
        q1 = now.strftime('%Y-%m')
        q2 = (now + timedelta(days=90)).strftime('%Y-%m')
        q3 = (now + timedelta(days=180)).strftime('%Y-%m')
        q4 = (now + timedelta(days=270)).strftime('%Y-%m')
        
        files["ROADMAP.md"] = f"""# 🗺️ Product Roadmap: {product}

**Created by:** PM-Agent  
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Timeline

```
{q1}        {q2}        {q3}        {q4}
  │           │           │           │
  ▼           ▼           ▼           ▼
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│ NOW │    │ Q2  │    │ Q3  │    │ Q4  │
└──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘
   │          │          │          │
   ▼          ▼          ▼          ▼
[MVP]    [Growth]  [Scale]   [Optimize]
```

---

## Phase 1: MVP ({q1})
**Theme:** Core functionality
**Goal:** Launch basic product

### Key Features
- [ ] Feature 1: [Описание]
- [ ] Feature 2: [Описание]
- [ ] Feature 3: [Описание]

### Success Metrics
- 100 users
- < 1% error rate
- Basic functionality working

---

## Phase 2: Growth ({q2})
**Theme:** User acquisition
**Goal:** Scale user base

### Key Features
- [ ] Feature 4: [Описание]
- [ ] Feature 5: [Описание]
- [ ] Integrations

### Success Metrics
- 1000 users
- 20% MoM growth
- NPS > 40

---

## Phase 3: Scale ({q3})
**Theme:** Enterprise readiness
**Goal:** Support larger customers

### Key Features
- [ ] SSO
- [ ] Advanced analytics
- [ ] API access

### Success Metrics
- 10 enterprise customers
- $10K MRR
- 99.9% uptime

---

## Phase 4: Optimize ({q4})
**Theme:** Efficiency & AI
**Goal:** Automated operations

### Key Features
- [ ] AI-powered features
- [ ] Performance optimization
- [ ] Self-service

### Success Metrics
- Automated 50% of operations
- CAC reduced by 30%

---

## Now / Next / Later

### 🔴 Now (This Quarter)
| Feature | Priority | Owner | Status |
|---------|----------|-------|--------|
| [Feature 1] | P0 | Team A | 🟡 |
| [Feature 2] | P0 | Team B | ⬜ |

### 🟡 Next (Next Quarter)
| Feature | Priority | Owner |
|---------|----------|-------|
| [Feature 3] | P1 | Team A |
| [Feature 4] | P1 | Team C |

### 🟢 Later (Future)
| Feature | Priority |
|---------|----------|
| [Feature 5] | P2 |
| [Feature 6] | P3 |

---

## Dependencies

```
[Feature A] ───────┐
                   ├──▶ [Feature C]
[Feature B] ───────┘
```

---

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Resource constraints | High | Medium | Hire contractors |
| Technical complexity | Medium | Low | Spike stories |
| Market changes | High | Low | Stay agile |

---

*Roadmap is subject to change based on market feedback and business priorities.*
"""
        return files
    
    def _generate_mvp(self, product: str) -> Dict[str, str]:
        """Генерация MVP scope"""
        files = {}
        
        files["MVP.md"] = f"""# 🚀 MVP Scope: {product}

**Created by:** PM-Agent  
**Goal:** Launch minimal viable product in 4 weeks

---

## Must Have (P0)

### Feature 1: [Core Feature]
**Why:** Without this product has no value  
**What:** [Description]  
**How:** [Implementation approach]

**Acceptance Criteria:**
- [ ] User can [action]
- [ ] System [response]
- [ ] Data [persisted]

### Feature 2: [Core Feature]
...

## Should Have (P1)

### Feature 3: [Important Feature]
**Why:** Significantly improves UX  
**What:** [Description]

## Won't Have (P2+)

- [Feature X] - Too complex for MVP
- [Feature Y] - Can be added later
- [Feature Z] - Low priority

---

## MVP Success Criteria

1. **Functional:** All P0 features work
2. **Stable:** < 1% crash rate
3. **Usable:** 5 users complete core flow
4. **Measurable:** Analytics in place

---

## Post-MVP Feedback Loop

```
Week 1-2:  User interviews
     ↓
Week 3-4:  Iterate based on feedback
     ↓
Week 5-6:  Plan v1.1
```
"""
        return files
    
    def _generate_prioritization(self, feature: str) -> Dict[str, str]:
        """Генерация приоритизации"""
        files = {}
        
        files["PRIORITIZATION.md"] = f"""# 📊 Feature Prioritization: {feature}

**Method:** RICE (Reach × Impact × Confidence / Effort)

---

## RICE Score Matrix

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Feature A | 1000 | 3 | 80% | 5 | 480 |
| Feature B | 500 | 2 | 90% | 2 | 450 |
| Feature C | 2000 | 1 | 70% | 10 | 140 |
| Feature D | 300 | 3 | 100% | 3 | 300 |

---

## Prioritization Framework

### MoSCoW Method

#### Must Have
- [ ] Feature A (RICE: 480)
- [ ] Feature B (RICE: 450)

#### Should Have
- [ ] Feature D (RICE: 300)

#### Could Have
- [ ] Feature C (RICE: 140)

#### Won't Have
- [ ] Feature E (RICE: 50)
- [ ] Feature F (RICE: 30)

---

## Impact vs Effort Matrix

```
        Low Effort    High Effort
        ┌─────────────┬─────────────┐
High    │  Quick Wins │  Big Bets   │
Impact  │  (Do First) │  (Plan)     │
        ├─────────────┼─────────────┤
Low     │  Fill-ins   │  Avoid      │
Impact  │  (Maybe)    │  (Don't)    │
        └─────────────┴─────────────┘
```

---

## Priority Queue

### P0 - Critical (This Sprint)
1. [Feature A]
2. [Feature B]

### P1 - High (Next 2 Sprints)
3. [Feature D]
4. [Feature C]

### P2 - Medium (Next Quarter)
5. [Feature E]

### P3 - Low (Backlog)
6. [Feature F]
"""
        return files


def main():
    parser = argparse.ArgumentParser(description="📊 PM-Agent — Product Manager")
    parser.add_argument("request", nargs="?", help="Что нужно спланировать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = PMAgent()
    
    if args.request:
        print(f"📊 {agent.NAME} создаёт: {args.request}")
        print("-" * 50)
        
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
            
            print(f"\n📁 Сохранено в: {output_dir}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:800] + "..." if len(content) > 800 else content)
    else:
        print(f"📊 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"Экспертиза: {', '.join(agent.EXPERTISE)}")
        print("\nПримеры:")
        print('  python pm_agent.py "PRD для чата"')
        print('  python pm_agent.py "User stories"')
        print('  python pm_agent.py "Roadmap на год"')


if __name__ == "__main__":
    main()
