#!/usr/bin/env python3
"""
📈 BI-Agent
Business Intelligence Specialist

BI-аналитика, дашборды, отчёты, data visualization.
"""

import argparse
from pathlib import Path
from typing import Dict


class BIAgent:
    """
    📈 BI-Agent
    
    Специализация: Business Intelligence
    Задачи: Dashboards, Reports, Data Analysis, KPIs
    """
    
    NAME = "📈 BI-Agent"
    ROLE = "BI Analyst"
    EXPERTISE = ["Business Intelligence", "Dashboards", "Analytics", "KPIs", "Reporting"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "kpi-dashboard.md": self._generate_dashboard(),
            "sql-queries.sql": self._generate_sql(),
            "report-template.md": self._generate_report(),
            "data-model.md": self._generate_datamodel()
        }
    
    def _generate_dashboard(self) -> str:
        return '''# Executive Dashboard Design

## Overview
Real-time business intelligence dashboard for leadership team

---

## 📊 Dashboard Layout

### Row 1: Key Metrics (KPIs)
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   Revenue    │    Users     │   Churn      │     NPS      │
│   $125K      │   12,500     │    4.2%      │     52       │
│   ↑ 15%      │   ↑ 8%       │   ↓ 1.1%     │   ↑ 5 pts    │
│   vs last mo │   vs last mo │   vs last mo │   vs last qt │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**Revenue**:
- Current: $125,000
- Target: $150,000
- Progress: 83%
- Trend: 📈 Positive

**Active Users**:
- Current: 12,500
- Target: 15,000
- Progress: 83%
- Trend: 📈 Growing

**Churn Rate**:
- Current: 4.2%
- Target: <5%
- Status: ✅ On Track
- Trend: 📉 Improving

**NPS Score**:
- Current: 52
- Target: 50
- Status: ✅ Exceeding
- Trend: 📈 Positive

---

### Row 2: Trend Charts

#### Revenue Trend (Last 12 Months)
```
Revenue ($K)
150 │                                    ●
140 │                              ●
130 │                        ●
120 │                  ●
110 │            ●
100 │      ●
 90 │ ●
    └────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────
         Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
```

#### User Growth
```
Users (K)
 15 │                                          ●
 14 │                                    ●
 13 │                              ●
 12 │                        ●
 11 │                  ●
 10 │            ●
    └────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────
         Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
```

---

### Row 3: Detailed Breakdowns

#### Revenue by Product
| Product | Revenue | % of Total | Growth |
|---------|---------|------------|--------|
| Enterprise | $75K | 60% | +20% |
| Pro | $35K | 28% | +10% |
| Starter | $15K | 12% | +5% |

#### Revenue by Region
| Region | Revenue | Users | ARPU |
|--------|---------|-------|------|
| North America | $60K | 5,000 | $12 |
| Europe | $40K | 4,000 | $10 |
| APAC | $25K | 3,500 | $7 |

#### User Acquisition Channels
| Channel | Users | CAC | LTV | LTV/CAC |
|---------|-------|-----|-----|---------|
| Organic | 5,000 | $0 | $120 | ∞ |
| Paid Search | 3,000 | $25 | $80 | 3.2x |
| Social | 2,500 | $30 | $60 | 2.0x |
| Referral | 2,000 | $15 | $100 | 6.7x |

---

## 🎯 Department Dashboards

### Sales Dashboard

**Pipeline Overview**:
```
Pipeline Value: $500K

Stage          │ Value   │ Count │ Win Rate
───────────────┼─────────┼───────┼──────────
Lead           │ $200K   │ 50    │ 20%
Qualified      │ $150K   │ 30    │ 35%
Proposal       │ $100K   │ 15    │ 50%
Negotiation    │ $50K    │ 8     │ 70%
```

**Sales Activity**:
- Calls made: 150
- Demos given: 45
- Proposals sent: 20
- Deals closed: 8

**Rep Performance**:
| Rep | Quota | Closed | % to Goal |
|-----|-------|--------|-----------|
| Alice | $50K | $45K | 90% |
| Bob | $50K | $60K | 120% |
| Carol | $50K | $40K | 80% |

---

### Marketing Dashboard

**Campaign Performance**:
| Campaign | Spend | Leads | CPL | MQLs | Cost/MQL |
|----------|-------|-------|-----|------|----------|
| Q1 Webinar | $5K | 500 | $10 | 100 | $50 |
| Whitepaper | $3K | 300 | $10 | 60 | $50 |
| LinkedIn Ads | $10K | 400 | $25 | 80 | $125 |

**Funnel Metrics**:
```
Impressions → Clicks → Leads → MQLs → SQLs → Customers
   100K    →  5K   →  1K  →  200  →  50  →   10
    100%    →  5%   → 20%  → 20%   → 25%  → 20%
```

**Website Analytics**:
- Visitors: 50,000
- Page views: 200,000
- Bounce rate: 35%
- Avg session: 3:45
- Conversion rate: 2%

---

### Product Dashboard

**Feature Usage**:
| Feature | MAU | % of Users | Avg Uses/Week |
|---------|-----|------------|---------------|
| Dashboard | 10,000 | 80% | 15 |
| Reports | 8,000 | 64% | 5 |
| API | 3,000 | 24% | 50 |
| Integrations | 5,000 | 40% | 3 |

**Performance Metrics**:
- Avg page load: 1.2s
- API response time: 85ms
- Uptime: 99.95%
- Error rate: 0.02%

**User Feedback**:
- NPS: 52
- CSAT: 4.6/5
- Feature requests: 150
- Bugs reported: 25

---

### Customer Success Dashboard

**Health Score Distribution**:
```
Healthy (80-100):  ████████████████████ 60%
At Risk (50-79):   ████████ 25%
Critical (0-49):   ███ 15%
```

**Support Metrics**:
| Metric | This Month | Last Month | Target |
|--------|------------|------------|--------|
| Tickets | 250 | 280 | <300 |
| First Response | 2h | 3h | <4h |
| Resolution | 8h | 12h | <24h |
| CSAT | 4.7 | 4.5 | >4.5 |

**Churn Analysis**:
- Churned this month: 25 customers
- Primary reasons:
  - Price (40%)
  - Missing features (30%)
  - Switched competitor (20%)
  - Other (10%)

---

## 📈 Alert Thresholds

### Red Alerts (Immediate Action)
- Revenue drops >20% vs last month
- Churn rate >8%
- Uptime <99%
- NPS <30

### Yellow Alerts (Monitor Closely)
- Revenue growth <5%
- Churn rate 5-8%
- Support tickets spike >50%
- Feature usage drops >30%

### Green (Healthy)
- All metrics within target range

---

## 🔄 Refresh Schedule

| Dashboard | Refresh Rate | Data Source |
|-----------|--------------|-------------|
| Executive | Real-time | Production DB |
| Sales | Hourly | CRM API |
| Marketing | Daily | GA + HubSpot |
| Product | Real-time | App events |
| CS | Hourly | Zendesk |

---

## 🛠️ Tools Used

- **Data Warehouse**: Snowflake
- **BI Tool**: Looker / Tableau
- **ETL**: Fivetran / Stitch
- **Visualization**: D3.js, Chart.js
- **Alerts**: PagerDuty, Slack
'''
    
    def _generate_sql(self) -> str:
        return '''-- Business Intelligence SQL Queries

-- ============================================
-- 1. DAILY REVENUE METRICS
-- ============================================

WITH daily_revenue AS (
  SELECT 
    DATE(created_at) as date,
    SUM(amount) as revenue,
    COUNT(*) as transactions,
    AVG(amount) as avg_order_value
  FROM orders
  WHERE status = 'completed'
    AND created_at >= DATE_TRUNC('month', CURRENT_DATE)
  GROUP BY 1
)
SELECT 
  date,
  revenue,
  transactions,
  avg_order_value,
  LAG(revenue) OVER (ORDER BY date) as prev_day_revenue,
  ROUND(
    (revenue - LAG(revenue) OVER (ORDER BY date)) / 
    NULLIF(LAG(revenue) OVER (ORDER BY date), 0) * 100, 
    2
  ) as growth_pct
FROM daily_revenue
ORDER BY date DESC;


-- ============================================
-- 2. COHORT RETENTION ANALYSIS
-- ============================================

WITH user_cohorts AS (
  SELECT 
    user_id,
    DATE_TRUNC('month', created_at) as cohort_month
  FROM users
),
user_activity AS (
  SELECT 
    u.user_id,
    uc.cohort_month,
    DATE_TRUNC('month', s.session_date) as activity_month,
    COUNT(*) as sessions
  FROM users u
  JOIN user_cohorts uc ON u.user_id = uc.user_id
  LEFT JOIN sessions s ON u.user_id = s.user_id
  GROUP BY 1, 2, 3
),
cohort_sizes AS (
  SELECT 
    cohort_month,
    COUNT(DISTINCT user_id) as cohort_size
  FROM user_cohorts
  GROUP BY 1
),
retention AS (
  SELECT 
    uc.cohort_month,
    ua.activity_month,
    cs.cohort_size,
    COUNT(DISTINCT ua.user_id) as active_users,
    ROUND(
      COUNT(DISTINCT ua.user_id) * 100.0 / cs.cohort_size, 
      2
    ) as retention_pct
  FROM user_cohorts uc
  JOIN cohort_sizes cs ON uc.cohort_month = cs.cohort_month
  LEFT JOIN user_activity ua ON uc.user_id = ua.user_id
  GROUP BY 1, 2, 3
)
SELECT * FROM retention
ORDER BY cohort_month DESC, activity_month;


-- ============================================
-- 3. CUSTOMER LIFETIME VALUE (LTV)
-- ============================================

WITH user_metrics AS (
  SELECT 
    u.user_id,
    u.created_at as first_order_date,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.amount) as total_revenue,
    AVG(o.amount) as avg_order_value,
    MAX(o.created_at) as last_order_date,
    DATE_PART('day', MAX(o.created_at) - u.created_at) as customer_lifespan_days
  FROM users u
  LEFT JOIN orders o ON u.user_id = o.user_id
  WHERE o.status = 'completed'
  GROUP BY 1, 2
)
SELECT 
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_revenue) as median_ltv,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_revenue) as p75_ltv,
  PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY total_revenue) as p90_ltv,
  AVG(total_revenue) as avg_ltv,
  AVG(avg_order_value) as avg_order_value,
  AVG(total_orders) as avg_orders_per_customer,
  AVG(customer_lifespan_days) as avg_customer_lifespan
FROM user_metrics;


-- ============================================
-- 4. FUNNEL ANALYSIS
-- ============================================

WITH funnel_stages AS (
  SELECT 
    user_id,
    MIN(CASE WHEN event_type = 'signup' THEN event_date END) as signup_date,
    MIN(CASE WHEN event_type = 'onboarding_complete' THEN event_date END) as onboarding_date,
    MIN(CASE WHEN event_type = 'first_transaction' THEN event_date END) as first_transaction_date,
    MIN(CASE WHEN event_type = 'purchase' THEN event_date END) as purchase_date
  FROM events
  WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY 1
)
SELECT 
  COUNT(user_id) as total_signups,
  COUNT(onboarding_date) as completed_onboarding,
  COUNT(first_transaction_date) as made_first_transaction,
  COUNT(purchase_date) as made_purchase,
  ROUND(COUNT(onboarding_date) * 100.0 / COUNT(user_id), 2) as onboarding_rate,
  ROUND(COUNT(first_transaction_date) * 100.0 / COUNT(user_id), 2) as activation_rate,
  ROUND(COUNT(purchase_date) * 100.0 / COUNT(user_id), 2) as conversion_rate
FROM funnel_stages;


-- ============================================
-- 5. CHURN ANALYSIS
-- ============================================

WITH user_activity AS (
  SELECT 
    user_id,
    DATE_TRUNC('month', session_date) as activity_month,
    COUNT(*) as session_count
  FROM sessions
  GROUP BY 1, 2
),
churned_users AS (
  SELECT 
    user_id,
    activity_month,
    LEAD(activity_month) OVER (PARTITION BY user_id ORDER BY activity_month) as next_activity_month
  FROM user_activity
)
SELECT 
  activity_month,
  COUNT(DISTINCT user_id) as total_users,
  COUNT(DISTINCT CASE WHEN next_activity_month IS NULL THEN user_id END) as churned_users,
  ROUND(
    COUNT(DISTINCT CASE WHEN next_activity_month IS NULL THEN user_id END) * 100.0 / 
    COUNT(DISTINCT user_id), 
    2
  ) as churn_rate
FROM churned_users
GROUP BY 1
ORDER BY 1;


-- ============================================
-- 6. PRODUCT FEATURE USAGE
-- ============================================

SELECT 
  feature_name,
  COUNT(DISTINCT user_id) as unique_users,
  COUNT(*) as total_uses,
  AVG(uses_per_user) as avg_uses_per_user,
  ROUND(
    COUNT(DISTINCT user_id) * 100.0 / (SELECT COUNT(*) FROM users), 
    2
  ) as adoption_rate
FROM (
  SELECT 
    user_id,
    feature_name,
    COUNT(*) as uses_per_user
  FROM feature_usage
  WHERE used_at >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY 1, 2
) usage_stats
GROUP BY 1
ORDER BY unique_users DESC;


-- ============================================
-- 7. SUPPORT TICKET ANALYSIS
-- ============================================

SELECT 
  DATE_TRUNC('week', created_at) as week,
  category,
  COUNT(*) as ticket_count,
  AVG(EXTRACT(EPOCH FROM (resolved_at - created_at))/3600) as avg_resolution_hours,
  SUM(CASE WHEN resolved_at IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as resolution_rate,
  AVG(satisfaction_score) as avg_csat
FROM support_tickets
WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY 1, 2
ORDER BY 1 DESC, ticket_count DESC;
'''
    
    def _generate_report(self) -> str:
        return '''# Monthly Business Report Template

## Executive Summary

**Report Period**: [Month Year]
**Prepared By**: [Name]
**Date**: [Date]

### Key Highlights
🎯 **Revenue**: $XXX,XXX (↑X% MoM)
👥 **Users**: XX,XXX (↑X% MoM)
📊 **Churn**: X.X% (↓X% MoM)
⭐ **NPS**: XX (↑X MoM)

### One-Page Summary
> This month we [achievement 1], [achievement 2], and [achievement 3]. 
> Key challenges include [challenge 1] and [challenge 2].
> Next month we will focus on [priority 1] and [priority 2].

---

## 📈 Financial Performance

### Revenue
| Metric | This Month | Last Month | Change | vs Budget |
|--------|------------|------------|--------|-----------|
| MRR | $XXX,XXX | $XXX,XXX | +X% | +X% |
| New Revenue | $XX,XXX | $XX,XXX | +X% | |
| Expansion | $X,XXX | $X,XXX | +X% | |
| Contraction | $X,XXX | $X,XXX | -X% | |
| Churned | $X,XXX | $X,XXX | X% | |

### Revenue by Segment
```
Enterprise  ████████████████████████████████ $XXX,XXX (XX%)
Mid-Market  ████████████████████ $XXX,XXX (XX%)
SMB         ██████████ $XXX,XXX (XX%)
```

### Unit Economics
- **CAC**: $XXX (↑X%)
- **LTV**: $X,XXX (↑X%)
- **LTV/CAC Ratio**: X.Xx
- **Payback Period**: X months
- **Gross Margin**: XX%

---

## 👥 Customer Metrics

### Growth
| Metric | Value | Change |
|--------|-------|--------|
| Total Customers | X,XXX | +XXX |
| New Customers | XXX | +XX |
| Churned Customers | XX | -X |
| Net Revenue Retention | XXX% | +X% |

### Engagement
- **DAU**: X,XXX (↑X%)
- **MAU**: XX,XXX (↑X%)
- **DAU/MAU Ratio**: XX% (sticky metric)
- **Avg Session Duration**: XX min
- **Feature Adoption**: XX%

### Satisfaction
- **NPS**: XX (↑X)
- **CSAT**: X.X/5 (↑X.X)
- **Support Tickets**: XXX (↓XX)
- **Ticket Satisfaction**: X.X/5

---

## 🚀 Product Updates

### Releases This Month
1. **Version X.X** - [Key feature]
   - Impact: [Metric change]
   - Adoption: XX%

2. **Version X.X** - [Key feature]
   - Impact: [Metric change]
   - Adoption: XX%

### Feature Usage
| Feature | Adoption | Engagement | Impact |
|---------|----------|------------|--------|
| Feature A | XX% | High | Positive |
| Feature B | XX% | Medium | Neutral |
| Feature C | XX% | Low | Negative |

### Technical Metrics
- **Uptime**: XX.XX%
- **Avg Response Time**: XXXms
- **Bug Count**: XX (↓X)
- **Security Incidents**: X

---

## 📣 Marketing Performance

### Lead Generation
| Channel | Leads | MQLs | Cost | CPL |
|---------|-------|------|------|-----|
| Organic | XXX | XX | $0 | $0 |
| Paid | XXX | XX | $X,XXX | $XX |
| Events | XX | X | $X,XXX | $XXX |
| Referral | XX | XX | $X,XXX | $XX |

### Content Performance
- **Blog Posts**: X (XXK views)
- **Webinars**: X (XXX attendees)
- **Social Engagement**: XX% (↑X%)
- **Email Open Rate**: XX% (↑X%)

### Website
- **Visitors**: XX,XXX
- **Conversion Rate**: X.X%
- **Demo Requests**: XXX
- **Free Trials**: XXX

---

## 💼 Sales Performance

### Pipeline
| Stage | Value | Count | Win Rate |
|-------|-------|-------|----------|
| New | $XXXK | XX | - |
| Qualified | $XXXK | XX | XX% |
| Proposal | $XXXK | XX | XX% |
| Negotiation | $XXXK | X | XX% |

### Performance
- **New ARR**: $XXX,XXX
- **Deals Closed**: XX
- **Avg Deal Size**: $XX,XXX
- **Sales Cycle**: XX days
- **Quota Attainment**: XX%

### Rep Performance
| Rep | Quota | Closed | Attainment |
|-----|-------|--------|------------|
| Rep A | $XXK | $XXK | XXX% |
| Rep B | $XXK | $XXK | XX% |

---

## ⚠️ Challenges & Risks

### Current Challenges
1. **[Challenge 1]**
   - Impact: [Description]
   - Mitigation: [Action plan]
   - Owner: [Name]

2. **[Challenge 2]**
   - Impact: [Description]
   - Mitigation: [Action plan]
   - Owner: [Name]

### Risks to Watch
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| | High/Med/Low | High/Med/Low | |

---

## 🎯 Next Month Priorities

### Top 3 Goals
1. **[Goal 1]**
   - Owner: [Name]
   - Target: [Metric]
   - Deadline: [Date]

2. **[Goal 2]**
   - Owner: [Name]
   - Target: [Metric]
   - Deadline: [Date]

3. **[Goal 3]**
   - Owner: [Name]
   - Target: [Metric]
   - Deadline: [Date]

### Key Initiatives
- [ ] [Initiative 1]
- [ ] [Initiative 2]
- [ ] [Initiative 3]

---

## 📊 Appendix: Detailed Charts

[Additional charts and data tables]

---

**Next Report**: [Date]
**Questions?**: Contact [Name] at [Email]
'''
    
    def _generate_datamodel(self) -> str:
        return '''# Data Model for BI

## Overview

This document outlines the data model for business intelligence reporting.

---

## Fact Tables

### fact_orders
```sql
CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    order_date DATE NOT NULL,
    user_id BIGINT NOT NULL,
    product_id BIGINT,
    amount DECIMAL(12,2) NOT NULL,
    quantity INT NOT NULL,
    discount_amount DECIMAL(12,2),
    tax_amount DECIMAL(12,2),
    total_amount DECIMAL(12,2) NOT NULL,
    currency_code VARCHAR(3),
    status VARCHAR(50),
    -- Foreign Keys
    date_id INT REFERENCES dim_date(date_id),
    user_segment_id INT REFERENCES dim_user_segment(segment_id),
    channel_id INT REFERENCES dim_channel(channel_id)
);
```

### fact_sessions
```sql
CREATE TABLE fact_sessions (
    session_id VARCHAR(100) PRIMARY KEY,
    session_date DATE NOT NULL,
    user_id BIGINT,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    duration_seconds INT,
    page_views INT,
    events INT,
    device_type VARCHAR(50),
    browser VARCHAR(100),
    os VARCHAR(100),
    country_code VARCHAR(2),
    is_conversion BOOLEAN,
    -- Foreign Keys
    date_id INT REFERENCES dim_date(date_id),
    channel_id INT REFERENCES dim_channel(channel_id)
);
```

### fact_support_tickets
```sql
CREATE TABLE fact_support_tickets (
    ticket_id BIGINT PRIMARY KEY,
    created_date DATE NOT NULL,
    resolved_date DATE,
    user_id BIGINT,
    category VARCHAR(100),
    priority VARCHAR(20),
    status VARCHAR(50),
    satisfaction_score INT,
    first_response_minutes INT,
    resolution_hours INT,
    agent_id BIGINT,
    -- Foreign Keys
    date_id INT REFERENCES dim_date(date_id)
);
```

---

## Dimension Tables

### dim_date
```sql
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week INT,
    day_name VARCHAR(10),
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_number INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    fiscal_quarter INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name VARCHAR(100)
);
```

### dim_users
```sql
CREATE TABLE dim_users (
    user_id BIGINT PRIMARY KEY,
    signup_date DATE,
    first_purchase_date DATE,
    last_active_date DATE,
    acquisition_channel VARCHAR(100),
    initial_plan VARCHAR(50),
    current_plan VARCHAR(50),
    country VARCHAR(100),
    region VARCHAR(100),
    company_size VARCHAR(50),
    industry VARCHAR(100),
    is_active BOOLEAN,
    lifetime_value DECIMAL(12,2)
);
```

### dim_products
```sql
CREATE TABLE dim_products (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(255),
    product_category VARCHAR(100),
    product_subcategory VARCHAR(100),
    unit_cost DECIMAL(12,2),
    unit_price DECIMAL(12,2),
    is_active BOOLEAN,
    created_date DATE
);
```

### dim_channel
```sql
CREATE TABLE dim_channel (
    channel_id INT PRIMARY KEY,
    channel_name VARCHAR(100),
    channel_type VARCHAR(50),
    channel_group VARCHAR(50),
    is_paid BOOLEAN,
    cost_per_click DECIMAL(8,4),
    is_active BOOLEAN
);
```

### dim_user_segment
```sql
CREATE TABLE dim_user_segment (
    segment_id INT PRIMARY KEY,
    segment_name VARCHAR(100),
    segment_criteria TEXT,
    avg_ltv DECIMAL(12,2),
    avg_engagement_score DECIMAL(5,2)
);
```

---

## Aggregate Tables

### agg_daily_metrics
```sql
CREATE TABLE agg_daily_metrics (
    date_id INT PRIMARY KEY,
    revenue DECIMAL(12,2),
    orders INT,
    new_users INT,
    active_users INT,
    sessions INT,
    conversion_rate DECIMAL(5,4),
    avg_order_value DECIMAL(12,2),
    support_tickets INT,
    avg_resolution_hours DECIMAL(6,2)
);
```

### agg_monthly_cohort_retention
```sql
CREATE TABLE agg_monthly_cohort_retention (
    cohort_month DATE,
    months_since_signup INT,
    cohort_size INT,
    active_users INT,
    retention_rate DECIMAL(5,4),
    PRIMARY KEY (cohort_month, months_since_signup)
);
```

---

## ETL Pipeline

### Daily Load Schedule
| Time | Job | Description |
|------|-----|-------------|
| 01:00 | Extract | Pull from source systems |
| 02:00 | Transform | Clean and transform data |
| 03:00 | Load | Load to warehouse |
| 04:00 | Aggregates | Build summary tables |
| 05:00 | Validation | Data quality checks |

### Data Quality Checks
- Row count validation
- Null checks
- Referential integrity
- Freshness checks
- Anomaly detection
'''


def main():
    parser = argparse.ArgumentParser(description="📈 BI-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = BIAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"📈 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
