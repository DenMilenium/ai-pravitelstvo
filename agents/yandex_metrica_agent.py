#!/usr/bin/env python3
"""
📊 YandexMetrica-Agent
Yandex Metrica Analytics Specialist

Настройка аналитики, целей, вебвизора.
Отслеживание конверсий и поведения пользователей.
"""

import argparse
from pathlib import Path
from typing import Dict


class YandexMetricaAgent:
    """
    📊 YandexMetrica-Agent
    
    Специализация: Yandex Metrica Analytics
    Задачи: Цели, вебвизор, отчёты, интеграция
    """
    
    NAME = "📊 YandexMetrica-Agent"
    ROLE = "Yandex Metrica Specialist"
    EXPERTISE = ["Yandex Metrica", "Web Analytics", "Goals Setup", "Webvisor", "E-commerce"]
    
    API_ENDPOINT = "https://api-metrika.yandex.net"
    
    # Шаблоны целей
    GOAL_TEMPLATES = {
        "form_submit": {
            "name": "Отправка формы",
            "type": "action",
            "conditions": ["event"],
            "priority": "high"
        },
        "phone_click": {
            "name": "Клик по телефону",
            "type": "action", 
            "conditions": ["event"],
            "priority": "high"
        },
        "purchase": {
            "name": "Покупка",
            "type": "action",
            "conditions": ["url"],
            "priority": "high"
        },
        "add_to_cart": {
            "name": "Добавление в корзину",
            "type": "action",
            "conditions": ["event"],
            "priority": "medium"
        },
        "scroll_75": {
            "name": "Прокрутка 75%",
            "type": "action",
            "conditions": ["event"],
            "priority": "low"
        },
        "time_3min": {
            "name": "Время на сайте 3 мин",
            "type": "action",
            "conditions": ["event"],
            "priority": "low"
        }
    }
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["metrica-setup.js"] = self._generate_tracking_code()
        files["goals-config.json"] = self._generate_goals_config()
        files["ecommerce-tracking.js"] = self._generate_ecommerce()
        files["analytics-dashboard.py"] = self._generate_dashboard()
        files["setup-guide.md"] = self._generate_setup_guide()
        
        return files
    
    def _generate_tracking_code(self) -> str:
        return '''/**
 * Yandex Metrica Tracking Setup
 * Настройка отслеживания Яндекс Метрика
 */

// Основной код Метрики (вставить в <head>)
const metricaCode = (counterId) => `
<!-- Yandex.Metrika counter -->
<script type="text/javascript" >
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();
   for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

   ym(${counterId}, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true,
        ecommerce:"dataLayer"
   });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/${counterId}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
`;

/**
 * Отправка цели в Метрику
 */
class YandexMetrica {
  constructor(counterId) {
    this.counterId = counterId;
  }
  
  /**
   * Достигнута цель
   * @param {string} targetName - Имя цели (например: 'form_submit')
   * @param {object} params - Дополнительные параметры
   */
  reachGoal(targetName, params = {}) {
    if (typeof ym !== 'undefined') {
      ym(this.counterId, 'reachGoal', targetName, params);
      console.log(`[Metrica] Goal reached: ${targetName}`, params);
    } else {
      console.warn('[Metrica] ym not loaded');
    }
  }
  
  /**
   * Параметры визита
   * @param {object} params - Параметры
   */
  params(params) {
    if (typeof ym !== 'undefined') {
      ym(this.counterId, 'params', params);
    }
  }
  
  /**
   * Просмотр страницы (для SPA)
   * @param {string} url - URL страницы
   * @param {string} title - Заголовок
   */
  hit(url, title) {
    if (typeof ym !== 'undefined') {
      ym(this.counterId, 'hit', url, {
        title: title,
        referer: document.referrer
      });
    }
  }
  
  /**
   * Отправка события электронной коммерции
   * @param {string} type - Тип события (detail, add, purchase)
   * @param {object} data - Данные о товаре/заказе
   */
  ecommerce(type, data) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      ecommerce: {
        [type]: {
          products: Array.isArray(data) ? data : [data]
        }
      }
    });
    
    // Отправка вручную, если автоматическая отправка отключена
    if (typeof ym !== 'undefined') {
      ym(this.counterId, 'ecommerce', type, data);
    }
  }
}

/**
 * Автоматическое отслеживание событий
 */
class AutoTracker {
  constructor(metrica) {
    this.metrica = metrica;
    this.init();
  }
  
  init() {
    this.trackForms();
    this.trackPhones();
    this.trackEmails();
    this.trackScroll();
    this.trackTime();
    this.trackOutboundLinks();
  }
  
  /**
   * Отслеживание отправки форм
   */
  trackForms() {
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', (e) => {
        const formName = form.getAttribute('name') || form.getAttribute('id') || 'unnamed';
        this.metrica.reachGoal('form_submit', {
          form_name: formName,
          form_id: form.id
        });
      });
    });
  }
  
  /**
   * Отслеживание кликов по телефонам
   */
  trackPhones() {
    document.querySelectorAll('a[href^="tel:"]').forEach(link => {
      link.addEventListener('click', () => {
        const phone = link.getAttribute('href').replace('tel:', '');
        this.metrica.reachGoal('phone_click', { phone });
      });
    });
  }
  
  /**
   * Отслеживание кликов по email
   */
  trackEmails() {
    document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
      link.addEventListener('click', () => {
        this.metrica.reachGoal('email_click');
      });
    });
  }
  
  /**
   * Отслеживание прокрутки
   */
  trackScroll() {
    let scrolled25 = false;
    let scrolled50 = false;
    let scrolled75 = false;
    let scrolled90 = false;
    
    window.addEventListener('scroll', () => {
      const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
      
      if (scrollPercent > 25 && !scrolled25) {
        this.metrica.reachGoal('scroll_25');
        scrolled25 = true;
      }
      if (scrollPercent > 50 && !scrolled50) {
        this.metrica.reachGoal('scroll_50');
        scrolled50 = true;
      }
      if (scrollPercent > 75 && !scrolled75) {
        this.metrica.reachGoal('scroll_75');
        scrolled75 = true;
      }
      if (scrollPercent > 90 && !scrolled90) {
        this.metrica.reachGoal('scroll_90');
        scrolled90 = true;
      }
    });
  }
  
  /**
   * Отслеживание времени на сайте
   */
  trackTime() {
    setTimeout(() => {
      this.metrica.reachGoal('time_30sec');
    }, 30000);
    
    setTimeout(() => {
      this.metrica.reachGoal('time_1min');
    }, 60000);
    
    setTimeout(() => {
      this.metrica.reachGoal('time_3min');
    }, 180000);
  }
  
  /**
   * Отслеживание внешних ссылок
   */
  trackOutboundLinks() {
    document.querySelectorAll('a[href^="http"]').forEach(link => {
      if (!link.href.includes(window.location.hostname)) {
        link.addEventListener('click', () => {
          this.metrica.reachGoal('outbound_link', {
            url: link.href
          });
        });
      }
    });
  }
}

// Использование
const counterId = 'YOUR_COUNTER_ID';
const metrica = new YandexMetrica(counterId);
const autoTracker = new AutoTracker(metrica);

// Экспорт для использования в других модулях
export { YandexMetrica, AutoTracker, metricaCode };
'''
    
    def _generate_goals_config(self) -> str:
        return '''{
  "counter_id": "YOUR_COUNTER_ID",
  "goals": [
    {
      "id": 1,
      "name": "Отправка формы обратной связи",
      "type": "action",
      "conditions": [
        {
          "type": "event",
          "event": "form_submit"
        }
      ],
      "is_retargeting": true
    },
    {
      "id": 2,
      "name": "Клик по телефону",
      "type": "action",
      "conditions": [
        {
          "type": "event",
          "event": "phone_click"
        }
      ],
      "is_retargeting": true
    },
    {
      "id": 3,
      "name": "Покупка (спасибо за заказ)",
      "type": "url",
      "conditions": [
        {
          "type": "url",
          "url": "thank-you",
          "operator": "contains"
        }
      ],
      "is_retargeting": true
    },
    {
      "id": 4,
      "name": "Добавление в корзину",
      "type": "action",
      "conditions": [
        {
          "type": "event",
          "event": "add_to_cart"
        }
      ],
      "is_retargeting": true
    },
    {
      "id": 5,
      "name": "Переход в корзину",
      "type": "url",
      "conditions": [
        {
          "type": "url",
          "url": "/cart",
          "operator": "contains"
        }
      ],
      "is_retargeting": false
    },
    {
      "id": 6,
      "name": "Начало оформления заказа",
      "type": "url",
      "conditions": [
        {
          "type": "url",
          "url": "/checkout",
          "operator": "contains"
        }
      ],
      "is_retargeting": true
    },
    {
      "id": 7,
      "name": "Прокрутка 75%",
      "type": "action",
      "conditions": [
        {
          "type": "event",
          "event": "scroll_75"
        }
      ],
      "is_retargeting": false
    },
    {
      "id": 8,
      "name": "Время на сайте 3 минуты",
      "type": "action",
      "conditions": [
        {
          "type": "event",
          "event": "time_3min"
        }
      ],
      "is_retargeting": false
    },
    {
      "id": 9,
      "name": "Подписка на рассылку",
      "type": "action",
      "conditions": [
        {
          "type": "event",
          "event": "newsletter_subscribe"
        }
      ],
      "is_retargeting": true
    },
    {
      "id": 10,
      "name": "Скачивание прайса",
      "type": "action",
      "conditions": [
        {
          "type": "event",
          "event": "price_download"
        }
      ],
      "is_retargeting": false
    }
  ],
  "filters": {
    "exclude_ips": ["192.168.1.1", "10.0.0.0/8"],
    "exclude_referrers": ["localhost", "test.mysite.ru"],
    "url_filter": {
      "type": "contains",
      "value": "utm_source"
    }
  },
  "params": {
    "visit_duration": true,
    "bounce_rate": true,
    "page_depth": true
  }
}
'''
    
    def _generate_ecommerce(self) -> str:
        return '''/**
 * Yandex Metrica E-commerce Tracking
 * Отслеживание электронной коммерции
 */

/**
 * Добавление товара в корзину
 */
function trackAddToCart(product) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    ecommerce: {
      add: {
        products: [{
          id: product.id,
          name: product.name,
          price: product.price,
          brand: product.brand,
          category: product.category,
          variant: product.variant,
          quantity: product.quantity || 1
        }]
      }
    }
  });
  
  // Цель для ретаргетинга
  if (typeof ym !== 'undefined') {
    ym(YOUR_COUNTER_ID, 'reachGoal', 'add_to_cart');
  }
}

/**
 * Удаление из корзины
 */
function trackRemoveFromCart(product) {
  window.dataLayer.push({
    ecommerce: {
      remove: {
        products: [{
          id: product.id,
          name: product.name,
          price: product.price,
          quantity: product.quantity
        }]
      }
    }
  });
}

/**
 * Просмотр деталей товара
 */
function trackProductDetail(product) {
  window.dataLayer.push({
    ecommerce: {
      detail: {
        products: [{
          id: product.id,
          name: product.name,
          price: product.price,
          brand: product.brand,
          category: product.category
        }]
      }
    }
  });
}

/**
 * Просмотр категории
 */
function trackCategoryView(category, products) {
  window.dataLayer.push({
    ecommerce: {
      impressions: products.map((p, index) => ({
        id: p.id,
        name: p.name,
        price: p.price,
        brand: p.brand,
        category: category,
        list: category,
        position: index + 1
      }))
    }
  });
}

/**
 * Оформление покупки (шаги)
 */
function trackCheckoutStep(step, products, options = {}) {
  const stepNames = {
    1: 'Корзина',
    2: 'Контактные данные',
    3: 'Доставка',
    4: 'Оплата',
    5: 'Подтверждение'
  };
  
  window.dataLayer.push({
    ecommerce: {
      checkout: {
        actionField: {
          step: step,
          option: stepNames[step]
        },
        products: products.map(p => ({
          id: p.id,
          name: p.name,
          price: p.price,
          quantity: p.quantity
        }))
      }
    }
  });
}

/**
 * Успешная покупка
 */
function trackPurchase(order) {
  window.dataLayer.push({
    ecommerce: {
      purchase: {
        actionField: {
          id: order.id,
          revenue: order.revenue,
          tax: order.tax || 0,
          shipping: order.shipping || 0,
          coupon: order.coupon || ''
        },
        products: order.products.map(p => ({
          id: p.id,
          name: p.name,
          price: p.price,
          brand: p.brand,
          category: p.category,
          variant: p.variant,
          quantity: p.quantity,
          coupon: p.coupon || ''
        }))
      }
    }
  });
  
  // Цель конверсии
  if (typeof ym !== 'undefined') {
    ym(YOUR_COUNTER_ID, 'reachGoal', 'purchase', {
      order_id: order.id,
      order_price: order.revenue
    });
  }
}

/**
 * Промокод применён
 */
function trackPromoView(promotion) {
  window.dataLayer.push({
    ecommerce: {
      promoView: {
        promotions: [{
          id: promotion.id,
          name: promotion.name,
          creative: promotion.creative,
          position: promotion.position
        }]
      }
    }
  });
}

/**
 * Клик по промо
 */
function trackPromoClick(promotion) {
  window.dataLayer.push({
    ecommerce: {
      promoClick: {
        promotions: [{
          id: promotion.id,
          name: promotion.name,
          creative: promotion.creative,
          position: promotion.position
        }]
      }
    }
  });
}

// Пример использования
// trackAddToCart({
//   id: 'SKU123',
//   name: 'iPhone 15 Pro',
//   price: 99990,
//   brand: 'Apple',
//   category: 'Смартфоны',
//   quantity: 1
// });

// trackPurchase({
//   id: 'ORDER-2024-001',
//   revenue: 99990,
//   shipping: 0,
//   products: [{
//     id: 'SKU123',
//     name: 'iPhone 15 Pro',
//     price: 99990,
//     quantity: 1
//   }]
// });
'''
    
    def _generate_dashboard(self) -> str:
        return '''#!/usr/bin/env python3
"""
Yandex Metrica Analytics Dashboard
Дашборд для анализа данных Метрики
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os


class MetricaAnalytics:
    """Аналитика Яндекс Метрики"""
    
    API_URL = "https://api-metrika.yandex.net/stat/v1/data"
    
    def __init__(self, token: str, counter_id: str):
        self.token = token
        self.counter_id = counter_id
        self.headers = {
            "Authorization": f"OAuth {token}",
            "Content-Type": "application/json"
        }
    
    def get_traffic(self, date_from: str, date_to: str) -> Dict:
        """Получить данные о трафике"""
        params = {
            "ids": self.counter_id,
            "date1": date_from,
            "date2": date_to,
            "metrics": "ym:s:visits,ym:s:users,ym:s:pageviews,ym:s:bounceRate,ym:s:pageDepth,ym:s:avgSessionDurationSeconds",
            "dimensions": "ym:s:date",
            "sort": "ym:s:date"
        }
        
        response = requests.get(self.API_URL, headers=self.headers, params=params)
        return response.json()
    
    def get_sources(self, date_from: str, date_to: str) -> Dict:
        """Источники трафика"""
        params = {
            "ids": self.counter_id,
            "date1": date_from,
            "date2": date_to,
            "metrics": "ym:s:visits,ym:s:users,ym:s:bounceRate",
            "dimensions": "ym:s:trafficSource",
            "sort": "-ym:s:visits"
        }
        
        response = requests.get(self.API_URL, headers=self.headers, params=params)
        return response.json()
    
    def get_goals(self, date_from: str, date_to: str) -> Dict:
        """Достижение целей"""
        params = {
            "ids": self.counter_id,
            "date1": date_from,
            "date2": date_to,
            "metrics": "ym:s:goal<goal_id>reaches,ym:s:goal<goal_id>conversionRate",
            "dimensions": "ym:s:goal",
            "sort": "-ym:s:goal<goal_id>reaches"
        }
        
        response = requests.get(self.API_URL, headers=self.headers, params=params)
        return response.json()
    
    def get_devices(self, date_from: str, date_to: str) -> Dict:
        """Устройства"""
        params = {
            "ids": self.counter_id,
            "date1": date_from,
            "date2": date_to,
            "metrics": "ym:s:visits,ym:s:users,ym:s:bounceRate",
            "dimensions": "ym:s:deviceCategory",
            "sort": "-ym:s:visits"
        }
        
        response = requests.get(self.API_URL, headers=self.headers, params=params)
        return response.json()
    
    def generate_report(self, days: int = 30) -> str:
        """Сгенерировать отчёт"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        date_from = start_date.strftime("%Y-%m-%d")
        date_to = end_date.strftime("%Y-%m-%d")
        
        # Получаем данные
        traffic = self.get_traffic(date_from, date_to)
        sources = self.get_sources(date_from, date_to)
        devices = self.get_devices(date_from, date_to)
        
        # Формируем отчёт
        report = f"""
# 📊 Отчёт Яндекс Метрика
## Период: {date_from} — {date_to}

### 📈 Общая статистика

| Метрика | Значение |
|---------|----------|
| Визиты | {self._extract_total(traffic, 'ym:s:visits')} |
| Посетители | {self._extract_total(traffic, 'ym:s:users')} |
| Просмотры | {self._extract_total(traffic, 'ym:s:pageviews')} |
| Отказы | {self._extract_total(traffic, 'ym:s:bounceRate')}% |
| Глубина | {self._extract_total(traffic, 'ym:s:pageDepth')} |

### 🌐 Источники трафика

{self._format_sources(sources)}

### 📱 Устройства

{self._format_devices(devices)}

---
*Отчёт сгенерирован: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
        return report
    
    def _extract_total(self, data: Dict, metric: str) -> str:
        """Извлечь общую сумму"""
        totals = data.get("totals", [])
        if totals:
            value = totals[0]
            if isinstance(value, float):
                return f"{value:.2f}"
            return str(value)
        return "N/A"
    
    def _format_sources(self, data: Dict) -> str:
        """Форматировать источники"""
        lines = ["| Источник | Визиты | Пользователи | Отказы |", "|----------|--------|--------------|--------|"]
        
        for item in data.get("data", [])[:5]:
            source = item["dimensions"][0]["name"]
            visits = item["metrics"][0]
            users = item["metrics"][1]
            bounce = item["metrics"][2]
            lines.append(f"| {source} | {visits} | {users} | {bounce:.1f}% |")
        
        return "\\n".join(lines)
    
    def _format_devices(self, data: Dict) -> str:
        """Форматировать устройства"""
        lines = ["| Устройство | Визиты | Пользователи | Отказы |", "|------------|--------|--------------|--------|"]
        
        for item in data.get("data", []):
            device = item["dimensions"][0]["name"]
            visits = item["metrics"][0]
            users = item["metrics"][1]
            bounce = item["metrics"][2]
            lines.append(f"| {device} | {visits} | {users} | {bounce:.1f}% |")
        
        return "\\n".join(lines)


def main():
    """Пример использования"""
    analytics = MetricaAnalytics(
        token=os.getenv("YANDEX_METRIKA_TOKEN"),
        counter_id=os.getenv("YANDEX_COUNTER_ID")
    )
    
    report = analytics.generate_report(days=7)
    print(report)


if __name__ == "__main__":
    main()
'''
    
    def _generate_setup_guide(self) -> str:
        return '''# Руководство по настройке Яндекс Метрика

## 🚀 Быстрый старт

### 1. Создание счётчика

1. Перейдите на https://metrika.yandex.ru
2. Нажмите "Добавить счётчик"
3. Введите название и адрес сайта
4. Скопируйте ID счётчика (например: 12345678)

### 2. Установка кода

Вставьте код в `<head>` вашего сайта:

```html
<!-- Yandex.Metrika counter -->
<script type="text/javascript" >
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();
   for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

   ym(YOUR_COUNTER_ID, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true,
        ecommerce:"dataLayer"
   });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/YOUR_COUNTER_ID" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
```

### 3. Настройка целей

#### Цель "Отправка формы":
1. Метрика → Настройка → Цели
2. "Добавить цель"
3. Тип: JavaScript-событие
4. Идентификатор: `form_submit`

#### Цель "Покупка":
1. Тип: Посещение страниц
2. Условие: URL содержит `thank-you` или `order-confirmation`

### 4. Включение Вебвизора

1. Настройка → Счётчик
2. Включить "Вебвизор, карта скроллинга, аналитика форм"
3. Сохранить

### 5. E-commerce (для магазинов)

```javascript
// При добавлении в корзину
ym(YOUR_COUNTER_ID, 'reachGoal', 'add_to_cart');

// При покупке
window.dataLayer.push({
  ecommerce: {
    purchase: {
      actionField: {
        id: 'ORDER-001',
        revenue: 15000
      },
      products: [{
        id: 'SKU123',
        name: 'Product Name',
        price: 15000,
        quantity: 1
      }]
    }
  }
});
```

## 📊 Ключевые отчёты

### 1. Источники, сводка
- Откуда приходят посетители
- Какой канал даёт больше конверсий

### 2. Стандартные отчёты → Конверсии
- Достижение целей по источникам
- Анализ эффективности

### 3. Вебвизор
- Записи посещений
- Анализ поведения пользователей

### 4. Карта кликов
- Где кликают посетители
- Тепловая карта

### 5. Воронка
- Путь пользователя
- Точки отказа

## 🎯 Рекомендуемые цели

| Цель | Тип | Приоритет |
|------|-----|-----------|
| Отправка формы | Событие | Высокий |
| Клик по телефону | Событие | Высокий |
| Покупка | URL | Высокий |
| Добавление в корзину | Событие | Средний |
| Прокрутка 75% | Событие | Низкий |
| Время 3 мин | Событие | Низкий |

## 🔗 Интеграция с Яндекс Директ

1. Метрика → Настройка → Реклама
2. "Подключить Яндекс Директ"
3. Выбрать кампании для связи
4. Теперь цели Метрики будут видны в Директе

## ⚙️ Фильтры

### Исключить свой трафик:
1. Настройка → Фильтры
2. Исключить мои визиты → По IP
3. Указать свой IP

### Исключить реферальный спам:
```
site.ru/ - исключить
/button/ - исключить
```

## 📱 Мобильное приложение

Скачайте приложение Яндекс Метрика для iOS/Android для отслеживания на ходу.

---

**Справка:** https://yandex.ru/support/metrica/
'''


def main():
    parser = argparse.ArgumentParser(description="📊 YandexMetrica-Agent")
    parser.add_argument("request", nargs="?", help="Задача")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = YandexMetricaAgent()
    
    if args.request:
        print(f"📊 {agent.NAME} создаёт: {args.request}")
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
        print(f"📊 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\\nAPI: {agent.API_ENDPOINT}")
        print(f"\\nШаблоны целей:")
        for name, goal in agent.GOAL_TEMPLATES.items():
            print(f"  - {name}: {goal['name']}")


if __name__ == "__main__":
    main()
