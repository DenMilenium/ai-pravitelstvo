#!/usr/bin/env python3
"""
🏃 Agile-Agent
Agile Methodology Specialist

Agile процессы, Scrum, Kanban, ретроспективы.
"""

import argparse
from pathlib import Path
from typing import Dict


class AgileAgent:
    """
    🏃 Agile-Agent
    
    Специализация: Agile Practices
    Задачи: Scrum, Kanban, Ceremonies, Retrospectives
    """
    
    NAME = "🏃 Agile-Agent"
    ROLE = "Agile Coach"
    EXPERTISE = ["Agile", "Scrum", "Kanban", "Retrospectives", "Facilitation"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "sprint-template.md": self._generate_sprint(),
            "ceremonies-guide.md": self._generate_ceremonies(),
            "retrospective.md": self._generate_retro(),
            "team-metrics.md": self._generate_metrics()
        }
    
    def _generate_sprint(self) -> str:
        return '''# Sprint Planning Template

## Sprint Information
- **Sprint Number**: 
- **Duration**: 2 weeks
- **Dates**: [Start] - [End]
- **Team**: 
- **Sprint Goal**: 

---

## 📊 Capacity

### Team Availability
| Team Member | Role | Days Available | Notes |
|-------------|------|----------------|-------|
| | Dev | | |
| | Dev | | |
| | QA | | |
| | Designer | | |

**Total Capacity**: ___ story points
**Buffer (20%)**: ___ story points
**Commitment**: ___ story points

---

## 🎯 Sprint Goal

> [One sentence describing what we want to achieve this sprint]

**Why this matters**: 

**Success looks like**:
- [ ] 
- [ ] 
- [ ] 

---

## 📋 Sprint Backlog

### High Priority (Must Have)
| ID | Story | Points | Owner | Notes |
|----|-------|--------|-------|-------|
| | | | | |
| | | | | |

### Medium Priority (Should Have)
| ID | Story | Points | Owner | Notes |
|----|-------|--------|-------|-------|
| | | | | |

### Low Priority (Nice to Have)
| ID | Story | Points | Owner | Notes |
|----|-------|--------|-------|-------|
| | | | | |

**Total Points Committed**: ___

---

## ⚠️ Risks & Dependencies

| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| | High/Med/Low | | |

### Dependencies
- [ ] Dependency 1: [Description] - Blocked by: [Team/Person]
- [ ] Dependency 2: [Description] - ETA: [Date]

---

## 📅 Sprint Schedule

### Week 1
| Day | Event | Time | Duration |
|-----|-------|------|----------|
| Monday | Sprint Planning | 10:00 | 2h |
| Tuesday | Standup | 9:30 | 15m |
| Wednesday | Standup | 9:30 | 15m |
| Thursday | Standup | 9:30 | 15m |
| Friday | Standup | 9:30 | 15m |

### Week 2
| Day | Event | Time | Duration |
|-----|-------|------|----------|
| Monday | Standup | 9:30 | 15m |
| Tuesday | Standup | 9:30 | 15m |
| Wednesday | Mid-sprint review | 14:00 | 30m |
| Thursday | Standup + Grooming | 9:30 | 1h |
| Friday | Demo + Retro | 15:00 | 2h |

---

## 🎮 Definition of Done

### For User Stories
- [ ] Code complete
- [ ] Code reviewed by at least 1 person
- [ ] All tests passing (unit, integration)
- [ ] QA approved
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PO acceptance

### For Bugs
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Regression test added
- [ ] QA verified

### For Tasks
- [ ] Task completed
- [ ] Verified by stakeholder

---

## 📈 Sprint Predictions

**Velocity Trend**: ___
**Burndown Target**: ___
**Confidence Level**: High / Medium / Low

**Factors affecting confidence**:
- 
- 

---

## 📝 Notes

[Space for additional notes, decisions made, etc.]
'''
    
    def _generate_ceremonies(self) -> str:
        return '''# Agile Ceremonies Guide

## 🌅 Daily Standup

### Purpose
- Synchronize team
- Identify blockers
- Build team cohesion

### Format (15 minutes)
Each person answers:
1. **Yesterday**: What did I complete?
2. **Today**: What will I work on?
3. **Blockers**: Any impediments?

### Anti-Patterns to Avoid
❌ Problem-solving in standup
❌ Talking to the Scrum Master only
❌ Going over 15 minutes
❌ Skipping it regularly
❌ Reporting status to manager

### Tips for Success
✅ Start on time (even if people are missing)
✅ Stand up (literally)
✅ Pass the token (who speaks next)
✅ Update board in real-time
✅ Take long discussions offline

---

## 🎯 Sprint Planning

### Purpose
- Select work for the sprint
- Define sprint goal
- Create plan to achieve goal

### Inputs
- Refined backlog
- Team velocity
- Capacity
- Sprint goal proposal

### Agenda (2-4 hours)

#### Part 1: The "What" (1 hour)
1. Review sprint goal (5 min)
2. Product owner presents priorities (15 min)
3. Team asks questions/clarifies (20 min)
4. Team selects items from backlog (20 min)

#### Part 2: The "How" (1-2 hours)
1. Break stories into tasks (30 min)
2. Estimate tasks (30 min)
3. Identify dependencies/risks (15 min)
4. Finalize commitment (15 min)

#### Output
- Sprint backlog
- Sprint goal
- Team commitment

---

## 📊 Sprint Review (Demo)

### Purpose
- Inspect increment
- Adapt product backlog
- Stakeholder feedback

### Participants
- Development team
- Product owner
- Stakeholders
- Customers (optional)

### Format (1 hour)

1. **Introduction** (5 min)
   - Sprint goal recap
   - What was committed

2. **Demo** (40 min)
   - Working software only
   - Each team member demos their work
   - Focus on value, not mechanics
   - Collect feedback

3. **Product Backlog Discussion** (10 min)
   - What's next?
   - Stakeholder input
   - Market/business updates

4. **Wrap-up** (5 min)
   - Next steps
   - Thank you

### Tips
✅ Demo working features
✅ Tell a story
✅ Prepare beforehand
✅ Invite right stakeholders
✅ Record for absent people

---

## 🔄 Sprint Retrospective

### Purpose
- Inspect process
- Identify improvements
- Create action plan

### The 5 Phases (1 hour)

#### 1. Set the Stage (5 min)
- Welcome everyone
- Review working agreements
- Focus on improvement, not blame

#### 2. Gather Data (15 min)
Activities to choose from:
- **What went well?** 😊
- **What didn't go well?** 😞
- **What confused us?** 😕

Or:
- Timeline of sprint
- Mad/Sad/Glad
- Sailboat (wind/anchors/rocks/sun)

#### 3. Generate Insights (15 min)
- Group similar items
- Dot voting on top issues
- Root cause analysis (5 Whys)

#### 4. Decide Actions (15 min)
- Select 1-3 improvements
- Make them SMART:
  - Specific
  - Measurable
  - Achievable
  - Relevant
  - Time-bound

#### 5. Close (10 min)
- Summarize actions
- Appreciations
- Rate the retro (1-5)

### Sample Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Add integration test for X | @dev1 | Next sprint |
| Update deployment docs | @dev2 | This week |
| Investigate CI slowdown | @dev3 | Next sprint |

---

## 🎓 Backlog Refinement

### Purpose
- Keep backlog healthy
- Clarify requirements
- Estimate effort

### When
- Weekly (1-2 hours)
- Or ongoing (10% of sprint)

### Activities
- [ ] Review new stories
- [ ] Clarify acceptance criteria
- [ ] Split large stories
- [ ] Estimate stories
- [ ] Reorder backlog
- [ ] Remove outdated items

### Definition of Ready
Story is ready for sprint when:
- [ ] Clear description
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Sized by team
- [ ] No blockers

---

## 📈 Metrics to Track

### Team Metrics
- Velocity (points per sprint)
- Sprint burndown
- Release burndown
- Cycle time
- Lead time

### Quality Metrics
- Defect rate
- Escaped defects
- Test coverage
- Technical debt items

### Team Health
- Happiness index
- Retrospective actions completed
- Team participation
- Blocker resolution time

---

## 🚨 Common Anti-Patterns

### Scrum Buts
- "We do Scrum, but we don't have retrospectives"
- "We do Scrum, but our sprints are 6 weeks"
- "We do Scrum, but the PM assigns all tasks"

### Solutions
1. **Educate** - Explain the "why"
2. **Start small** - Implement one thing at a time
3. **Inspect & Adapt** - Retro your retros
4. **Get help** - Agile coach/training

---

## 🛠️ Tools

### Digital Boards
- Jira
- Linear
- Azure DevOps
- GitHub Projects
- Notion

### Collaboration
- Miro (retros)
- FunRetro
- Parabol
- EasyRetro

### Metrics
- Jira dashboards
- ActionableAgile
- Screenful
'''
    
    def _generate_retro(self) -> str:
        return '''# Sprint Retrospective Template

## 📅 Sprint Info
- **Sprint**: 
- **Dates**: 
- **Goal**: 
- **Achieved?**: Yes / Partially / No
- **Velocity**: ___ points

---

## 🎯 Quick Check-in (1-5 scale)

| Question | Avg Score |
|----------|-----------|
| How was this sprint? | |
| Did we meet our goal? | |
| How's team collaboration? | |
| Any blockers/impediments? | |

---

## 📊 Sprint Data

### Completed
| ID | Story | Points | Notes |
|----|-------|--------|-------|
| | | | |

### Not Completed
| ID | Story | Points | Why? |
|----|-------|--------|------|
| | | | |

### Metrics
- **Committed**: ___ points
- **Completed**: ___ points
- **Completion Rate**: ___%
- **Bugs Found**: ___
- **Bugs Fixed**: ___

---

## 📝 Retrospective Board

### 😊 What Went Well
- 
- 
- 

### 😞 What Didn't Go Well
- 
- 
- 

### 💡 Ideas for Improvement
- 
- 
- 

### 🙏 Shout-outs / Appreciations
- @person - for [reason]
- @person - for [reason]

---

## 🔍 Deep Dive Discussion

### Topic 1: [Highest Voted Item]
**Problem**: 

**Root Cause Analysis**:
- Why? → 
- Why? → 
- Why? → 

**Potential Solutions**:
1. 
2. 
3. 

---

## ✅ Action Items

| # | Action | Owner | Due | Priority |
|---|--------|-------|-----|----------|
| 1 | | | | High |
| 2 | | | | Medium |
| 3 | | | | Low |

---

## 📚 Previous Action Review

| Action | Owner | Status | Notes |
|--------|-------|--------|-------|
| | | ✅/❌/⏳ | |

---

## 🎲 Retrospective Activities

### Activity: Sailboat

```
                    🌞 Goal/Vision
                         |
                         |
    🌬️ Wind        ⛵ Team        ⚓ Anchors
   (Helping us)   (What we did)  (Holding us back)
                         |
                         |
                    🪨 Rocks/Risks
```

**Wind** (what helped us):
- 

**Anchors** (what slowed us):
- 

**Rocks** (risks ahead):
- 

---

### Activity: Mad / Sad / Glad

**Mad** (frustrated about):
- 

**Sad** (disappointed about):
- 

**Glad** (happy about):
- 

---

## 📈 Trend Analysis

### Last 3 Sprints
| Sprint | Velocity | Mood | Completed Actions |
|--------|----------|------|-------------------|
| N-2 | | | |
| N-1 | | | |
| N | | | |

### Patterns
- 
- 

---

## 🎯 Next Sprint Focus

**One thing to keep doing**:

**One thing to stop doing**:

**One thing to start doing**:

---

## 📝 Closing

**Retro Rating** (1-5): 

**One word to describe this sprint**:

**Team mood**: 😊 😐 😔

**Next retro facilitator**: 
'''
    
    def _generate_metrics(self) -> str:
        return '''# Team Metrics Dashboard

## 📊 Velocity Tracking

### Sprint Velocity Chart
```
Points
  50 |                                        ●
  45 |                              ●
  40 |                    ●
  35 |          ●
  30 |    ●
  25 |
     +----+----+----+----+----+----+----+----
       S1   S2   S3   S4   S5   S6   S7   S8
```

### Key Metrics
| Metric | Current | Trend | Target |
|--------|---------|-------|--------|
| Average Velocity | 42 pts | ↑ | 45 pts |
| Velocity Variance | ±8 pts | ↓ | ±5 pts |
| Sprint Completion | 95% | → | 90% |

---

## ⏱️ Flow Metrics

### Cycle Time
| Percentile | Time | Trend |
|------------|------|-------|
| 50th (Median) | 3.2 days | ↓ |
| 85th | 6.5 days | ↓ |
| 95th | 9.1 days | → |

**Goal**: 85% of stories complete within 5 days

### Lead Time
- **Average**: 8.5 days
- **Trend**: Improving ↓
- **Breakdown**:
  - Backlog: 2 days
  - In Progress: 4 days
  - Review: 1.5 days
  - Testing: 1 day

---

## 🐛 Quality Metrics

### Defect Rate
| Sprint | Found | Fixed | Escaped |
|--------|-------|-------|---------|
| S1 | 8 | 8 | 1 |
| S2 | 5 | 5 | 0 |
| S3 | 6 | 6 | 1 |

**Defect Density**: 0.15 bugs per story point

### Test Coverage
- Unit Tests: 78% ↑
- Integration Tests: 45% →
- E2E Tests: 25% ↑

**Goal**: 80% unit, 60% integration

---

## 🎯 Sprint Goals

### Goal Achievement Rate
```
S1:  ✅✅✅❌  75%
S2:  ✅✅✅✅ 100%
S3:  ✅✅❌❌  50%
S4:  ✅✅✅❌  75%
```

**Average**: 75%
**Trend**: Stable

---

## 👥 Team Health

### Happiness Index (1-5)
```
Week 1: ████░░░░░░ 4.2
Week 2: █████░░░░░ 4.5
Week 3: ████░░░░░░ 4.1
Week 4: █████░░░░░ 4.6
```

### Participation
- Standup attendance: 98%
- Retro participation: 100%
- Story point estimation: 100%

---

## 🚀 Predictability

### Forecasting
Based on last 6 sprints:
- **Next sprint (80% confidence)**: 35-48 points
- **Next quarter (80% confidence)**: 12-16 stories

### Release Projection
| Feature | Points Remaining | Sprints to Complete |
|---------|------------------|---------------------|
| Feature A | 45 pts | 1.1 |
| Feature B | 120 pts | 2.9 |
| Feature C | 80 pts | 1.9 |

---

## 📋 Improvement Areas

### Top 3 Metrics to Improve
1. **Cycle Time** - Target: 85% within 5 days
   - Action: WIP limits, smaller stories
   
2. **Test Coverage** - Target: 80%
   - Action: TDD enforcement, coverage gates
   
3. **Escaped Defects** - Target: 0
   - Action: Better definition of done

---

## 📈 Team Performance Summary

### What We're Doing Well ✅
- Consistent velocity
- High sprint completion
- Good team happiness

### What Needs Attention ⚠️
- Integration test coverage
- Cycle time variability
- Goal achievement consistency

### Actions in Progress 🔄
- [ ] Implement WIP limits
- [ ] Add integration test framework
- [ ] Refine story splitting

---

## 🎯 Next Quarter Goals

### Performance
- [ ] Increase velocity to 50 pts/sprint
- [ ] Reduce cycle time 85th percentile to 5 days
- [ ] Achieve 90% sprint goal completion

### Quality
- [ ] Zero escaped defects
- [ ] 80% test coverage
- [ ] <1 day review time

### Team
- [ ] Maintain happiness >4.5
- [ ] 100% retro action completion
- [ ] Reduce context switching
'''


def main():
    parser = argparse.ArgumentParser(description="🏃 Agile-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = AgileAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🏃 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
