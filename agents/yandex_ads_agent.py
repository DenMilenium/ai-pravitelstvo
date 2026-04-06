#!/usr/bin/env python3
"""
📢 YandexAds-Agent
Yandex Advertising Specialist

Создание и управление рекламными кампаниями в Яндекс Директ.
Анализ, оптимизация, автоматизация рекламы.
"""

import argparse
from pathlib import Path
from typing import Dict, List


class YandexAdsAgent:
    """
    📢 YandexAds-Agent
    
    Специализация: Yandex Direct Advertising
    Задачи: Создание кампаний, оптимизация, аналитика
    """
    
    NAME = "📢 YandexAds-Agent"
    ROLE = "Yandex Advertising Specialist"
    EXPERTISE = ["Yandex Direct", "Contextual Ads", "Campaign Management", "Budget Optimization", "Analytics"]
    
    API_ENDPOINT = "https://api.direct.yandex.com/json/v5"
    
    # Рекомендации по ставкам (в условных единицах)
    BID_RECOMMENDATIONS = {
        "low_competition": {
            "min_bid": 10,
            "recommended_bid": 25,
            "strategy": "Ручное управление с минимальными ставками"
        },
        "medium_competition": {
            "min_bid": 30,
            "recommended_bid": 60,
            "strategy": "Автоматические стратегии с ограничением"
        },
        "high_competition": {
            "min_bid": 80,
            "recommended_bid": 150,
            "strategy": "Агрессивный показ в поиске + ретаргетинг"
        }
    }
    
    # Шаблоны кампаний
    CAMPAIGN_TEMPLATES = {
        "brand_awareness": {
            "name": "Узнаваемость бренда",
            "description": "Максимальный охват целевой аудитории",
            "network": ["SEARCH", "YAN"],
            "strategy": "MAXIMUM_COVERAGE",
            "budget_type": "DAILY_BUDGET",
            "time_targeting": "WHOLE_WEEK"
        },
        "lead_generation": {
            "name": "Лидогенерация",
            "description": "Получение заявок и контактов",
            "network": ["SEARCH"],
            "strategy": "AVERAGE_CPC",
            "budget_type": "DAILY_BUDGET",
            "time_targeting": "BUSINESS_HOURS"
        },
        "sales_conversion": {
            "name": "Продажи",
            "description": "Максимум конверсий",
            "network": ["SEARCH", "YAN"],
            "strategy": "AVERAGE_CPA",
            "budget_type": "WEEKLY_BUDGET",
            "time_targeting": "WHOLE_WEEK"
        },
        "remarketing": {
            "name": "Ретаргетинг",
            "description": "Возврат посетителей сайта",
            "network": ["YAN"],
            "strategy": "AVERAGE_CPC",
            "budget_type": "DAILY_BUDGET",
            "time_targeting": "WHOLE_WEEK"
        }
    }
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["yandex-direct-api.py"] = self._generate_api_client()
        files["campaign-generator.js"] = self._generate_campaign_generator()
        files["ad-templates.md"] = self._generate_ad_templates()
        files["optimization-guide.md"] = self._generate_optimization_guide()
        files["budget-calculator.py"] = self._generate_budget_calculator()
        
        return files
    
    def _generate_api_client(self) -> str:
        return '''"""
Yandex Direct API Client
Клиент для управления рекламными кампаниями
"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class YandexDirectAPI:
    """Клиент API Яндекс Директ"""
    
    API_URL = "https://api.direct.yandex.com/json/v5"
    
    def __init__(self, token: str, client_login: Optional[str] = None):
        self.token = token
        self.client_login = client_login
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept-Language": "ru",
            "Content-Type": "application/json"
        })
        if client_login:
            self.session.headers["Client-Login"] = client_login
    
    def _make_request(self, service: str, method: str, params: Dict = None) -> Dict:
        """Выполнить запрос к API"""
        url = f"{self.API_URL}/{service}"
        
        payload = {
            "method": method,
            "params": params or {}
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    # === Кампании ===
    
    def get_campaigns(self, ids: Optional[List[int]] = None) -> List[Dict]:
        """Получить список кампаний"""
        params = {
            "SelectionCriteria": {},
            "FieldNames": ["Id", "Name", "Type", "Status", "State", 
                          "DailyBudget", "StartDate", "EndDate"]
        }
        
        if ids:
            params["SelectionCriteria"]["Ids"] = ids
        
        result = self._make_request("campaigns", "get", params)
        return result.get("result", {}).get("Campaigns", [])
    
    def create_campaign(self, campaign_data: Dict) -> Dict:
        """Создать рекламную кампанию"""
        params = {
            "Campaigns": [campaign_data]
        }
        
        return self._make_request("campaigns", "add", params)
    
    def update_campaign(self, campaign_id: int, updates: Dict) -> Dict:
        """Обновить кампанию"""
        params = {
            "Campaigns": [{
                "Id": campaign_id,
                **updates
            }]
        }
        
        return self._make_request("campaigns", "update", params)
    
    # === Объявления ===
    
    def get_ads(self, campaign_id: Optional[int] = None) -> List[Dict]:
        """Получить объявления"""
        params = {
            "SelectionCriteria": {},
            "FieldNames": ["Id", "CampaignId", "AdGroupId", "Status", 
                          "State", "Type"],
            "TextAdFieldNames": ["Title", "Text", "Href"]
        }
        
        if campaign_id:
            params["SelectionCriteria"]["CampaignIds"] = [campaign_id]
        
        result = self._make_request("ads", "get", params)
        return result.get("result", {}).get("Ads", [])
    
    def create_ad(self, ad_group_id: int, text_ad: Dict) -> Dict:
        """Создать текстовое объявление"""
        params = {
            "Ads": [{
                "AdGroupId": ad_group_id,
                "TextAd": text_ad
            }]
        }
        
        return self._make_request("ads", "add", params)
    
    # === Ключевые слова ===
    
    def get_keywords(self, ad_group_id: Optional[int] = None) -> List[Dict]:
        """Получить ключевые слова"""
        params = {
            "SelectionCriteria": {},
            "FieldNames": ["Id", "Keyword", "State", "Status", 
                          "Bid", "ContextBid", "StrategyPriority"]
        }
        
        if ad_group_id:
            params["SelectionCriteria"]["AdGroupIds"] = [ad_group_id]
        
        result = self._make_request("keywords", "get", params)
        return result.get("result", {}).get("Keywords", [])
    
    def add_keywords(self, ad_group_id: int, keywords: List[Dict]) -> Dict:
        """Добавить ключевые слова"""
        params = {
            "Keywords": [
                {
                    "AdGroupId": ad_group_id,
                    "Keyword": kw["keyword"],
                    "Bid": kw.get("bid"),
                    "ContextBid": kw.get("context_bid"),
                    "StrategyPriority": kw.get("priority", "NORMAL")
                }
                for kw in keywords
            ]
        }
        
        return self._make_request("keywords", "add", params)
    
    # === Отчёты ===
    
    def get_report(self, report_type: str, date_from: str, date_to: str) -> Dict:
        """Получить отчёт"""
        params = {
            "SelectionCriteria": {
                "DateFrom": date_from,
                "DateTo": date_to
            },
            "ReportName": f"Report_{date_from}_{date_to}",
            "ReportType": report_type,
            "DateRangeType": "CUSTOM_DATE",
            "Format": "TSV",
            "IncludeVAT": "YES",
            "IncludeDiscount": "NO",
            "FieldNames": ["CampaignName", "Clicks", "Impressions", 
                          "Cost", "Ctr", "AvgCpc", "AvgCpm", "Conversions"]
        }
        
        return self._make_request("reports", "get", params)
    
    # === Аналитика ===
    
    def get_campaign_stats(self, campaign_ids: List[int]) -> List[Dict]:
        """Получить статистику кампаний"""
        params = {
            "SelectionCriteria": {
                "CampaignIds": campaign_ids
            },
            "FieldNames": ["CampaignId", "CampaignName", "Clicks", 
                          "Impressions", "Cost", "Ctr", "AvgCpc"]
        }
        
        result = self._make_request("campaigns", "get", params)
        return result.get("result", {}).get("Campaigns", [])


class CampaignOptimizer:
    """Оптимизатор кампаний"""
    
    def __init__(self, api: YandexDirectAPI):
        self.api = api
    
    def analyze_performance(self, days: int = 30) -> Dict:
        """Анализ эффективности кампаний"""
        campaigns = self.api.get_campaigns()
        
        analysis = {
            "total_campaigns": len(campaigns),
            "active_campaigns": 0,
            "low_performers": [],
            "high_performers": [],
            "recommendations": []
        }
        
        for camp in campaigns:
            if camp.get("State") == "ON":
                analysis["active_campaigns"] += 1
            
            # Примерная логика анализа
            # В реальности нужны данные по кликам/конверсиям
        
        return analysis
    
    def optimize_bids(self, campaign_id: int, target_cpa: float) -> List[Dict]:
        """Оптимизировать ставки по целевой CPA"""
        keywords = self.api.get_keywords()
        
        changes = []
        
        for kw in keywords:
            current_bid = kw.get("Bid", 0) / 1000000  # Конвертация из микроединиц
            
            # Логика оптимизации
            if current_bid > target_cpa * 1.5:
                new_bid = int(target_cpa * 1000000)
                changes.append({
                    "keyword_id": kw["Id"],
                    "keyword": kw["Keyword"],
                    "old_bid": current_bid,
                    "new_bid": new_bid,
                    "action": "decrease"
                })
        
        return changes
    
    def get_budget_recommendations(self, monthly_budget: float) -> Dict:
        """Рекомендации по распределению бюджета"""
        daily_budget = monthly_budget / 30
        
        return {
            "search_campaigns": {
                "allocation": 0.6,
                "daily_budget": daily_budget * 0.6,
                "strategy": "Максимум кликов с ограничением CPC"
            },
            "display_campaigns": {
                "allocation": 0.3,
                "daily_budget": daily_budget * 0.3,
                "strategy": "Максимум конверсий"
            },
            "remarketing": {
                "allocation": 0.1,
                "daily_budget": daily_budget * 0.1,
                "strategy": "Ручное управление"
            }
        }


# Пример использования
if __name__ == "__main__":
    import os
    
    api = YandexDirectAPI(
        token=os.getenv("YANDEX_DIRECT_TOKEN"),
        client_login=os.getenv("YANDEX_CLIENT_LOGIN")
    )
    
    # Получить кампании
    campaigns = api.get_campaigns()
    print(f"Всего кампаний: {len(campaigns)}")
    
    for camp in campaigns[:5]:
        print(f"  - {camp['Name']} ({camp['Status']})")
'''
    
    def _generate_campaign_generator(self) -> str:
        return '''/**
 * Campaign Generator for Yandex Direct
 * Генератор рекламных кампаний
 */

class YandexCampaignGenerator {
  constructor() {
    this.templates = {
      brand: {
        name: (businessName) => `${businessName} — Официальный сайт`,
        titles: [
          "{businessName} — Официальный сайт",
          "{businessName} — Лучшие цены",
          "{businessName} — Быстрая доставка"
        ],
        texts: [
          "✓ Официальный дилер ✓ Гарантия ✓ Доставка по России",
          "⭐ Тысячи довольных клиентов ⭐ Скидки до 30%",
          "🎁 Подарки каждому покупателю 🎁 Рассрочка 0%"
        ]
      },
      
      ecommerce: {
        name: (category) => `Купить ${category} — Низкие цены`,
        titles: [
          "Купить {product} недорого",
          "{product} — Скидки до 50%",
          "{product} в наличии — Доставка сегодня"
        ],
        texts: [
          "✓ В наличии ✓ Доставка 1-3 дня ✓ Оплата при получении",
          "💰 Лучшие цены 💰 Гарантия 2 года 💰 Возврат 14 дней",
          "🏪 50+ магазинов 🏪 Самовывоз бесплатно"
        ]
      },
      
      service: {
        name: (service) => `{service} — Заказать услугу`,
        titles: [
          "{service} — Заказать в {city}",
          "{service} — Цены от {price}₽",
          "{service} — Выезд за 1 час"
        ],
        texts: [
          "✓ Опыт 10+ лет ✓ Гарантия результата ✓ Бесплатный выезд",
          "⭐ 500+ отзывов ⭐ Работаем 24/7 ⭐ Скидка 20%",
          "📞 Звоните прямо сейчас 📞 Рассрочка без %"
        ]
      }
    };
  }
  
  generateCampaign(campaignType, params) {
    const template = this.templates[campaignType];
    if (!template) {
      throw new Error(`Unknown campaign type: ${campaignType}`);
    }
    
    return {
      name: this.interpolate(template.name(params.businessName), params),
      ads: this.generateAds(template, params),
      keywords: this.generateKeywords(params),
      targeting: this.generateTargeting(params),
      budget: this.calculateBudget(params.monthlyBudget)
    };
  }
  
  interpolate(template, params) {
    return template.replace(/{(\\w+)}/g, (match, key) => params[key] || match);
  }
  
  generateAds(template, params) {
    const ads = [];
    
    for (const title of template.titles) {
      for (const text of template.texts) {
        ads.push({
          title: this.interpolate(title, params),
          text: this.interpolate(text, params),
          href: params.landingUrl,
          callouts: params.callouts || ["Бесплатная доставка", "Гарантия", "Скидки"],
          sitelinks: params.sitelinks || [
            { title: "Каталог", href: `${params.landingUrl}/catalog` },
            { title: "Акции", href: `${params.landingUrl}/sale` },
            { title: "Контакты", href: `${params.landingUrl}/contacts` }
          ]
        });
      }
    }
    
    return ads;
  }
  
  generateKeywords(params) {
    const { product, category, city, synonyms = [] } = params;
    
    const keywords = [
      // Точное соответствие
      { keyword: `"купить ${product}"`, bid: 50 },
      { keyword: `"${product} цена"`, bid: 45 },
      
      // Фразовое соответствие
      { keyword: `купить ${category}`, bid: 40 },
      { keyword: `${category} недорого`, bid: 35 },
      { keyword: `${product} ${city}`, bid: 30 },
      
      // Модификатор широкого соответствия
      { keyword: `+купить +${category}`, bid: 25 },
    ];
    
    // Добавляем синонимы
    for (const syn of synonyms) {
      keywords.push({ keyword: syn, bid: 30 });
    }
    
    // Минус-слова
    const negativeKeywords = [
      "бесплатно", "самодельный", "diy", "как сделать",
      "чертеж", "схема", "взлом", "кряк", "торрент"
    ];
    
    return { positive: keywords, negative: negativeKeywords };
  }
  
  generateTargeting(params) {
    return {
      geo: {
        regions: params.regions || [1], // Москва по умолчанию
        showInConnectedRegions: true
      },
      time: {
        schedule: [
          { days: [1,2,3,4,5], hours: [9,10,11,12,13,14,15,16,17,18,19,20,21,22] },
          { days: [6,7], hours: [10,11,12,13,14,15,16,17,18,19,20] }
        ],
        timezone: "Europe/Moscow"
      },
      demographics: {
        age: params.targetAge || ["25-34", "35-44"],
        gender: params.targetGender || ["MALE", "FEMALE"]
      },
      devices: {
        desktop: true,
        mobile: true,
        tablet: true
      }
    };
  }
  
  calculateBudget(monthlyBudget) {
    const daily = Math.round(monthlyBudget / 30);
    
    return {
      daily: daily,
      weekly: daily * 7,
      monthly: monthlyBudget,
      distribution: {
        search: Math.round(monthlyBudget * 0.6),
        display: Math.round(monthlyBudget * 0.3),
        remarketing: Math.round(monthlyBudget * 0.1)
      }
    };
  }
  
  // A/B тестирование объявлений
  generateABTest(ads) {
    const variants = [];
    
    for (let i = 0; i < ads.length; i++) {
      variants.push({
        id: `ad_${i + 1}`,
        ...ads[i],
        utm: `utm_content=variant_${i + 1}`
      });
    }
    
    return {
      testId: `ab_test_${Date.now()}`,
      variants: variants,
      metrics: ["ctr", "conversion_rate", "cost_per_conversion"],
      duration: 14 // дней
    };
  }
}


// Пример использования
const generator = new YandexCampaignGenerator();

const campaign = generator.generateCampaign("ecommerce", {
  businessName: "ТехноМаркет",
  product: "iPhone 15 Pro",
  category: "смартфоны",
  city: "Москва",
  landingUrl: "https://technomarket.ru/iphone-15",
  monthlyBudget: 150000,
  regions: [1, 2], // Москва, СПб
  synonyms: ["айфон 15", "iphone 15 pro max", "apple iphone"]
});

console.log("Campaign:", JSON.stringify(campaign, null, 2));

module.exports = YandexCampaignGenerator;
'''
    
    def _generate_ad_templates(self) -> str:
        return '''# Шаблоны объявлений Яндекс Директ

## 📱 E-commerce (Интернет-магазин)

### Шаблон 1: Продуктовая кампания
```
Заголовок 1: Купить {product} — {price}₽
Заголовок 2: {product} в наличии — Доставка сегодня
Текст: ✓ Официальная гарантия ✓ Доставка 1-3 дня ✓ Оплата при получении

Быстрые ссылки:
- Все модели → /catalog/{category}
- Акции → /sale
- Отзывы → /reviews
- Доставка → /delivery

Уточнения:
• Бесплатная доставка
• Гарантия 2 года
• Рассрочка 0%
• 50+ магазинов
```

### Шаблон 2: Распродажа
```
Заголовок 1: {category} — Скидки до {discount}%
Заголовок 2: Распродажа {product} — Успей купить!
Текст: 🔥 Только {date} 🔥 Ограниченное количество 🔥 Гарантия лучшей цены
```

## 🏢 Услуги (B2C)

### Шаблон 1: Местные услуги
```
Заголовок 1: {service} в {city} — от {price}₽
Заголовок 2: {service} — Выезд мастера за {time}
Текст: ✓ Опыт 10+ лет ✓ Гарантия результата ✓ Работаем 24/7

Визитка:
📞 {phone}
📍 {address}
🕐 {working_hours}
```

### Шаблон 2: Консультация
```
Заголовок 1: {service} — Бесплатная консультация
Заголовок 2: Профессиональный {specialist} в {city}
Текст: ⭐ 500+ довольных клиентов ⭐ Решение за 1 день ⭐ Договор
```

## 🎓 Образование / Курсы

```
Заголовок 1: {course_name} — Запишись сейчас
Заголовок 2: Обучение {skill} — С нуля до профи
Текст: 🎓 Практические занятия 🎓 Сертификат 🎓 Трудоустройство

Уточнения:
• Дистанционно
• Опытные преподаватели
• Помощь с трудоустройством
• Рассрочка оплаты
```

## 🏥 Медицина

```
Заголовок 1: {service} — Запись онлайн
Заголовок 2: {clinic_name} — {specialty}
Текст: ✓ Лицензия ✓ Современное оборудование ✓ Опытные врачи

Визитка:
📞 Запись: {phone}
📍 {address}
🕐 Пн-Сб: 8:00-20:00
```

## ⚠️ Минус-слова (универсальные)

### Для e-commerce:
```
-бесплатно -самодельный -diy -как сделать -чертеж -схема
-взлом -кряк -торрент -игрушка -детский -играть -кукла
-б/у -буу -used -secondhand -разбитый -неисправный
```

### Для услуг:
```
-вакансия -требуется -работа -ищу работу -резюме
-бесплатно -без опыта -стажер -стажировка
-купить -продать -цена
```

## 🎯 Структура успешной кампании

### 1. Группы объявлений (Ad Groups)

| Группа | Ключевые слова | Ставка |
|--------|----------------|--------|
| Точное соответствие | [купить айфон] | Высокая |
| Фразовое соответствие | "айфон цена" | Средняя |
| Широкое соответствие | айфон москва | Низкая |
| Конкуренты | iphone samsung | Средняя |

### 2. Распределение бюджета

```
Поиск: 60%
  └── Точное: 40%
  └── Фразовое: 20%
РСЯ: 30%
  └── Тематические: 20%
  └── Ретаргетинг: 10%
Ретаргетинг: 10%
```

### 3. UTM-метки

```
?utm_source=yandex&utm_medium=cpc&utm_campaign={campaign_id}&utm_content={ad_id}&utm_term={keyword}
```

## 📊 Ключевые метрики

| Метрика | Хорошо | Отлично |
|---------|--------|---------|
| CTR | > 5% | > 10% |
| CPC | < 50₽ | < 30₽ |
| Конверсия | > 2% | > 5% |
| ДРР | < 20% | < 15% |

---

**Создано:** YandexAds-Agent v1.0
'''
    
    def _generate_optimization_guide(self) -> str:
        return '''# Руководство по оптимизации Яндекс Директ

## 🚀 Быстрый старт (первые 2 недели)

### День 1-3: Сбор данных
- [ ] Запустить кампании с 20-30% выше рекомендуемых ставок
- [ ] Включить все площадки (Поиск + РСЯ)
- [ ] Установить корректировки: Москва +20%, мобильные +10%

### День 4-7: Первый анализ
- [ ] Выключить площадки с CTR < 0.5%
- [ ] Добавить минус-слова (см. отчёт "Поисковые запросы")
- [ ] Увеличить ставки на ключи с высокой конверсией

### День 8-14: Оптимизация
- [ ] A/B тестирование объявлений
- [ ] Корректировка по времени суток
- [ ] Добавление ретаргетинга

## 📈 Еженедельный чеклист

### Понедельник: Анализ
```
1. Проверить ДРР по кампаниям
2. Выгрузить отчёт по конверсиям
3. Сравнить с прошлой неделей
4. Определить топ-5 и аутсайдеров
```

### Среда: Корректировки
```
1. Обновить минус-слова
2. Проверить посадочные страницы
3. Протестировать новые объявления
4. Корректировка ставок
```

### Пятница: Планирование
```
1. Проверить бюджет на выходные
2. Запланировать новые кампании
3. Подготовить рекламные материалы
```

## 🎯 Стратегии назначения ставок

### 1. Ручное управление
**Когда:** Начало работы, небольшие бюджеты
```
Ставка = Средняя по нише × 1.2
```

### 2. Средняя цена клика
**Когда:** Стабильная кампания, известный CPC
```
Целевой CPC = 80% от максимально допустимого
```

### 3. Средняя цена конверсии (CPA)
**Когда:** Есть статистика конверсий
```
Целевой CPA = Допустимая стоимость лида
```

### 4. Оптимизация конверсий
**Когда:** 50+ конверсий в неделю
```
Автоматическая, задаёте только бюджет
```

## 🔧 Автоматические правила

### Правило 1: Пауза низкопроизводительных
```
ЕСЛИ: CTR < 1% за 7 дней И показы > 1000
ТО: Поставить на паузу
```

### Правило 2: Повышение ставок
```
ЕСЛИ: Конверсия > 3% И ДРР < 15%
ТО: Увеличить ставку на 20%
```

### Правило 3: Снижение ставок
```
ЕСЛИ: ДРР > 30% за 3 дня
ТО: Уменьшить ставку на 30%
```

## 📊 Как снизить стоимость клика

### 1. Качество объявлений
- [ ] Уникальные торговые предложения
- [ ] Цифры и конкретика («от 2990₽»)
- [ ] Призыв к действию
- [ ] Релевантность ключевым словам

### 2. Расширения
- [ ] Быстрые ссылки (минимум 4)
- [ ] Уточнения (минимум 4)
- [ ] Визитка с адресом
- [ ] Структурированные описания

### 3. Минус-слова
- [ ] Ежедневный просмотр поисковых запросов
- [ ] Добавление нерелевантных
- [ ] Создание общего списка

## 🚨 Частые ошибки

### ❌ Ошибка 1: Слишком широкие ключи
**Решение:** Использовать точное и фразовое соответствие

### ❌ Ошибка 2: Нет минус-слов
**Решение:** Добавить минимум 50-100 минус-слов перед запуском

### ❌ Ошибка 3: Одно объявление на группу
**Решение:** Минимум 3 объявления для A/B теста

### ❌ Ошибка 4: Отсутствие аналитики
**Решение:** Настроить цели в Метрике и передавать в Директ

### ❌ Ошибка 5: Неправильное гео
**Решение:** Указывать регионы продаж, а не присутствия

## 💡 Лайфхаки

### Поиск
- Используйте ключи с уточнением «купить», «цена», «заказать»
- Ставьте выше ставки на коммерческие запросы
- Используйте минус-слова для информационных запросов

### РСЯ
- Работайте с аудиториями Look-alike
- Используйте ретаргетинг
- Создавайте отдельные объявления для РСЯ (более "мягкие")

### Ретаргетинг
- Сегментируйте по глубине просмотра
- Разные сообщения для разных этапов воронки
- Частота показа: макс. 3 раза в день

## 📅 График оптимизации

| Период | Действие |
|--------|----------|
| Каждый день | Проверка бюджета и статуса |
| Раз в 2 дня | Добавление минус-слов |
| Раз в неделю | Анализ конверсий, корректировка ставок |
| Раз в 2 недели | A/B тесты объявлений |
| Раз в месяц | Пересмотр стратегии, бюджета |

---

**Важно:** Дайте кампании набрать 1000+ кликов перед серьёзными изменениями!
'''
    
    def _generate_budget_calculator(self) -> str:
        return '''#!/usr/bin/env python3
"""
Yandex Direct Budget Calculator
Калькулятор бюджета рекламных кампаний
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


class BusinessType(Enum):
    ECOMMERCE = "ecommerce"
    SERVICES = "services"
    B2B = "b2b"
    EDUCATION = "education"


@dataclass
class CampaignBudget:
    """Бюджет кампании"""
    name: str
    daily: float
    monthly: float
    cpc_target: float
    conversion_rate: float
    expected_conversions: int


class BudgetCalculator:
    """Калькулятор бюджета Яндекс Директ"""
    
    # Средние показатели по нишам
    BENCHMARKS = {
        BusinessType.ECOMMERCE: {
            "avg_cpc": 25,
            "conversion_rate": 0.02,
            "cpa_target": 1250
        },
        BusinessType.SERVICES: {
            "avg_cpc": 80,
            "conversion_rate": 0.05,
            "cpa_target": 1600
        },
        BusinessType.B2B: {
            "avg_cpc": 120,
            "conversion_rate": 0.03,
            "cpa_target": 4000
        },
        BusinessType.EDUCATION: {
            "avg_cpc": 45,
            "conversion_rate": 0.04,
            "cpa_target": 1125
        }
    }
    
    def __init__(self, business_type: BusinessType):
        self.business_type = business_type
        self.benchmark = self.BENCHMARKS[business_type]
    
    def calculate_for_target(
        self,
        target_leads: int,
        cost_per_lead: float = None
    ) -> CampaignBudget:
        """
        Расчёт бюджета для целевого количества лидов
        
        Args:
            target_leads: Целевое количество лидов в месяц
            cost_per_lead: Допустимая стоимость лида
        """
        cpa = cost_per_lead or self.benchmark["cpa_target"]
        monthly_budget = target_leads * cpa
        daily_budget = monthly_budget / 30
        
        # Расчёт кликов
        clicks_needed = target_leads / self.benchmark["conversion_rate"]
        cpc_needed = monthly_budget / clicks_needed if clicks_needed > 0 else 0
        
        return CampaignBudget(
            name=f"Target: {target_leads} leads/month",
            daily=round(daily_budget, 2),
            monthly=round(monthly_budget, 2),
            cpc_target=round(cpc_needed, 2),
            conversion_rate=self.benchmark["conversion_rate"],
            expected_conversions=target_leads
        )
    
    def calculate_for_budget(self, monthly_budget: float) -> CampaignBudget:
        """
        Расчёт ожидаемых результатов для заданного бюджета
        
        Args:
            monthly_budget: Месячный бюджет
        """
        daily_budget = monthly_budget / 30
        
        # Ожидаемое количество кликов
        expected_clicks = monthly_budget / self.benchmark["avg_cpc"]
        
        # Ожидаемое количество конверсий
        expected_conversions = int(expected_clicks * self.benchmark["conversion_rate"])
        
        # Фактическая стоимость конверсии
        actual_cpa = monthly_budget / expected_conversions if expected_conversions > 0 else 0
        
        return CampaignBudget(
            name=f"Budget: {monthly_budget:,.0f}₽/month",
            daily=round(daily_budget, 2),
            monthly=round(monthly_budget, 2),
            cpc_target=self.benchmark["avg_cpc"],
            conversion_rate=self.benchmark["conversion_rate"],
            expected_conversions=expected_conversions
        )
    
    def distribute_budget(self, monthly_budget: float) -> Dict[str, float]:
        """
        Распределение бюджета по каналам
        
        Args:
            monthly_budget: Общий бюджет
        """
        if self.business_type == BusinessType.ECOMMERCE:
            return {
                "search_brand": monthly_budget * 0.15,
                "search_generic": monthly_budget * 0.30,
                "search_competitor": monthly_budget * 0.10,
                "rsya_thematic": monthly_budget * 0.25,
                "rsya_retargeting": monthly_budget * 0.15,
                "remarketing": monthly_budget * 0.05
            }
        elif self.business_type == BusinessType.SERVICES:
            return {
                "search_high_intent": monthly_budget * 0.45,
                "search_medium_intent": monthly_budget * 0.20,
                "rsya_retargeting": monthly_budget * 0.25,
                "remarketing": monthly_budget * 0.10
            }
        else:
            return {
                "search": monthly_budget * 0.60,
                "rsya": monthly_budget * 0.30,
                "remarketing": monthly_budget * 0.10
            }
    
    def generate_recommendations(self, monthly_budget: float) -> List[str]:
        """Генерация рекомендаций"""
        recs = []
        
        if monthly_budget < 30000:
            recs.append("💡 Рекомендуется минимум 30,000₽/мес для получения статистики")
        
        if monthly_budget < 50000:
            recs.append("💡 Сфокусируйтесь на поиске, отключите РСЯ")
        
        if self.business_type == BusinessType.ECOMMERCE and monthly_budget > 100000:
            recs.append("✅ Можно запускать Smart Banners")
        
        recs.append(f"📊 Ожидаемая конверсия: {self.benchmark['conversion_rate']*100:.1f}%")
        recs.append(f"📊 Целевой CPC: {self.benchmark['avg_cpc']}₽")
        
        return recs


def main():
    print("📢 Yandex Direct Budget Calculator")
    print("=" * 50)
    
    # Примеры расчётов
    for business_type in BusinessType:
        print(f"\\n{business_type.value.upper()}:")
        calc = BudgetCalculator(business_type)
        
        # Расчёт для бюджета 50,000₽
        result = calc.calculate_for_budget(50000)
        print(f"  Бюджет 50,000₽/мес:")
        print(f"    - Дневной: {result.daily:,.0f}₽")
        print(f"    - Ожидается лидов: {result.expected_conversions}")
        print(f"    - Стоимость лида: ~{result.monthly/max(result.expected_conversions,1):,.0f}₽")
        
        # Распределение
        distribution = calc.distribute_budget(50000)
        print(f"  Распределение:")
        for channel, amount in distribution.items():
            print(f"    - {channel}: {amount:,.0f}₽")


if __name__ == "__main__":
    main()
'''


def main():
    parser = argparse.ArgumentParser(description="📢 YandexAds-Agent")
    parser.add_argument("request", nargs="?", help="Задача")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = YandexAdsAgent()
    
    if args.request:
        print(f"📢 {agent.NAME} создаёт: {args.request}")
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
                print(f"\\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"📢 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\\nAPI: {agent.API_ENDPOINT}")
        print(f"\\nШаблоны кампаний:")
        for name in agent.CAMPAIGN_TEMPLATES.keys():
            print(f"  - {name}")


if __name__ == "__main__":
    main()
