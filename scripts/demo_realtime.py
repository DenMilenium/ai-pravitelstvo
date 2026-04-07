#!/usr/bin/env python3
"""
🎮 Demo Real-time Analytics + Alerts
Тестирование WebSocket обновлений и алертов
"""
import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.utils.analytics import AnalyticsEngine
from orchestrator.utils.alert_system import AlertManager, AnalyticsMonitor


def demo_realtime():
    """Демонстрация real-time обновлений"""
    print("🎮 Demo Real-time Analytics + Alerts")
    print("=" * 60)
    
    engine = AnalyticsEngine()
    alert_manager = AlertManager()
    alert_manager.create_default_rules()
    
    print("\n📊 Генерация событий для тестирования алертов...")
    print("(Симулируем падение success rate)")
    
    # Генерируем много ошибок чтобы вызвать алерт
    agents = ['react', 'django', 'docker']
    
    for i in range(20):
        agent = random.choice(agents)
        # 50% ошибок - должно вызвать алерт
        is_success = random.random() < 0.5
        
        engine.log_event(
            agent_type=agent,
            agent_name=f"{agent.title()} Agent",
            event_type='success' if is_success else 'error',
            duration_ms=random.randint(1000, 3000),
            artifacts_count=random.randint(2, 5),
            error_message=None if is_success else "Demo error"
        )
        
        print(f"  {'✅' if is_success else '❌'} {agent} - {'success' if is_success else 'error'}")
        time.sleep(0.1)
    
    print("\n🔍 Проверяем метрики...")
    stats = engine.get_overview_stats(1)
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Total: {stats['total_executions']}")
    print(f"  Successful: {stats['successful']}")
    print(f"  Failed: {stats['failed']}")
    
    print("\n🚨 Проверяем алерты...")
    monitor = AnalyticsMonitor()
    alerts = monitor.check_analytics()
    
    if alerts:
        print(f"  🔔 Triggered {len(alerts)} alerts:")
        for alert in alerts:
            print(f"     [{alert['level'].upper()}] {alert['title']}")
            print(f"         {alert['message']}")
    else:
        print("  ✅ No alerts triggered")
    
    # Показываем активные алерты
    active = alert_manager.get_active_alerts()
    print(f"\n📋 Active alerts in DB: {len(active)}")
    
    # Статистика алертов
    alert_stats = alert_manager.get_alert_stats()
    print(f"\n📈 Alert stats (24h):")
    print(f"  Total: {alert_stats['total_24h']}")
    print(f"  Active: {alert_stats['active']}")
    print(f"  By level: {alert_stats['by_level']}")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")
    print("\nОткройте /analytics и выполните:")
    print("  python3 scripts/test_alert.py")


def test_websocket_alert():
    """Тест отправки алерта через WebSocket"""
    print("\n📡 Testing WebSocket alert...")
    
    try:
        from dashboard.websocket import broadcast_alert
        
        broadcast_alert({
            'level': 'warning',
            'title': '🧪 Test Alert',
            'message': 'This is a test alert from demo script',
            'metric_name': 'success_rate',
            'threshold_value': 80,
            'current_value': 75
        })
        
        print("  ✅ WebSocket alert sent!")
    except Exception as e:
        print(f"  ❌ WebSocket not available: {e}")


if __name__ == '__main__':
    demo_realtime()
    test_websocket_alert()
