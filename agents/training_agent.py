#!/usr/bin/env python3
"""
🎓 Training-Agent
Learning & Development Specialist

Обучение, развитие, тренинги, knowledge base.
"""

import argparse
from pathlib import Path
from typing import Dict


class TrainingAgent:
    """
    🎓 Training-Agent
    
    Специализация: Learning & Development
    Задачи: Training, Skill Development, Knowledge Management
    """
    
    NAME = "🎓 Training-Agent"
    ROLE = "L&D Specialist"
    EXPERTISE = ["Training", "Skill Development", "eLearning", "Knowledge Base"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "training-plan.md": self._generate_training_plan(),
            "skill-matrix.md": self._generate_skill_matrix(),
            "workshop-outline.md": self._generate_workshop(),
            "knowledge-base.md": self._generate_knowledge_base()
        }
    
    def _generate_training_plan(self) -> str:
        return '''# Employee Training Plan

## Overview
**Employee**: [Name]
**Role**: [Position]
**Start Date**: [Date]
**Plan Duration**: 90 days

---

## 🎯 Training Objectives

### Short-term (Month 1)
- [ ] Understand company products/services
- [ ] Learn internal tools and systems
- [ ] Complete compliance training
- [ ] Shadow team members

### Medium-term (Month 2-3)
- [ ] Technical skill development
- [ ] Soft skills training
- [ ] Cross-functional collaboration
- [ ] Project participation

### Long-term (Ongoing)
- [ ] Leadership development
- [ ] Industry certifications
- [ ] Mentorship program
- [ ] Conference attendance

---

## 📚 Technical Skills Training

### Week 1-2: Fundamentals
| Topic | Format | Duration | Resources |
|-------|--------|----------|-----------|
| Company Tech Stack | Self-paced | 4 hours | Internal wiki |
| Codebase Overview | Workshop | 2 hours | Tech Lead |
| Git Workflow | Hands-on | 2 hours | Git tutorial |
| CI/CD Pipeline | Demo | 1 hour | DevOps team |

### Week 3-4: Deep Dive
| Topic | Format | Duration | Resources |
|-------|--------|----------|-----------|
| Architecture Patterns | Course | 6 hours | Pluralsight |
| Testing Best Practices | Workshop | 3 hours | QA team |
| Database Design | Course | 4 hours | Internal training |
| Security Fundamentals | Self-paced | 3 hours | Security team |

### Month 2: Advanced Topics
| Topic | Format | Duration | Resources |
|-------|--------|----------|-----------|
| Microservices | Course | 8 hours | Udemy |
| Kubernetes | Hands-on | 10 hours | K8s workshop |
| Performance Tuning | Workshop | 4 hours | Senior dev |
| Design Patterns | Course | 6 hours | Refactoring Guru |

---

## 🗣️ Soft Skills Training

### Communication
- [ ] Effective written communication
- [ ] Technical presentation skills
- [ ] Active listening
- [ ] Giving and receiving feedback

### Collaboration
- [ ] Agile methodologies
- [ ] Cross-functional teamwork
- [ ] Conflict resolution
- [ ] Remote work best practices

### Professional Development
- [ ] Time management
- [ ] Prioritization techniques
- [ ] Stress management
- [ ] Work-life balance

---

## 🎓 Learning Resources

### Internal
- [ ] Company wiki/documentation
- [ ] Internal code repositories
- [ ] Previous project post-mortems
- [ ] Lunch & learn recordings

### External
- [ ] Pluralsight subscription
- [ ] Coursera courses
- [ ] Technical books library
- [ ] Industry newsletters

### Community
- [ ] Internal Slack channels
- [ ] Tech talks and meetups
- [ ] Open source contributions
- [ ] Hackathons

---

## 📊 Assessment & Evaluation

### Knowledge Checks
| Week | Assessment | Format | Passing Score |
|------|------------|--------|---------------|
| 2 | Tech stack quiz | Online | 80% |
| 4 | Code review exercise | Practical | Pass/Fail |
| 8 | System design interview | Interview | Pass/Fail |
| 12 | Project presentation | Demo | Manager review |

### Progress Tracking
- **Week 2**: Manager check-in
- **Week 4**: Technical assessment
- **Week 8**: Mid-point review
- **Week 12**: Final evaluation

---

## 👥 Mentorship Program

### Mentor Assignment
**Mentor**: [Name]
**Role**: [Senior Position]
**Meeting Schedule**: Weekly 1:1

### Mentorship Goals
1. Technical guidance and code reviews
2. Career path discussions
3. Industry insights
4. Networking opportunities

### Mentee Responsibilities
- Come prepared to meetings
- Ask questions
- Seek feedback
- Share progress

---

## 🏆 Certification Goals

### Year 1
- [ ] AWS Cloud Practitioner
- [ ] Company Internal Certification

### Year 2
- [ ] AWS Solutions Architect
- [ ] Certified Scrum Master (optional)

### Year 3+
- [ ] Domain-specific certifications
- [ ] Conference speaking
- [ ] Technical blog writing

---

## 📅 90-Day Training Calendar

### Month 1
| Week | Focus | Activities |
|------|-------|------------|
| 1 | Onboarding | Orientation, tools setup |
| 2 | Fundamentals | Tech stack, codebase |
| 3 | Integration | First tasks, shadowing |
| 4 | Assessment | Knowledge check |

### Month 2
| Week | Focus | Activities |
|------|-------|------------|
| 5 | Skill Building | Advanced courses |
| 6 | Project Work | Real assignments |
| 7 | Collaboration | Cross-team work |
| 8 | Review | Mid-point assessment |

### Month 3
| Week | Focus | Activities |
|------|-------|------------|
| 9 | Advanced Topics | Specialization |
| 10 | Leadership | Mentoring others |
| 11 | Innovation | Side projects |
| 12 | Evaluation | Final assessment |

---

## 💰 Training Budget

| Category | Budget | Actual | Notes |
|----------|--------|--------|-------|
| Courses | $1,000 | | Pluralsight, Udemy |
| Books | $200 | | Technical books |
| Conferences | $2,000 | | Annual budget |
| Certifications | $500 | | Exam fees |
| **Total** | **$3,700** | | |
'''
    
    def _generate_skill_matrix(self) -> str:
        return '''# Team Skill Matrix

## Legend
| Level | Description |
|-------|-------------|
| 🟢 Expert | Can teach others, go-to person |
| 🟡 Proficient | Can work independently |
| 🟠 Developing | Needs some guidance |
| 🔴 Beginner | Learning, needs support |
| ⚪ N/A | Not required for role |

---

## Engineering Team Skills

### Programming Languages
| Team Member | Python | JavaScript | Go | SQL | Rust |
|-------------|--------|------------|----|---- |------|
| Alice | 🟢 | 🟢 | 🟡 | 🟢 | 🟠 |
| Bob | 🟡 | 🟢 | 🟢 | 🟡 | ⚪ |
| Carol | 🟢 | 🟡 | 🟠 | 🟢 | 🟠 |
| David | 🟠 | 🟢 | 🟡 | 🟡 | ⚪ |
| Eve | 🟡 | 🟡 | 🟢 | 🟠 | 🟢 |

### Frontend Technologies
| Team Member | React | Vue | TypeScript | CSS | Webpack |
|-------------|-------|-----|------------|-----|---------|
| Alice | 🟢 | 🟠 | 🟢 | 🟡 | 🟡 |
| Bob | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 |
| Carol | 🟡 | ⚪ | 🟡 | 🟢 | 🟠 |
| David | 🟢 | 🟡 | 🟢 | 🟡 | 🟢 |
| Eve | 🟠 | ⚪ | 🟡 | 🟠 | ⚪ |

### Backend & Infrastructure
| Team Member | Node.js | Django | K8s | AWS | Docker |
|-------------|---------|--------|-----|-----|--------|
| Alice | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 |
| Bob | 🟢 | ⚪ | 🟢 | 🟡 | 🟢 |
| Carol | 🟡 | 🟢 | 🟠 | 🟡 | 🟡 |
| David | 🟢 | ⚪ | 🟡 | 🟠 | 🟡 |
| Eve | 🟠 | ⚪ | 🟢 | 🟢 | 🟢 |

### Soft Skills
| Team Member | Communication | Leadership | Mentoring | Presentation |
|-------------|---------------|------------|-----------|--------------|
| Alice | 🟢 | 🟢 | 🟢 | 🟡 |
| Bob | 🟡 | 🟡 | 🟡 | 🟢 |
| Carol | 🟢 | 🟡 | 🟠 | 🟡 |
| David | 🟡 | 🟠 | 🟠 | 🟠 |
| Eve | 🟢 | 🟢 | 🟡 | 🟢 |

---

## Skill Gap Analysis

### Critical Skills (Need More Coverage)
| Skill | Current Coverage | Target | Action |
|-------|-----------------|--------|--------|
| Kubernetes | 40% | 80% | Training needed |
| Rust | 20% | 40% | Hire or train |
| AWS | 60% | 100% | Certifications |
| Technical Writing | 20% | 60% | Workshop |

### Individual Development Plans

#### Alice
**Strengths**: Python, React, AWS
**Gaps**: Rust, Public speaking
**Plan**: 
- Rust course (Q2)
- Conference speaking (Q3)

#### Bob
**Strengths**: Full-stack JavaScript, Go
**Gaps**: Python, Leadership
**Plan**:
- Python bootcamp (Q2)
- Leadership training (Q3)

#### Carol
**Strengths**: Python, SQL, CSS
**Gaps**: Kubernetes, Frontend frameworks
**Plan**:
- K8s certification (Q2)
- Advanced React (Q3)

---

## Training Needs by Skill

### High Priority
**Kubernetes**
- Who needs it: Alice, Carol, David
- Training: K8s workshop (2 days)
- Budget: $2,000

**AWS Advanced**
- Who needs it: Bob, Carol, David
- Training: Solutions Architect prep
- Budget: $1,500

### Medium Priority
**Rust Programming**
- Who needs it: Alice, Carol
- Training: Rust book + project
- Budget: $500

**Technical Writing**
- Who needs it: All
- Training: Workshop + practice
- Budget: $1,000

---

## Career Progression Paths

### Individual Contributor Track
```
Junior → Mid → Senior → Staff → Principal
  🟠      🟡      🟢       🟢        🟢
```

**Senior Developer Requirements**:
- 3+ technologies at 🟢 level
- 2+ areas at 🟢 level
- Mentoring experience

### Management Track
```
Developer → Tech Lead → Engineering Manager → Director
    🟡          🟢              🟢                  🟢
```

**Tech Lead Requirements**:
- Technical expertise (multiple 🟢)
- Communication 🟢
- Leadership 🟡

---

## Team Capability Heatmap

```
                    Expertise Level
              Low ◄─────────────────► High
              0    25    50    75   100
              
Frontend      ████████░░░░░░░░░░░░  40%
Backend       ████████████░░░░░░░░  60%
DevOps        ██████░░░░░░░░░░░░░░  30%
Data/ML       ██████████░░░░░░░░░░  50%
Mobile        ████░░░░░░░░░░░░░░░░  20%
Security      ██████░░░░░░░░░░░░░░  30%
```

**Recommendations**:
- Hire: DevOps Engineer, Mobile Developer
- Train: Existing team in DevOps
- Priority: Backend scaling
'''
    
    def _generate_workshop(self) -> str:
        return '''# Workshop: Clean Code Best Practices

## Overview
**Duration**: 4 hours
**Format**: Interactive workshop
**Audience**: Software developers
**Prerequisites**: Basic programming knowledge

---

## 🎯 Learning Objectives

By the end of this workshop, participants will be able to:
1. Identify code smells in existing code
2. Apply refactoring techniques to improve code quality
3. Write meaningful names and comments
4. Create functions that follow SRP
5. Apply SOLID principles in practice

---

## 📋 Agenda

### Part 1: Introduction (30 min)
**9:00 - 9:30**

- Welcome and icebreaker (10 min)
- Workshop objectives (5 min)
- Code quality importance (10 min)
- Agenda overview (5 min)

**Materials**: Slides, handouts

---

### Part 2: Naming (45 min)
**9:30 - 10:15**

#### Theory (15 min)
- Why naming matters
- Rules for meaningful names
- Common anti-patterns

#### Exercise: Rename This (20 min)
```python
# Bad example
def calc(d):
    return d * 0.05

# Participants refactor to:
def calculate_tax(amount):
    TAX_RATE = 0.05
    return amount * TAX_RATE
```

#### Discussion (10 min)
- Share solutions
- Discuss trade-offs

---

### Part 3: Functions (45 min)
**10:15 - 11:00**

#### Theory (15 min)
- Function size guidelines
- Single Responsibility Principle
- Parameters best practices

#### Exercise: Function Refactoring (25 min)
```python
# Bad example
def process_user_data(user):
    # 50 lines of code doing:
    # - Validation
    # - Database operations
    # - Email sending
    # - Logging
    pass

# Refactor into:
def validate_user(user)
def save_user(user)
def send_welcome_email(user)
def log_user_creation(user)
```

#### Break (15 min)
**11:00 - 11:15**

---

### Part 4: Code Smells (45 min)
**11:15 - 12:00**

#### Theory (15 min)
Common code smells:
- Long method
- Large class
- Duplicated code
- Feature envy
- Shotgun surgery

#### Exercise: Spot the Smell (20 min)
Present code examples, participants identify smells.

```python
# Example 1: Long method
def handle_request(request):
    # 100 lines of code...
    pass

# Example 2: Duplicated code
def calculate_price_a(order):
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * 0.1
    return subtotal + tax

def calculate_price_b(order):
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * 0.1
    return subtotal + tax + 5  # Only difference!
```

#### Discussion (10 min)

---

### Part 5: SOLID Principles (45 min)
**12:00 - 12:45**

#### Theory (20 min)
- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

#### Exercise: Apply SOLID (20 min)
Refactor a messy class to follow SOLID principles.

```python
# Before: Violates multiple principles
class Employee:
    def calculate_pay(self): pass
    def save_to_database(self): pass
    def generate_report(self): pass
    def send_email(self): pass

# After: Separated concerns
class Employee:
    def calculate_pay(self): pass

class EmployeeRepository:
    def save(self, employee): pass

class EmployeeReport:
    def generate(self, employee): pass
```

#### Wrap-up (5 min)

---

### Part 6: Hands-on Lab (60 min)
**12:45 - 13:45**

#### Challenge: Refactor Legacy Code

Participants receive a real (anonymized) codebase with:
- 5+ code smells
- Poor naming
- Long functions
- Tight coupling

**Tasks**:
1. Identify issues (15 min)
2. Plan refactoring (15 min)
3. Implement changes (30 min)

#### Code Review (15 min)
- Pair up and review
- Share learnings

---

### Part 7: Closing (15 min)
**13:45 - 14:00**

- Recap key takeaways (5 min)
- Q&A (5 min)
- Resources and next steps (5 min)

---

## 🛠️ Materials Needed

### For Instructor
- [ ] Projector and screen
- [ ] Whiteboard and markers
- [ ] Slide deck
- [ ] Code examples repository
- [ ] Timer

### For Participants
- [ ] Laptop with IDE
- [ ] Access to code repository
- [ ] Notebook and pen
- [ ] Handouts (cheat sheets)

### Digital Resources
- [ ] GitHub repo with examples
- [ ] Refactoring catalog reference
- [ ] Clean Code book (optional)

---

## 📊 Assessment

### Knowledge Check (5 questions)
1. What makes a good function name?
2. How many parameters should a function ideally have?
3. What is the Single Responsibility Principle?
4. Name 3 code smells.
5. When should you add a comment?

### Practical Assessment
- Submit refactored code
- Peer review another participant's work

### Success Criteria
- 80% pass rate on knowledge check
- Code review approval from instructor

---

## 🎁 Takeaways

### Cheat Sheet: Clean Code Checklist
- [ ] Names reveal intent
- [ ] Functions do one thing
- [ ] No side effects
- [ ] DRY (Don't Repeat Yourself)
- [ ] Comments explain "why", not "what"
- [ ] Small classes with single purpose
- [ ] Proper error handling

### Resources
- Clean Code by Robert C. Martin
- Refactoring.guru website
- Company's coding standards
- Internal code review guidelines

---

## 📈 Follow-up

### Week 1: Practice
- Apply learnings to real work
- Request code review with focus on clean code

### Week 2: Reinforcement
- Lunch & learn: Share experience
- Present before/after examples

### Month 1: Measurement
- Track code review comments
- Monitor code quality metrics
- Gather feedback
'''
    
    def _generate_knowledge_base(self) -> str:
        return '''# Internal Knowledge Base

## 🏠 Home

Welcome to the Company Knowledge Base! 
Find documentation, guides, and resources here.

### Quick Links
- [Engineering Handbook](#)
- [Onboarding Guide](#)
- [API Documentation](#)
- [Runbooks](#)
- [FAQs](#)

---

## 📚 Engineering

### Getting Started
- [Development Environment Setup](engineering/setup.md)
- [First Day Checklist](engineering/first-day.md)
- [Coding Standards](engineering/standards.md)
- [Git Workflow](engineering/git.md)

### Architecture
- [System Overview](engineering/architecture/overview.md)
- [Service Dependencies](engineering/architecture/services.md)
- [Data Flow Diagrams](engineering/architecture/data-flow.md)
- [Technology Stack](engineering/architecture/stack.md)

### Development
- [Local Development](engineering/dev/local.md)
- [Testing Guide](engineering/dev/testing.md)
- [Code Review Process](engineering/dev/code-review.md)
- [Debugging Tips](engineering/dev/debugging.md)

### Deployment
- [CI/CD Pipeline](engineering/deploy/cicd.md)
- [Environments](engineering/deploy/environments.md)
- [Release Process](engineering/deploy/releases.md)
- [Rollback Procedures](engineering/deploy/rollback.md)

### Operations
- [Monitoring](engineering/ops/monitoring.md)
- [Alerting](engineering/ops/alerting.md)
- [Incident Response](engineering/ops/incidents.md)
- [On-Call Runbooks](engineering/ops/runbooks.md)

---

## 🎨 Product

### Product Overview
- [Product Vision](product/vision.md)
- [Roadmap](product/roadmap.md)
- [User Personas](product/personas.md)
- [Competitive Analysis](product/competition.md)

### Design
- [Design System](product/design/system.md)
- [Component Library](product/design/components.md)
- [Style Guide](product/design/style-guide.md)
- [Accessibility Standards](product/design/a11y.md)

### Research
- [User Research](product/research/users.md)
- [Usability Testing](product/research/testing.md)
- [Analytics Dashboard](product/research/analytics.md)
- [Feature Requests](product/research/requests.md)

---

## 💼 Operations

### HR
- [Employee Handbook](ops/hr/handbook.md)
- [Benefits Guide](ops/hr/benefits.md)
- [Time Off Policy](ops/hr/time-off.md)
- [Performance Reviews](ops/hr/performance.md)

### IT
- [Equipment Policy](ops/it/equipment.md)
- [Security Guidelines](ops/it/security.md)
- [Software Access](ops/it/software.md)
- [VPN Setup](ops/it/vpn.md)

### Finance
- [Expense Policy](ops/finance/expenses.md)
- [Travel Guidelines](ops/finance/travel.md)
- [Budget Process](ops/finance/budget.md)
- [Invoice Procedures](ops/finance/invoicing.md)

---

## 🚀 Playbooks

### Incident Response
```
1. Detect → 2. Triage → 3. Mitigate → 4. Resolve → 5. Post-mortem
```

[Full Incident Response Playbook](playbooks/incident-response.md)

### Security Breach
[Security Incident Playbook](playbooks/security-breach.md)

### Customer Escalation
[Customer Escalation Playbook](playbooks/customer-escalation.md)

### Data Recovery
[Data Recovery Playbook](playbooks/data-recovery.md)

---

## 📖 How-To Guides

### Common Tasks

#### Request Time Off
1. Check your balance in [HR system]
2. Submit request at least 2 weeks in advance
3. Add to team calendar
4. Set Slack status

#### Order Equipment
1. Check approved equipment list
2. Get manager approval if >$500
3. Submit IT ticket
4. Allow 1-2 weeks for delivery

#### Access Production
1. Complete security training
2. Request access via IT ticket
3. Get manager approval
4. Access granted within 24 hours

#### Submit Expense Report
1. Keep all receipts
2. Fill expense form within 30 days
3. Attach receipts
4. Manager approval required

---

## ❓ FAQs

### Engineering

**Q: How do I get access to the staging environment?**
A: Submit an IT ticket with your public SSH key.

**Q: What's our code review policy?**
A: All code requires 2 approvals before merging.

**Q: How do I deploy to production?**
A: Use the deployment runbook and get approval from on-call.

**Q: Where do I report bugs?**
A: Create a ticket in Jira with [BUG] prefix.

### General

**Q: What are working hours?**
A: Core hours 10am-4pm, flexible otherwise.

**Q: How do I book meeting rooms?**
A: Use Google Calendar room booking.

**Q: Where can I find the WiFi password?**
A: Check the #it-help Slack channel pinned messages.

**Q: How do I update my direct deposit?**
A: Contact HR or update in [HR system].

---

## 🔍 Search Tips

### Finding Information
- Use the search bar at the top
- Browse by category in the sidebar
- Check related articles at the bottom
- Ask in #help Slack channel if not found

### Contributing
- Everyone can suggest edits
- Create PR for significant changes
- Keep documentation up to date
- Add examples and screenshots

---

## 🆘 Getting Help

### Slack Channels
- **#general** - Company-wide announcements
- **#engineering** - Engineering discussions
- **#help** - General questions
- **#it-help** - Technical issues
- **#hr** - HR-related questions

### Contacts
| Role | Name | Slack | Email |
|------|------|-------|-------|
| IT Support | @it-support | #it-help | it@company.com |
| HR | @hr-team | #hr | hr@company.com |
| Engineering Manager | @eng-manager | DMs | eng-mgr@company.com |

### Emergency
For urgent issues:
- Page on-call engineer: [PagerDuty link]
- Security incidents: security@company.com
- After-hours IT: [emergency number]

---

## 📝 Templates

### Meeting Notes
[Meeting Notes Template](templates/meeting-notes.md)

### Project Proposal
[Project Proposal Template](templates/project-proposal.md)

### Incident Report
[Incident Report Template](templates/incident-report.md)

### Post-mortem
[Post-mortem Template](templates/post-mortem.md)

---

## 📊 Stats

- **Total Articles**: 150+
- **Last Updated**: Today
- **Contributors**: 45
- **Monthly Views**: 5,000+

---

**Need to add something?** 
Create a PR or contact the #knowledge-base team.
'''


def main():
    parser = argparse.ArgumentParser(description="🎓 Training-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = TrainingAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🎓 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
