"""
🚨 Alert System - Система алертов AI Правительства
Мониторинг метрик и отправка уведомлений
"""
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import threading
import time


class AlertManager:
    """Менеджер алертов"""
    
    # Уровни алертов
    LEVELS = {
        'info': {'priority': 1, 'color': '#3b82f6', 'icon': 'ℹ️'},
        'warning': {'priority': 2, 'color': '#f59e0b', 'icon': '⚠️'},
        'critical': {'priority': 3, 'color': '#ef4444', 'icon': '🚨'}
    }
    
    def __init__(self, db_path: str = 'alerts.db'):
        self.db_path = Path(db_path)
        self._init_db()
        self._running = False
        self._monitor_thread = None
    
    def _init_db(self):
        """Инициализация БД алертов"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    level TEXT NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT,
                    metric_name TEXT,
                    threshold_value REAL,
                    current_value REAL,
                    is_resolved BOOLEAN DEFAULT 0,
                    resolved_at DATETIME
                );
                
                CREATE TABLE IF NOT EXISTS alert_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    enabled BOOLEAN DEFAULT 1,
                    metric TEXT NOT NULL,
                    operator TEXT NOT NULL,  -- '>', '<', '==', '!='
                    threshold REAL NOT NULL,
                    level TEXT DEFAULT 'warning',
                    duration_minutes INTEGER DEFAULT 0,
                    cooldown_minutes INTEGER DEFAULT 60,
                    last_triggered DATETIME,
                    notification_channels TEXT  -- JSON: ['websocket', 'email', 'telegram']
                );
                
                CREATE INDEX IF NOT EXISTS idx_alerts_time ON alerts(timestamp);
                CREATE INDEX IF NOT EXISTS idx_alerts_level ON alerts(level);
                CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(is_resolved);
            ''')
    
    def create_default_rules(self):
        """Создание правил по умолчанию"""
        default_rules = [
            {
                'name': 'Low Success Rate',
                'metric': 'success_rate',
                'operator': '<',
                'threshold': 80.0,
                'level': 'warning',
                'cooldown_minutes': 30
            },
            {
                'name': 'Critical Success Rate',
                'metric': 'success_rate',
                'operator': '<',
                'threshold': 60.0,
                'level': 'critical',
                'cooldown_minutes': 15
            },
            {
                'name': 'High Error Rate',
                'metric': 'error_rate',
                'operator': '>',
                'threshold': 20.0,
                'level': 'warning',
                'cooldown_minutes': 30
            },
            {
                'name': 'No Activity',
                'metric': 'executions_per_hour',
                'operator': '<',
                'threshold': 1.0,
                'level': 'info',
                'cooldown_minutes': 120
            },
            {
                'name': 'Slow Execution',
                'metric': 'avg_duration_ms',
                'operator': '>',
                'threshold': 5000.0,
                'level': 'warning',
                'cooldown_minutes': 20
            }
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            for rule in default_rules:
                conn.execute('''
                    INSERT OR IGNORE INTO alert_rules 
                    (name, metric, operator, threshold, level, cooldown_minutes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    rule['name'], rule['metric'], rule['operator'],
                    rule['threshold'], rule['level'], rule['cooldown_minutes']
                ))
    
    def check_metric(self, metric_name: str, value: float) -> Optional[Dict]:
        """Проверка метрики против правил"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            rules = conn.execute('''
                SELECT * FROM alert_rules 
                WHERE enabled = 1 AND metric = ?
            ''', (metric_name,)).fetchall()
            
            for rule in rules:
                # Проверяем cooldown
                if rule['last_triggered']:
                    last = datetime.fromisoformat(rule['last_triggered'])
                    cooldown = timedelta(minutes=rule['cooldown_minutes'])
                    if datetime.now() - last < cooldown:
                        continue
                
                # Проверяем условие
                triggered = False
                op = rule['operator']
                threshold = rule['threshold']
                
                if op == '>' and value > threshold:
                    triggered = True
                elif op == '<' and value < threshold:
                    triggered = True
                elif op == '>=' and value >= threshold:
                    triggered = True
                elif op == '<=' and value <= threshold:
                    triggered = True
                elif op == '==' and value == threshold:
                    triggered = True
                
                if triggered:
                    # Обновляем last_triggered
                    conn.execute('''
                        UPDATE alert_rules SET last_triggered = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (rule['id'],))
                    
                    return {
                        'rule_id': rule['id'],
                        'rule_name': rule['name'],
                        'level': rule['level'],
                        'metric': metric_name,
                        'threshold': threshold,
                        'current_value': value,
                        'operator': op
                    }
        
        return None
    
    def create_alert(self, alert_data: Dict) -> int:
        """Создание алерта"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO alerts 
                (level, category, title, message, metric_name, threshold_value, current_value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert_data['level'],
                alert_data.get('category', 'system'),
                alert_data['title'],
                alert_data.get('message', ''),
                alert_data.get('metric_name'),
                alert_data.get('threshold_value'),
                alert_data.get('current_value')
            ))
            
            return cursor.lastrowid
    
    def get_active_alerts(self, level: str = None) -> List[Dict]:
        """Получение активных алертов"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            query = '''
                SELECT * FROM alerts 
                WHERE is_resolved = 0
            '''
            params = []
            
            if level:
                query += ' AND level = ?'
                params.append(level)
            
            query += ' ORDER BY timestamp DESC'
            
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
    
    def resolve_alert(self, alert_id: int):
        """Отметить алерт как решённый"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE alerts 
                SET is_resolved = 1, resolved_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (alert_id,))
    
    def get_alert_stats(self, hours: int = 24) -> Dict:
        """Статистика алертов"""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute('''
                SELECT COUNT(*) FROM alerts WHERE timestamp > ?
            ''', (since,)).fetchone()[0]
            
            by_level = conn.execute('''
                SELECT level, COUNT(*) as count 
                FROM alerts 
                WHERE timestamp > ?
                GROUP BY level
            ''', (since,)).fetchall()
            
            active = conn.execute('''
                SELECT COUNT(*) FROM alerts WHERE is_resolved = 0
            ''').fetchone()[0]
            
            return {
                'total_24h': total,
                'by_level': {row[0]: row[1] for row in by_level},
                'active': active,
                'resolved_24h': total - active
            }


class AnalyticsMonitor:
    """Мониторинг аналитики с алертами"""
    
    def __init__(self):
        self.alert_manager = AlertManager()
        self.alert_manager.create_default_rules()
        self._running = False
        self._thread = None
    
    def check_analytics(self):
        """Проверка аналитических метрик"""
        from orchestrator.utils.analytics import AnalyticsEngine
        
        engine = AnalyticsEngine()
        
        # Получаем текущую статистику
        stats = engine.get_overview_stats(1)  # за последний день
        
        alerts_triggered = []
        
        # Проверяем success rate
        success_rate = stats.get('success_rate', 100)
        alert = self.alert_manager.check_metric('success_rate', success_rate)
        if alert:
            alert_data = {
                'level': alert['level'],
                'category': 'performance',
                'title': f"⚠️ {alert['rule_name']}",
                'message': f"Success rate упал до {success_rate:.1f}% (порог: {alert['threshold']}%)",
                'metric_name': 'success_rate',
                'threshold_value': alert['threshold'],
                'current_value': success_rate
            }
            alert_id = self.alert_manager.create_alert(alert_data)
            alerts_triggered.append({**alert_data, 'id': alert_id})
        
        # Проверяем error rate
        error_rate = 100 - success_rate
        alert = self.alert_manager.check_metric('error_rate', error_rate)
        if alert:
            alert_data = {
                'level': alert['level'],
                'category': 'performance',
                'title': f"⚠️ {alert['rule_name']}",
                'message': f"Error rate вырос до {error_rate:.1f}% (порог: {alert['threshold']}%)",
                'metric_name': 'error_rate',
                'threshold_value': alert['threshold'],
                'current_value': error_rate
            }
            alert_id = self.alert_manager.create_alert(alert_data)
            alerts_triggered.append({**alert_data, 'id': alert_id})
        
        # Проверяем среднее время
        avg_duration = stats.get('avg_execution_time_ms', 0)
        alert = self.alert_manager.check_metric('avg_duration_ms', avg_duration)
        if alert:
            alert_data = {
                'level': alert['level'],
                'category': 'performance',
                'title': f"⏱️ {alert['rule_name']}",
                'message': f"Среднее время выполнения: {avg_duration:.0f}мс (порог: {alert['threshold']:.0f}мс)",
                'metric_name': 'avg_duration_ms',
                'threshold_value': alert['threshold'],
                'current_value': avg_duration
            }
            alert_id = self.alert_manager.create_alert(alert_data)
            alerts_triggered.append({**alert_data, 'id': alert_id})
        
        return alerts_triggered
    
    def start_monitoring(self, interval_seconds: int = 60):
        """Запуск фонового мониторинга"""
        self._running = True
        
        def monitor_loop():
            while self._running:
                try:
                    alerts = self.check_analytics()
                    
                    if alerts:
                        print(f"🚨 Triggered {len(alerts)} alerts")
                        
                        # Отправляем через WebSocket
                        try:
                            from dashboard.websocket import broadcast_alert
                            for alert in alerts:
                                broadcast_alert(alert)
                        except Exception as e:
                            print(f"WebSocket broadcast failed: {e}")
                    
                    time.sleep(interval_seconds)
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(interval_seconds)
        
        self._thread = threading.Thread(target=monitor_loop, daemon=True)
        self._thread.start()
        print(f"🚨 Alert monitoring started (interval: {interval_seconds}s)")
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        print("🚨 Alert monitoring stopped")


if __name__ == '__main__':
    # Тест
    monitor = AnalyticsMonitor()
    
    print("🚨 Alert System Test")
    print("=" * 50)
    
    # Создаём тестовый алерт
    alert_manager = AlertManager()
    alert_id = alert_manager.create_alert({
        'level': 'warning',
        'category': 'test',
        'title': 'Test Alert',
        'message': 'This is a test alert',
        'metric_name': 'success_rate',
        'threshold_value': 80,
        'current_value': 75
    })
    
    print(f"✅ Created alert #{alert_id}")
    
    # Получаем активные алерты
    active = alert_manager.get_active_alerts()
    print(f"📊 Active alerts: {len(active)}")
    
    # Получаем статистику
    stats = alert_manager.get_alert_stats()
    print(f"📈 Alert stats: {stats}")
    
    # Проверяем метрики
    print("\n🔍 Checking metrics...")
    alerts = monitor.check_analytics()
    print(f"🚨 Triggered alerts: {len(alerts)}")
