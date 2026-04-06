#!/usr/bin/env python3
"""
📚 Onboarding-Agent
Employee Onboarding Specialist

Адаптация новых сотрудников, онбординг процессы.
"""

import argparse
from pathlib import Path
from typing import Dict


class OnboardingAgent:
    """
    📚 Onboarding-Agent
    
    Специализация: Employee Onboarding
    Задачи: New hire integration, 30-60-90 day plans
    """
    
    NAME = "📚 Onboarding-Agent"
    ROLE = "Onboarding Specialist"
    EXPERTISE = ["Onboarding", "Training", "Employee Integration"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "onboarding-checklist.md": self._generate_checklist(),
            "first-day-guide.md": self._generate_first_day(),
            "30-60-90-plan.md": self._generate_plan(),
            "buddy-program.md": self._generate_buddy()
        }
    
    def _generate_checklist(self) -> str:
        return '''# New Hire Onboarding Checklist

## Before First Day

### HR Tasks
- [ ] Send welcome email
- [ ] Prepare employment contract
- [ ] Set up payroll
- [ ] Add to company directory
- [ ] Order business cards (if applicable)
- [ ] Create email account
- [ ] Create Slack/Teams account
- [ ] Add to relevant channels/groups

### IT Setup
- [ ] Prepare laptop/workstation
- [ ] Create accounts:
  - [ ] GitHub (add to organization)
  - [ ] Jira/Linear
  - [ ] Figma
  - [ ] Google Workspace/Office 365
  - [ ] VPN access
  - [ ] AWS/GCP/Azure console
- [ ] Install required software
- [ ] Configure development environment
- [ ] Set up 2FA/MFA

### Manager Tasks
- [ ] Assign buddy/mentor
- [ ] Schedule intro meetings
- [ ] Prepare first project/tasks
- [ ] Book 1:1 meetings
- [ ] Add to team calendar

---

## First Day

### Morning (9:00 - 12:00)
- [ ] Welcome and office tour (or remote setup help)
- [ ] Introduction to team
- [ ] Setup workspace
- [ ] HR paperwork (if not done)
- [ ] IT orientation
- [ ] Lunch with team

### Afternoon (13:00 - 17:00)
- [ ] Company overview presentation
- [ ] Product demo
- [ ] Codebase walkthrough
- [ ] First 1:1 with manager
- [ ] Set up development environment

---

## First Week

### Day 2-3
- [ ] Access all necessary systems
- [ ] Read documentation:
  - [ ] Engineering handbook
  - [ ] Coding standards
  - [ ] Architecture overview
  - [ ] Team processes
- [ ] Setup local development
- [ ] Run project locally
- [ ] Attend team standup

### Day 4-5
- [ ] First code review
- [ ] Complete first small task
- [ ] Meet with key stakeholders
- [ ] Attend team retrospective (if applicable)
- [ ] Feedback session with buddy

---

## First Month

### Week 2
- [ ] Complete onboarding tickets
- [ ] Shadow senior developer
- [ ] Attend architecture review
- [ ] One-on-ones with team members
- [ ] Complete security training

### Week 3
- [ ] Take on first real feature
- [ ] Participate in technical discussion
- [ ] Write documentation
- [ ] Attend cross-team meeting

### Week 4
- [ ] Complete first feature
- [ ] 30-day check-in with manager
- [ ] Feedback survey
- [ ] Set 90-day goals

---

## 30-60-90 Day Milestones

### Day 30: Learn
- [ ] Understand codebase structure
- [ ] Know team processes
- [ ] Completed first tasks
- [ ] Met all key team members
- [ ] Comfortable with tools

### Day 60: Contribute
- [ ] Working independently on tasks
- [ ] Contributing to code reviews
- [ ] Participating in planning
- [ ] Identified improvement areas
- [ ] Building relationships

### Day 90: Optimize
- [ ] Full ownership of features
- [ ] Mentoring newer team members
- [ ] Proposing process improvements
- [ ] Deep domain knowledge
- [ ] Performance review ready
'''
    
    def _generate_first_day(self) -> str:
        return '''# First Day Guide for New Developers

## 🎉 Welcome!

We're excited to have you join the team! This guide will help you 
navigate your first day smoothly.

---

## 📧 Your Welcome Email

You've received an email with:
- Your login credentials
- Slack invitation
- Calendar invites for today
- Pre-reading materials

**Action**: Check your personal email and accept all invites.

---

## 🏢 Morning Schedule (9:00 AM)

### 9:00 - 9:30: Arrival & Setup
**Location**: [Office address / Zoom link]

**What to bring**:
- Laptop (if you have one)
- ID for badge
- Questions!

**Who you'll meet**: [Buddy name] - your onboarding buddy

### 9:30 - 10:30: Office Tour / Remote Setup
- Tour of the office (if on-site)
- Workspace setup
- Coffee/tea break
- Meet the immediate team

### 10:30 - 12:00: HR & IT Orientation
- Complete any remaining paperwork
- IT setup (accounts, laptop, VPN)
- Security briefing
- Benefits overview

---

## 🍽️ Lunch (12:00 - 13:00)

**Team lunch!** 
This is a great time to get to know your colleagues in a relaxed setting.

**Icebreaker topics**:
- What got you into coding?
- Favorite side projects?
- Best book/podcast for developers?

---

## 💻 Afternoon (13:00 - 17:00)

### 13:00 - 14:00: Company Overview
**Presenter**: [CEO/CTO/Team Lead]

**Topics**:
- Company history and mission
- Product overview
- Team structure
- Company culture
- Q&A

### 14:00 - 15:00: Product Deep Dive
- Demo of main product
- User personas
- Current roadmap
- Your role in the big picture

### 15:00 - 16:00: Technical Overview
**With**: Tech Lead

- Architecture diagram walkthrough
- Tech stack explanation
- Development workflow
- Deployment process
- Monitoring and alerts

### 16:00 - 17:00: 1:1 with Manager
**Topics**:
- Role expectations
- First week priorities
- 30-60-90 day plan
- Questions and concerns
- Regular 1:1 schedule

---

## 📋 Day 1 Action Items

### Immediate
- [ ] Set up Slack profile (photo, timezone)
- [ ] Join these channels:
  - #general
  - #engineering
  - #random
  - #[your-team]
- [ ] Add photo to company directory
- [ ] Update calendar availability

### This Week
- [ ] Complete security training
- [ ] Read engineering handbook
- [ ] Set up local development
- [ ] Introduce yourself in #general

---

## ❓ Common Questions

**Q: What if I get stuck?**
A: Ask your buddy first, then post in #engineering-help

**Q: What are working hours?**
A: Core hours are 10am-4pm [Timezone], but flexible

**Q: How do I request time off?**
A: Through [HR system] - see handbook for process

**Q: Where's the best coffee? ☕**
A: [Local recommendations]

---

## 📞 Key Contacts

| Role | Name | Slack | Email |
|------|------|-------|-------|
| Manager | [Name] | @[handle] | [email] |
| Buddy | [Name] | @[handle] | [email] |
| HR | [Name] | @[handle] | [email] |
| IT Support | [Name] | @[handle] | [email] |

---

## 🎯 Success for Day 1

✅ Feel welcomed and oriented
✅ Have working laptop and accounts
✅ Met your team
✅ Understand the product
✅ Know who to ask for help

**Remember**: No one expects you to be productive on day 1. 
Focus on learning and asking questions!

---

## 💬 Quote to Remember

> "The only stupid question is the one you don't ask."

We've all been the new person. Everyone is here to help! 🚀
'''
    
    def _generate_plan(self) -> str:
        return '''# 30-60-90 Day Plan for New Developers

## 📅 Day 1-30: LEARN

### Goals
- Understand our product and users
- Learn the codebase and architecture
- Know the team and processes
- Complete first small tasks

### Week 1-2: Orientation
**Learning Focus**: Product & People

| Task | Status | Notes |
|------|--------|-------|
| Complete all onboarding modules | [ ] | |
| Attend product training | [ ] | |
| Shadow 3 senior developers | [ ] | |
| Read architecture docs | [ ] | |
| Understand CI/CD pipeline | [ ] | |
| Complete first bug fix | [ ] | |

**Key Meetings**:
- [ ] 1:1 with each team member
- [ ] Architecture review
- [ ] Product demo
- [ ] User research session

**Deliverables**:
- [ ] Local environment running
- [ ] First PR merged
- [ ] Documentation feedback provided

### Week 3-4: Integration
**Learning Focus**: Technical Deep Dive

| Task | Status | Notes |
|------|--------|-------|
| Complete 3 small features | [ ] | |
| Participate in code reviews | [ ] | |
| Write technical documentation | [ ] | |
| Attend customer call | [ ] | |
| Join on-call rotation (shadow) | [ ] | |

**Success Metrics**:
- Can explain system architecture
- Comfortable with git workflow
- Knows how to deploy
- Understands monitoring

---

## 📅 Day 31-60: CONTRIBUTE

### Goals
- Work independently on features
- Contribute to team processes
- Build cross-team relationships
- Identify improvement areas

### Week 5-6: Ownership
**Focus**: Independent Contribution

| Task | Status | Notes |
|------|--------|-------|
| Own first medium feature | [ ] | |
| Lead a code review | [ ] | |
| Participate in sprint planning | [ ] | |
| Present in team demo | [ ] | |
| Fix 2 production bugs | [ ] | |

**Key Meetings**:
- [ ] First performance check-in
- [ ] 1:1 with product manager
- [ ] Cross-team sync

### Week 7-8: Impact
**Focus**: Team Contribution

| Task | Status | Notes |
|------|--------|-------|
| Propose process improvement | [ ] | |
| Mentor another new hire | [ ] | |
| Contribute to team rituals | [ ] | |
| Complete security certification | [ ] | |
| Write blog post/talk | [ ] | Optional |

**Deliverables**:
- [ ] Feature shipped to production
- [ ] Documentation written
- [ ] Process improvement implemented

---

## 📅 Day 61-90: OPTIMIZE

### Goals
- Full ownership of area
- Strategic thinking
- Mentoring others
- Prepare for performance review

### Week 9-10: Leadership
**Focus**: Technical Leadership

| Task | Status | Notes |
|------|--------|-------|
| Design complex feature | [ ] | |
| Mentor junior developer | [ ] | |
| Lead technical discussion | [ ] | |
| Contribute to architecture decisions | [ ] | |
| Give tech talk | [ ] | |

### Week 11-12: Excellence
**Focus**: Performance Review Prep

| Task | Status | Notes |
|------|--------|-------|
| Self-assessment | [ ] | |
| Gather feedback | [ ] | |
| Set next quarter goals | [ ] | |
| Career path discussion | [ ] | |
| 90-day retrospective | [ ] | |

**Success Metrics**:
- Shipped major feature
- Improved team process
- Strong peer feedback
- Clear growth trajectory

---

## 📊 Success Metrics by Phase

### Day 30 Check-in
**Technical**:
- [ ] Can navigate codebase independently
- [ ] Understands deployment process
- [ ] Knows monitoring and debugging tools

**Cultural**:
- [ ] Knows everyone on the team
- [ ] Comfortable asking questions
- [ ] Participates in team discussions

### Day 60 Check-in
**Technical**:
- [ ] Ships features independently
- [ ] Produces quality code
- [ ] Contributes to technical decisions

**Cultural**:
- [ ] Contributes to team culture
- [ ] Helps unblock others
- [ ] Provides constructive feedback

### Day 90 Check-in
**Technical**:
- [ ] Expert in domain area
- [ ] Leads technical initiatives
- [ ] Mentors others

**Cultural**:
- [ ] Embodies company values
- [ ] Trusted team member
- [ ] Ready for next level

---

## 🎯 Manager's Checklist

### Week 1
- [ ] Daily check-ins
- [ ] Clarify expectations
- [ ] Ensure tools access
- [ ] Introduce to stakeholders

### Week 4
- [ ] 30-day formal check-in
- [ ] Adjust goals if needed
- [ ] Gather peer feedback
- [ ] Celebrate wins

### Week 8
- [ ] 60-day check-in
- [ ] Career path discussion
- [ ] Increase responsibilities
- [ ] Provide growth opportunities

### Week 12
- [ ] 90-day performance review
- [ ] Set next quarter goals
- [ ] Discuss promotion timeline
- [ ] Document achievements
'''
    
    def _generate_buddy(self) -> str:
        return '''# Buddy Program Guide

## 🎯 Program Overview

**Purpose**: Help new hires integrate quickly and feel welcome
**Commitment**: 30-60 minutes daily for first 2 weeks
**Relationship**: Informal mentor and friend

---

## 👥 Your Role as a Buddy

### Week 1: Daily Touchpoints

**Day 1**:
- [ ] Meet for coffee/breakfast
- [ ] Office tour
- [ ] Introduce to team members
- [ ] Answer "where is..." questions
- [ ] Lunch together

**Day 2-5**:
- [ ] Morning check-in (15 min)
- [ ] Help with setup questions
- [ ] Include in social conversations
- [ ] Answer Slack messages promptly

### Week 2-4: Regular Check-ins
- [ ] 3x weekly check-ins
- [ ] Code review together
- [ ] Explain team norms
- [ ] Share "unwritten rules"

---

## 📋 Buddy Checklist

### Before They Arrive
- [ ] Review their background/LinkedIn
- [ ] Prepare your "day in the life" story
- [ ] Think about who they should meet
- [ ] Prepare list of resources

### First Day
- [ ] Be at reception/zoom early
- [ ] Help with IT setup
- [ ] Explain Slack etiquette
- [ ] Show where to get food/coffee
- [ ] Introduce to key people
- [ ] Check in at end of day

### First Week
- [ ] Explain team rituals (standups, retros)
- [ ] Walk through codebase together
- [ ] Share your favorite tools/extensions
- [ ] Explain our code review culture
- [ ] Introduce to people from other teams

### Ongoing
- [ ] Include them in lunch/coffee
- [ ] Answer "stupid questions" without judgment
- [ ] Share context on decisions
- [ ] Provide honest feedback
- [ ] Celebrate their wins

---

## 💬 Conversation Starters

### Getting to Know Them
- "What got you into software development?"
- "What's your favorite side project?"
- "What are you most excited to learn here?"
- "What's your superpower as a developer?"
- "How do you like to receive feedback?"

### Sharing Context
- "Here's how we handle disagreements..."
- "The best way to get help is..."
- "One thing I wish I knew when I started..."
- "Our unwritten rules include..."
- "The person to know for X is..."

### Checking In
- "How are you feeling about everything?"
- "What's been most confusing?"
- "Is there anything you feel stuck on?"
- "What's going well?"
- "How can I help better?"

---

## 🚨 Red Flags to Watch For

### Signs They Might Be Struggling
- [ ] Not asking any questions
- [ ] Working very late consistently
- [ ] Seeming isolated from team
- [ ] Expressing frustration
- [ ] Missing standups/meetings

### What to Do
1. Ask directly: "How are you really doing?"
2. Listen without judgment
3. Offer specific help
4. Escalate to manager if needed
5. Follow up

---

## 📚 Resources to Share

### Day 1
- [ ] Team Slack channels cheat sheet
- [ ] Calendar of recurring meetings
- [ ] Link to engineering handbook
- [ ] Contact list for support

### Week 1
- [ ] Best learning resources for our stack
- [ ] Recommended codebase areas to explore
- [ ] Documentation that helped you
- [ ] Conference talks about our architecture

### Ongoing
- [ ] Professional development opportunities
- [ ] Internal mobility options
- [ ] Company perks and benefits
- [ ] Social events and groups

---

## ✅ Buddy Success Metrics

**After 30 days, your buddy should:**
- [ ] Know who to ask for what
- [ ] Feel comfortable in team meetings
- [ ] Have made at least one friend
- [ ] Understand team culture
- [ ] Be productive on their tasks

**Your feedback to manager should include:**
- How are they adjusting?
- Any concerns?
- What support do they need?
- How can the process improve?

---

## 🏆 Great Buddy Traits

✅ **Available** - Responds to questions quickly
✅ **Patient** - Doesn't get frustrated with basics
✅ **Proactive** - Checks in without being asked
✅ **Inclusive** - Brings them into conversations
✅ **Honest** - Shares both good and challenging aspects

---

## 💝 Thank You!

Being a buddy is one of the most impactful things you can do 
for our team culture. Thank you for helping make someone's 
first days great!

**Remember**: The relationships you build as a buddy often 
become the strongest professional connections you'll have.
'''


def main():
    parser = argparse.ArgumentParser(description="📚 Onboarding-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = OnboardingAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"📚 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
