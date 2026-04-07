"""
📊 Analytics Engine - Движок аналитики AI Правительства
Сбор, агрегация и визуализация метрик использования агентов
"""
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import threading


class AnalyticsEngine:
    """Движок аналитики для AI Правительства"""
    
    def __init__(self, db_path: str = 'analytics.db'):
        self.db_path = Path(db_path)
        self._lock = threading.Lock()
        self._init_db()
    
    def _init_db(self):
        """Инициализация БД аналитики"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript('''
                -- События использования агентов
                CREATE TABLE IF NOT EXISTS agent_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    agent_type TEXT NOT NULL,
                    agent_name TEXT,
                    event_type TEXT NOT NULL,  -- 'execution', 'success', 'error', 'download'
                    project_id TEXT,
                    task_id TEXT,
                    duration_ms INTEGER,  -- время выполнения
                    artifacts_count INTEGER,
                    error_message TEXT,
                    metadata TEXT  -- JSON с доп. данными
                );
                
                -- Ежедневная агрегация
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    total_executions INTEGER DEFAULT 0,
                    successful INTEGER DEFAULT 0,
                    failed INTEGER DEFAULT 0,
                    unique_agents INTEGER DEFAULT 0,
                    total_artifacts INTEGER DEFAULT 0,
                    avg_duration_ms INTEGER DEFAULT 0
                );
                
                -- Популярность агентов
                CREATE TABLE IF NOT EXISTS agent_popularity (
                    agent_type TEXT PRIMARY KEY,
                    total_uses INTEGER DEFAULT 0,
                    last_used DATETIME,
                    success_rate REAL DEFAULT 0.0
                );
                
                -- Проекты и их статистика
                CREATE TABLE IF NOT EXISTS project_stats (
                    project_id TEXT PRIMARY KEY,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_tasks INTEGER DEFAULT 0,
                    completed_tasks INTEGER DEFAULT 0,
                    total_downloads INTEGER DEFAULT 0,
                    last_activity DATETIME
                );
                
                CREATE INDEX IF NOT EXISTS idx_events_time ON agent_events(timestamp);
                CREATE INDEX IF NOT EXISTS idx_events_agent ON agent_events(agent_type);
                CREATE INDEX IF NOT EXISTS idx_events_type ON agent_events(event_type);
            ''')
    
    def log_event(self, 
                  agent_type: str,
                  event_type: str,
                  agent_name: str = None,
                  project_id: str = None,
                  task_id: str = None,
                  duration_ms: int = None,
                  artifacts_count: int = None,
                  error_message: str = None,
                  metadata: dict = None):
        """Логирование события"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO agent_events 
                (agent_type, agent_name, event_type, project_id, task_id, 
                 duration_ms, artifacts_count, error_message, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                agent_type, agent_name, event_type, project_id, task_id,
                duration_ms, artifacts_count, error_message,
                json.dumps(metadata) if metadata else None
            ))
            
            # Обновляем агрегации
            self._update_aggregations(conn, agent_type, event_type)
    
    def _update_aggregations(self, conn: sqlite3.Connection, agent_type: str, event_type: str):
        """Обновление агрегированных данных"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Обновляем daily_stats
        conn.execute('''
            INSERT INTO daily_stats (date, total_executions)
            VALUES (?, 1)
            ON CONFLICT(date) DO UPDATE SET
                total_executions = total_executions + 1
        ''', (today,))
        
        if event_type == 'success':
            conn.execute('''
                UPDATE daily_stats SET successful = successful + 1 WHERE date = ?
            ''', (today,))
        elif event_type == 'error':
            conn.execute('''
                UPDATE daily_stats SET failed = failed + 1 WHERE date = ?
            ''', (today,))
        
        # Обновляем agent_popularity
        conn.execute('''
            INSERT INTO agent_popularity (agent_type, total_uses, last_used)
            VALUES (?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(agent_type) DO UPDATE SET
                total_uses = total_uses + 1,
                last_used = CURRENT_TIMESTAMP
        ''', (agent_type,))
    
    def get_overview_stats(self, days: int = 30) -> Dict:
        """Общая статистика за период"""
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Всего выполнений
            total = conn.execute('''
                SELECT COUNT(*) as count FROM agent_events 
                WHERE timestamp >= date(?)
            ''', (start_date,)).fetchone()['count']
            
            # Успешных/неуспешных
            success = conn.execute('''
                SELECT COUNT(*) as count FROM agent_events 
                WHERE timestamp >= date(?) AND event_type = 'success'
            ''', (start_date,)).fetchone()['count']
            
            failed = conn.execute('''
                SELECT COUNT(*) as count FROM agent_events 
                WHERE timestamp >= date(?) AND event_type = 'error'
            ''', (start_date,)).fetchone()['count']
            
            # Уникальные агенты
            unique_agents = conn.execute('''
                SELECT COUNT(DISTINCT agent_type) as count FROM agent_events 
                WHERE timestamp >= date(?)
            ''', (start_date,)).fetchone()['count']
            
            # Среднее время выполнения
            avg_duration = conn.execute('''
                SELECT AVG(duration_ms) as avg FROM agent_events 
                WHERE timestamp >= date(?) AND duration_ms IS NOT NULL
            ''', (start_date,)).fetchone()['avg'] or 0
            
            return {
                'period_days': days,
                'total_executions': total,
                'successful': success,
                'failed': failed,
                'success_rate': (success / total * 100) if total > 0 else 0,
                'unique_agents_used': unique_agents,
                'avg_execution_time_ms': round(avg_duration, 2),
                'generated_at': datetime.now().isoformat()
            }
    
    def get_daily_chart_data(self, days: int = 30) -> List[Dict]:
        """Данные для графика по дням"""
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            rows = conn.execute('''
                SELECT 
                    date(timestamp) as day,
                    COUNT(*) as total,
                    SUM(CASE WHEN event_type = 'success' THEN 1 ELSE 0 END) as success,
                    SUM(CASE WHEN event_type = 'error' THEN 1 ELSE 0 END) as failed
                FROM agent_events
                WHERE timestamp >= date(?)
                GROUP BY date(timestamp)
                ORDER BY day
            ''', (start_date,)).fetchall()
            
            return [dict(row) for row in rows]
    
    def get_agent_ranking(self, limit: int = 20) -> List[Dict]:
        """Рейтинг популярности агентов"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            rows = conn.execute('''
                SELECT 
                    agent_type,
                    COUNT(*) as uses,
                    SUM(CASE WHEN event_type = 'success' THEN 1 ELSE 0 END) as successes,
                    AVG(duration_ms) as avg_duration
                FROM agent_events
                WHERE timestamp >= date('now', '-30 days')
                GROUP BY agent_type
                ORDER BY uses DESC
                LIMIT ?
            ''', (limit,)).fetchall()
            
            result = []
            for row in rows:
                data = dict(row)
                data['success_rate'] = (data['successes'] / data['uses'] * 100) if data['uses'] > 0 else 0
                result.append(data)
            
            return result
    
    def get_category_stats(self) -> List[Dict]:
        """Статистика по категориям агентов"""
        # Маппинг категорий
        categories = {
            'react': 'Frontend', 'vue': 'Frontend', 'angular': 'Frontend',
            'svelte': 'Frontend', 'nextjs': 'Frontend', 'nuxt': 'Frontend',
            'django': 'Backend', 'fastapi': 'Backend', 'nodejs': 'Backend',
            'go': 'Backend', 'laravel': 'Backend', 'ruby': 'Backend',
            'docker': 'Cloud', 'kubernetes': 'Cloud', 'aws': 'Cloud',
            'postgres': 'Database', 'mongodb': 'Database', 'redis': 'Database',
        }
        
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute('''
                SELECT agent_type, COUNT(*) as count
                FROM agent_events
                WHERE timestamp >= date('now', '-30 days')
                GROUP BY agent_type
            ''').fetchall()
            
            category_counts = defaultdict(int)
            for agent_type, count in rows:
                cat = categories.get(agent_type, 'Other')
                category_counts[cat] += count
            
            return [
                {'category': cat, 'count': count}
                for cat, count in sorted(category_counts.items(), key=lambda x: -x[1])
            ]
    
    def get_hourly_heatmap(self) -> List[Dict]:
        """Тепловая карта активности по часам"""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute('''
                SELECT 
                    CAST(strftime('%H', timestamp) AS INTEGER) as hour,
                    CAST(strftime('%w', timestamp) AS INTEGER) as day_of_week,
                    COUNT(*) as count
                FROM agent_events
                WHERE timestamp >= date('now', '-30 days')
                GROUP BY hour, day_of_week
            ''').fetchall()
            
            return [{'hour': r[0], 'day': r[1], 'count': r[2]} for r in rows]
    
    def get_execution_trends(self, days: int = 7) -> Dict:
        """Тренды выполнения"""
        daily_data = self.get_daily_chart_data(days)
        
        if len(daily_data) < 2:
            return {'trend': 'insufficient_data'}
        
        # Расчёт тренда
        first_half = daily_data[:len(daily_data)//2]
        second_half = daily_data[len(daily_data)//2:]
        
        first_avg = sum(d['total'] for d in first_half) / len(first_half) if first_half else 0
        second_avg = sum(d['total'] for d in second_half) / len(second_half) if second_half else 0
        
        change_pct = ((second_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0
        
        return {
            'trend': 'up' if change_pct > 5 else 'down' if change_pct < -5 else 'stable',
            'change_percent': round(change_pct, 2),
            'first_period_avg': round(first_avg, 2),
            'second_period_avg': round(second_avg, 2),
            'daily_data': daily_data
        }
    
    def generate_full_report(self) -> Dict:
        """Полный аналитический отчёт"""
        return {
            'generated_at': datetime.now().isoformat(),
            'overview': self.get_overview_stats(30),
            'daily_chart': self.get_daily_chart_data(30),
            'agent_ranking': self.get_agent_ranking(20),
            'category_stats': self.get_category_stats(),
            'hourly_heatmap': self.get_hourly_heatmap(),
            'trends': self.get_execution_trends(7)
        }


# Интеграция с Dashboard
class AnalyticsMiddleware:
    """Middleware для автоматического сбора аналитики"""
    
    def __init__(self, app=None):
        self.engine = AnalyticsEngine()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask app"""
        app.before_request(self._before_request)
        app.after_request(self._after_request)
    
    def _before_request(self):
        """Запоминаем время начала"""
        from flask import g
        g.start_time = datetime.now()
    
    def _after_request(self, response):
        """Логируем после запроса"""
        from flask import g, request
        
        if hasattr(g, 'start_time') and request.endpoint:
            duration = (datetime.now() - g.start_time).total_seconds() * 1000
            
            # Логируем API вызовы агентов
            if 'agent' in request.endpoint or 'execute' in request.endpoint:
                self.engine.log_event(
                    agent_type=request.endpoint,
                    event_type='api_call',
                    duration_ms=duration,
                    metadata={'endpoint': request.endpoint, 'method': request.method}
                )
        
        return response


if __name__ == '__main__':
    # Демо аналитики
    engine = AnalyticsEngine()
    
    # Генерируем тестовые данные
    print("📊 Демо аналитики AI Правительства")
    print("=" * 50)
    
    # Симулируем события
    for i in range(10):
        engine.log_event(
            agent_type='react',
            agent_name='React Agent',
            event_type='success' if i % 3 != 0 else 'error',
            duration_ms=1500 + i * 100,
            artifacts_count=4
        )
    
    # Выводим статистику
    stats = engine.get_overview_stats(30)
    print(f"\n📈 Общая статистика (30 дней):")
    print(f"   Всего выполнений: {stats['total_executions']}")
    print(f"   Успешных: {stats['successful']}")
    print(f"   Success rate: {stats['success_rate']:.1f}%")
    
    ranking = engine.get_agent_ranking()
    print(f"\n🏆 Топ агенты:")
    for i, agent in enumerate(ranking[:5], 1):
        print(f"   {i}. {agent['agent_type']}: {agent['uses']} uses")
