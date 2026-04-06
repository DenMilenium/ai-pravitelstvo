#!/usr/bin/env python3
"""
👔 Recruiter-Agent
Talent Acquisition Specialist

Подбор персонала, собеседования, HR процессы.
"""

import argparse
from pathlib import Path
from typing import Dict


class RecruiterAgent:
    """
    👔 Recruiter-Agent
    
    Специализация: Talent Acquisition
    Задачи: Hiring, Screening, Interviews
    """
    
    NAME = "👔 Recruiter-Agent"
    ROLE = "Technical Recruiter"
    EXPERTISE = ["Recruiting", "Screening", "Interviews", "Talent Acquisition"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "job-description.md": self._generate_jd(),
            "interview-guide.md": self._generate_interview(),
            "evaluation-rubric.md": self._generate_rubric(),
            "hiring-process.md": self._generate_process()
        }
    
    def _generate_jd(self) -> str:
        return '''# Job Description: Senior Full Stack Developer

## About the Role
We're looking for a Senior Full Stack Developer to join our growing team. 
You'll work on challenging projects using modern technologies.

## Responsibilities
- Design and implement scalable web applications
- Collaborate with cross-functional teams
- Mentor junior developers
- Code reviews and technical leadership
- Architect solutions for complex problems

## Requirements

### Must Have
- 5+ years of experience in web development
- Strong proficiency in **JavaScript/TypeScript**
- Experience with **React** and **Node.js**
- Database design (PostgreSQL, MongoDB)
- RESTful API design and implementation
- Git, CI/CD, Docker
- Upper-intermediate English

### Nice to Have
- Experience with **AWS/GCP/Azure**
- Knowledge of **GraphQL**
- Microservices architecture
- Kubernetes experience
- Open source contributions
- Tech blog or conference talks

## What We Offer
- Competitive salary: $80,000 - $120,000
- Remote-first culture
- Flexible working hours
- Learning budget: $2,000/year
- Health insurance
- 25 days paid vacation
- Stock options

## Tech Stack
- **Frontend**: React, TypeScript, Next.js, Tailwind CSS
- **Backend**: Node.js, Python, PostgreSQL
- **DevOps**: AWS, Docker, Kubernetes, GitHub Actions
- **Tools**: Figma, Jira, Slack, Notion

## Interview Process
1. **Screening Call** (30 min) - HR + Culture fit
2. **Technical Interview** (60 min) - Live coding + System design
3. **Take-home Task** (4 hours) - Real-world problem
4. **Final Interview** (60 min) - Team fit with CTO

## How to Apply
Send your CV and GitHub profile to: careers@company.com
'''
    
    def _generate_interview(self) -> str:
        return '''# Interview Guide: Senior Developer

## Pre-Interview Checklist
- [ ] Review candidate's CV and GitHub
- [ ] Prepare coding exercise
- [ ] Check system design scenario
- [ ] Review previous interviews (if any)

---

## 1. Introduction (5 min)
**Goal**: Make candidate comfortable, set expectations

**Script**:
> "Hi [Name], thanks for joining! I'm [Your name], [Role]. 
> Today we'll spend about 60 minutes together. 
> First, I'd love to hear about your background, 
> then we'll do some coding, and finally discuss system design."

**Ask**:
- How are you doing today?
- Any questions about the process before we start?

---

## 2. Background & Experience (15 min)
**Goal**: Understand depth of experience

**Questions**:
1. "Walk me through your recent project. What was your role?"
2. "What's the most challenging technical problem you've solved?"
3. "Tell me about a time you had to make a difficult architectural decision."
4. "How do you approach code reviews?"
5. "How do you mentor junior developers?"

**Green Flags**:
- Clear communication
- Takes ownership
- Mentions trade-offs
- Mentions team collaboration

**Red Flags**:
- Only "I" (no "we")
- Vague answers
- No depth when probed

---

## 3. Live Coding (25 min)
**Goal**: Assess problem-solving and coding skills

**Problem**: Build a simple autocomplete component

**Requirements**:
- Fetch data from API
- Debounce input
- Handle loading/error states
- Keyboard navigation

**Evaluation Criteria**:
| Aspect | Poor | Good | Excellent |
|--------|------|------|-----------|
| Problem Understanding | Needs clarification | Understands quickly | Asks edge cases |
| Approach | Jumps into code | Plans first | Discusses trade-offs |
| Code Quality | Messy | Clean | Production-ready |
| Testing | None | Some | Comprehensive |
| Communication | Silent | Explains | Collaborative |

---

## 4. System Design (10 min)
**Goal**: Assess architectural thinking

**Question**: 
> "Design a URL shortener like bit.ly. 
> Focus on scalability and availability."

**What to Look For**:
- Requirements clarification
- Database choice (SQL vs NoSQL)
- Caching strategy
- Handling collisions
- Analytics/metrics

---

## 5. Candidate Questions (5 min)
**Goal**: Gauge interest and cultural fit

**Common Questions**:
- "What does success look like in this role?"
- "Tell me about the team structure."
- "What are the biggest challenges?"

---

## Rating Scale

| Category | 1 (Poor) | 2 | 3 (Good) | 4 | 5 (Excellent) |
|----------|----------|---|----------|---|---------------|
| Technical Skills | | | | | |
| Problem Solving | | | | | |
| Communication | | | | | |
| Cultural Fit | | | | | |

**Overall Recommendation**:
- [ ] Strong Hire
- [ ] Hire
- [ ] Lean Hire
- [ ] Lean No Hire
- [ ] No Hire

**Notes**:

'''
    
    def _generate_rubric(self) -> str:
        return '''# Technical Interview Evaluation Rubric

## Technical Skills (40%)

### Coding (20 points)
| Score | Criteria |
|-------|----------|
| 1-4 | Struggles with basic syntax, needs lots of help |
| 5-8 | Gets it done but code is messy |
| 9-12 | Good solution, minor issues |
| 13-16 | Clean code, good practices |
| 17-20 | Excellent, production-ready, handles edge cases |

### System Design (20 points)
| Score | Criteria |
|-------|----------|
| 1-4 | Doesn't understand scale, poor choices |
| 5-8 | Basic understanding, misses important aspects |
| 9-12 | Good design, reasonable trade-offs |
| 13-16 | Strong design, considers multiple factors |
| 17-20 | Excellent, deep understanding, innovative |

## Problem Solving (30%)

### Approach (15 points)
- **1-3**: No plan, jumps into coding
- **4-6**: Some planning but unclear
- **7-9**: Clear plan, breaks down problem
- **10-12**: Methodical, considers alternatives
- **13-15**: Exceptional analytical thinking

### Handling Feedback (15 points)
- **1-3**: Defensive or ignores hints
- **4-6**: Accepts feedback but struggles
- **7-9**: Takes feedback well
- **10-12**: Incorporates feedback effectively
- **13-15**: Thrives on feedback, adapts quickly

## Communication (20%)

### Clarity (10 points)
- **1-2**: Hard to follow, mumbling
- **3-4**: Okay but sometimes unclear
- **5-6**: Clear and organized
- **7-8**: Very clear, good structure
- **9-10**: Exceptional communicator

### Collaboration (10 points)
- **1-2**: Works in isolation
- **3-4**: Some interaction
- **5-6**: Good collaboration
- **7-8**: Engages interviewer as teammate
- **9-10**: Outstanding team player

## Cultural Fit (10%)

### Values Alignment (5 points)
- **1**: Red flags on values
- **2-3**: Okay fit
- **4**: Good fit
- **5**: Excellent alignment

### Growth Mindset (5 points)
- **1**: Fixed mindset, knows everything
- **2-3**: Some openness
- **4**: Eager to learn
- **5**: Learning enthusiast

---

## Score Interpretation

| Total Score | Recommendation |
|-------------|----------------|
| 90-100 | Strong Hire - Exceptional candidate |
| 80-89 | Hire - Solid candidate |
| 70-79 | Lean Hire - Good with reservations |
| 60-69 | Lean No Hire - Some concerns |
| 50-59 | No Hire - Significant gaps |
| <50 | Strong No Hire - Multiple red flags |

## Hiring Decision

**Hire if:**
- Technical score ≥ 12/20
- Communication ≥ 7/10
- No red flags in cultural fit

**Strong Hire if:**
- Technical score ≥ 16/20
- All categories ≥ 4/5
- Would be excited to work with them
'''
    
    def _generate_process(self) -> str:
        return '''# Hiring Process Template

## Stage 1: Sourcing (Week 1-2)

### Channels
- [ ] Job boards (LinkedIn, Indeed, Glassdoor)
- [ ] Employee referrals
- [ ] GitHub/StackOverflow sourcing
- [ ] University recruiting
- [ ] Agency partnerships

### Outreach Template
```
Subject: Opportunity at [Company] - [Role]

Hi [Name],

I came across your profile and was impressed by your work on [Project].

We're hiring for a [Role] at [Company]. Based on your experience with 
[Technology], I think you'd be a great fit.

Would you be open to a quick call to learn more?

Best,
[Recruiter Name]
```

---

## Stage 2: Screening (Week 2-3)

### HR Screening (30 min)
**Topics:**
- Career goals
- Salary expectations
- Notice period
- Basic culture fit
- Visa/work authorization

**Go/No-Go Criteria:**
- Salary within budget
- Timeline aligns
- Communication skills adequate
- Enthusiasm for role

---

## Stage 3: Technical (Week 3-4)

### Technical Interview 1: Coding
- **Duration**: 60 min
- **Format**: Live coding
- **Focus**: Problem-solving, code quality

### Technical Interview 2: System Design
- **Duration**: 60 min
- **Format**: Architecture discussion
- **Focus**: Scalability, trade-offs

### Take-Home Assignment (Optional)
- **Duration**: 4 hours max
- **Focus**: Real-world scenario
- **Review**: Code review session

---

## Stage 4: Final (Week 4-5)

### Team Fit
- **Interviewers**: Future teammates
- **Focus**: Collaboration, values

### Leadership Interview
- **Interviewers**: CTO/VP Engineering
- **Focus**: Career growth, vision alignment

### Offer
- **Timeline**: Within 48 hours
- **Includes**: Compensation, start date, benefits

---

## Timeline Summary

| Stage | Duration | Owners |
|-------|----------|--------|
| Application | 1-3 days | Recruiting |
| HR Screening | 30 min | HR |
| Technical 1 | 60 min | Senior Dev |
| Technical 2 | 60 min | Staff Engineer |
| Take-home | 4 hours | Candidate |
| Final | 60 min | CTO |
| Offer | 2 days | HR |
| **Total** | **2-3 weeks** | |

---

## Rejection Handling

### Template
```
Subject: Application Update - [Company]

Hi [Name],

Thank you for your interest in [Role] at [Company].

After careful consideration, we've decided not to move forward 
with your application at this time. [Optional: brief reason]

We wish you the best in your job search and future endeavors.

Best regards,
[Company] Recruiting Team
```

---

## Onboarding Prep

### Before Day 1
- [ ] Send welcome email
- [ ] Prepare equipment
- [ ] Create accounts
- [ ] Assign buddy
- [ ] Schedule orientation

### First Week
- [ ] Office tour / remote setup
- [ ] Team introductions
- [ ] Access provisioning
- [ ] First tasks assigned
- [ ] 1:1 with manager
'''


def main():
    parser = argparse.ArgumentParser(description="👔 Recruiter-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = RecruiterAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"👔 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
