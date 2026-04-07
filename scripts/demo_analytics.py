#!/usr/bin/env python3
"""
🎮 Demo Analytics - Генерация тестовых данных для аналитики
"""
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.utils.analytics import AnalyticsEngine


def generate_demo_data():
    """Генерация демо-данных"""
    engine = AnalyticsEngine()
    
    print("🎮 Генерация демо-данных аналитики...")
    print("=" * 50)
    
    # Агенты и их категории
    agents = [
        ('react', 'React Agent'),
        ('vue', 'Vue Agent'),
        ('django', 'Django Agent'),
        ('fastapi', 'FastAPI Agent'),
        ('docker', 'Docker Agent'),
        ('kubernetes', 'Kubernetes Agent'),
        ('postgres', 'Postgres Agent'),
        ('aws', 'AWS Agent'),
        ('testing', 'Testing Agent'),
        ('flutter', 'Flutter Agent'),
    ]
    
    # Генерируем события за последние 30 дней
    total_events = 0
    
    for day_offset in range(30, 0, -1):
        date = datetime.now() - timedelta(days=day_offset)
        
        # Случайное количество событий в день (5-20)
        daily_events = random.randint(5, 20)
        
        for _ in range(daily_events):
            agent_type, agent_name = random.choice(agents)
            
            # 85% успешных
            is_success = random.random() < 0.85
            event_type = 'success' if is_success else 'error'
            
            # Время выполнения 1000-3000 мс
            duration = random.randint(1000, 3000)
            
            # 2-5 артефактов
            artifacts = random.randint(2, 5)
            
            engine.log_event(
                agent_type=agent_type,
                agent_name=agent_name,
                event_type=event_type,
                project_id=f"proj-{random.randint(1, 10):03d}",
                task_id=f"task-{random.randint(1000, 9999)}",
                duration_ms=duration,
                artifacts_count=artifacts,
                error_message=None if is_success else "Sample error message"
            )
            
            total_events += 1
    
    print(f"✅ Сгенерировано {total_events} событий")
    
    # Выводим статистику
    print("\n📊 Статистика:")
    stats = engine.get_overview_stats(30)
    print(f"   Всего выполнений: {stats['total_executions']}")
    print(f"   Успешных: {stats['successful']}")
    print(f"   Success rate: {stats['success_rate']:.1f}%")
    print(f"   Уникальных агентов: {stats['unique_agents_used']}")
    print(f"   Среднее время: {stats['avg_execution_time_ms']:.0f} мс")
    
    print("\n🏆 Топ-5 агентов:")
    ranking = engine.get_agent_ranking(5)
    for i, agent in enumerate(ranking, 1):
        print(f"   {i}. {agent['agent_type']}: {agent['uses']} uses ({agent['success_rate']:.1f}% success)")
    
    print("\n📈 График по дням:")
    daily = engine.get_daily_chart_data(7)
    for day in daily[-7:]:
        bar = "█" * (day['total'] // 2)
        print(f"   {day['day']}: {bar} ({day['total']})")
    
    print("\n✅ Демо-данные готовы! Откройте /analytics в Dashboard")


if __name__ == '__main__':
    generate_demo_data()
