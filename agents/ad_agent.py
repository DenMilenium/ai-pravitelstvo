#!/usr/bin/env python3
"""
📢 Ad-Agent
Advertising & Campaign Specialist

Создание рекламных кампаний, креативы, медиапланирование.
"""

import argparse
from pathlib import Path
from typing import Dict


class AdAgent:
    """
    📢 Ad-Agent
    
    Специализация: Digital Advertising
    Задачи: Campaigns, Creatives, Media Planning
    """
    
    NAME = "📢 Ad-Agent"
    ROLE = "Advertising Specialist"
    EXPERTISE = ["Digital Ads", "Campaigns", "Creatives", "Media Buying", "ROI"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "campaign-brief.md": self._generate_brief(),
            "ad-creatives.md": self._generate_creatives(),
            "media-plan.md": self._generate_media_plan(),
            "tracking-setup.md": self._generate_tracking()
        }
    
    def _generate_brief(self) -> str:
        return '''# Бриф на рекламную кампанию

## 🎯 Цель кампании
- **Основная цель**: Увеличение продаж / Лиды / Осведомленность
- **KPI**: CTR > 2%, CPC < $1, ROAS > 3

## 👥 Целевая аудитория
- **Демография**: Возраст 25-45, доход средний+
- **Интересы**: Технологии, бизнес, саморазвитие
- **Поведение**: Активные пользователи соцсетей

## 💼 Предложение
- **УТП**: Уникальное торговое предложение
- **Выгоды**: Экономия времени, рост прибыли
- **Призыв к действию**: "Попробуй бесплатно" / "Получить консультацию"

## 📅 Сроки и бюджет
- **Длительность**: 4 недели
- **Бюджет**: $5000
- **Площадки**: Google Ads, Facebook, Instagram

## 📊 Метрики успеха
- [ ] CTR > 2%
- [ ] Конверсия > 5%
- [ ] Стоимость лида < $10
'''
    
    def _generate_creatives(self) -> str:
        return '''# Креативы для рекламной кампании

## 🎨 Визуальные форматы

### 1. Статичные баннеры (Google Display)
```
Размеры: 300x250, 728x90, 160x600, 320x50
```

**Вариант A - Проблема/Решение:**
- Заголовок: "Устали от рутины?"
- Подзаг: "Автоматизируйте за 5 минут"
- CTA: "Попробовать →"
- Цвета: Синий (#0066FF), Белый

**Вариант B - Цифры:**
- Заголовок: "+150% к прибыли"
- Подзаг: "Уже через 30 дней"
- CTA: "Узнать как →"
- Цвета: Зелёный (#00AA44), Белый

### 2. Видео-реклама (15 сек)
```
0-3с: Проблема (захват внимания)
3-10с: Решение (демонстрация)
10-15с: CTA + Логотип
```

### 3. Карусель (Instagram/Facebook)
- Слайд 1: Hook (вопрос/проблема)
- Слайд 2-4: Преимущества
- Слайд 5: CTA + Форма

## ✍️ Тексты объявлений

**Google Ads:**
```
Заголовок 1: Автоматизация бизнеса
Заголовок 2: Экономьте 10 часов в неделю
Заголовок 3: Попробуйте бесплатно

Описание: Внедряем автоматизацию за 1 день. 
Без программистов. Гарантия результата.
```

**Facebook:**
```
🔥 Откройте секрет эффективных предпринимателей

Они не работают больше — они работают умнее.
Наша система автоматизации освобождает 
10+ часов в неделю.

✅ Настройка за 1 день
✅ Без программистов  
✅ Гарантия возврата

👉 Нажмите "Узнать больше"
'''
    
    def _generate_media_plan(self) -> str:
        return '''# Медиаплан кампании

## 📊 Распределение бюджета

| Площадка | Бюджет | Доля | Цель |
|----------|--------|------|------|
| Google Search | $2000 | 40% | Лиды |
| Google Display | $1000 | 20% | Охват |
| Facebook | $1000 | 20% | Лиды |
| Instagram | $750 | 15% | Бренд |
| Retargeting | $250 | 5% | Конверсия |

## 📅 Календарь размещения

### Неделя 1: Запуск и тестирование
- Все площадки запущены
- A/B тест креативов (3 варианта)
- Сбор данных по аудиториям

### Неделя 2: Оптимизация
- Отключение неэффективных
- Увеличение бюджета на TOP
- Запуск ретаргетинга

### Неделя 3: Масштабирование
- Увеличение бюджета на +30%
- Новые аудитории lookalike
- Запуск видео-креативов

### Неделя 4: Финиш
- Максимальная конверсия
- Сбор результатов
- Планирование следующей

## 🎯 Аудитории

1. **Лукалайк 1%** - Похожие на покупателей
2. **Интересы** - Бизнес, маркетинг, IT
3. **Поведение** - Посетители сайта (30 дн)
4. **Ретаргетинг** - Корзина, заявки
'''
    
    def _generate_tracking(self) -> str:
        return '''# Настройка отслеживания

## 🔗 UTM-метки

```
Источник:
- google (поиск)
- google_display (баннеры)
- facebook (FB)
- instagram (IG)

Кампания: launch_2024

Пример URL:
https://site.com/?utm_source=google&utm_medium=cpc&utm_campaign=launch_2024&utm_content=banner_a
```

## 📈 События конверсии

**Google Ads:**
- `submit_form` - Отправка формы
- `purchase` - Покупка
- `phone_call` - Звонок

**Facebook Pixel:**
```javascript
// Base code
!function(f,b,e,v,n,t,s)
{...}

// Events
fbq('track', 'PageView');
fbq('track', 'Lead');
fbq('track', 'Purchase', {value: 100, currency: 'USD'});
```

## 📊 Дашборд отчётности

| Метрика | Цель | Текущее | Статус |
|---------|------|---------|--------|
| impressions | 100K | - | 🟡 |
| clicks | 2000 | - | 🟡 |
| CTR | >2% | - | 🟡 |
| CPC | <$1 | - | 🟡 |
| конверсии | 100 | - | 🟡 |
| CPA | <$50 | - | 🟡 |
| ROAS | >3 | - | 🟡 |
'''


def main():
    parser = argparse.ArgumentParser(description="📢 Ad-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = AdAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"📢 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
