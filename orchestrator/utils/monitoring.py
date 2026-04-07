"""
📊 System Monitor - Мониторинг системы и проектов
Отслеживает: CPU, RAM, диск, задачи, агентов
"""
import psutil
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import threading


class SystemMonitor:
    """Мониторинг системных ресурсов"""
    
    def __init__(self, db_path: str = 'monitoring.db'):
        self.db_path = Path(db_path)
        self.metrics_history: List[Dict] = []
        self.max_history = 1000
        self._lock = threading.Lock()
        self._running = False
        self._thread = None
    
    def get_system_stats(self) -> Dict:
        """Получение текущей статистики системы"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # RAM
        memory = psutil.virtual_memory()
        
        # Диск
        disk = psutil.disk_usage('/')
        
        # Сеть
        net_io = psutil.net_io_counters()
        
        # Процессы
        processes = len(list(psutil.process_iter()))
        
        # Uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'frequency': cpu_freq.current if cpu_freq else None,
                'per_cpu': psutil.cpu_percent(interval=0.1, percpu=True)
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used,
                'free': memory.free
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': (disk.used / disk.total) * 100
            },
            'network': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            },
            'processes': processes,
            'uptime': {
                'days': uptime.days,
                'hours': uptime.seconds // 3600,
                'minutes': (uptime.seconds % 3600) // 60
            }
        }
    
    def get_process_stats(self, name_filter: str = None) -> List[Dict]:
        """Получение статистики по процессам"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                if name_filter and name_filter.lower() not in info['name'].lower():
                    continue
                
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'cpu_percent': info['cpu_percent'],
                    'memory_percent': info['memory_percent'],
                    'status': info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Сортируем по CPU
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:20]
    
    def get_dashboard_processes(self) -> List[Dict]:
        """Получение процессов Dashboard и агентов"""
        dashboard_procs = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                info = proc.info
                cmdline = ' '.join(info['cmdline'] or [])
                
                if any(x in cmdline for x in ['ai-pravitelstvo', 'dashboard', 'app.py', 'python']):
                    dashboard_procs.append({
                        'pid': info['pid'],
                        'name': info['name'],
                        'cpu_percent': info['cpu_percent'],
                        'memory_mb': info['memory_info'].rss / 1024 / 1024 if info['memory_info'] else 0,
                        'type': 'dashboard' if 'app.py' in cmdline else 'agent'
                    })
            except:
                pass
        
        return dashboard_procs
    
    def record_metric(self, metric: Dict):
        """Запись метрики в историю"""
        with self._lock:
            self.metrics_history.append(metric)
            
            # Ограничиваем размер истории
            if len(self.metrics_history) > self.max_history:
                self.metrics_history = self.metrics_history[-self.max_history:]
    
    def get_metrics_history(self, limit: int = 100) -> List[Dict]:
        """Получение истории метрик"""
        with self._lock:
            return self.metrics_history[-limit:]
    
    def start_monitoring(self, interval: int = 60):
        """Запуск фонового мониторинга"""
        self._running = True
        
        def monitor_loop():
            while self._running:
                try:
                    stats = self.get_system_stats()
                    self.record_metric(stats)
                    time.sleep(interval)
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(interval)
        
        self._thread = threading.Thread(target=monitor_loop, daemon=True)
        self._thread.start()
        print(f"📊 Мониторинг запущен (интервал: {interval}с)")
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        print("📊 Мониторинг остановлен")
    
    def get_alerts(self) -> List[Dict]:
        """Получение активных алертов"""
        alerts = []
        stats = self.get_system_stats()
        
        # CPU alert
        if stats['cpu']['percent'] > 80:
            alerts.append({
                'level': 'warning',
                'type': 'cpu',
                'message': f"⚠️ CPU загружен на {stats['cpu']['percent']:.1f}%"
            })
        
        # Memory alert
        if stats['memory']['percent'] > 85:
            alerts.append({
                'level': 'warning', 
                'type': 'memory',
                'message': f"⚠️ RAM заполнена на {stats['memory']['percent']:.1f}%"
            })
        
        # Disk alert
        if stats['disk']['percent'] > 90:
            alerts.append({
                'level': 'critical',
                'type': 'disk',
                'message': f"🚨 Диск заполнен на {stats['disk']['percent']:.1f}%"
            })
        
        return alerts
    
    def generate_report(self) -> Dict:
        """Генерация отчёта о системе"""
        stats = self.get_system_stats()
        alerts = self.get_alerts()
        processes = self.get_dashboard_processes()
        
        # Расчёт средних значений за последний час
        recent = self.get_metrics_history(60)
        
        avg_cpu = sum(m['cpu']['percent'] for m in recent) / len(recent) if recent else 0
        avg_mem = sum(m['memory']['percent'] for m in recent) / len(recent) if recent else 0
        
        return {
            'generated_at': datetime.now().isoformat(),
            'current': stats,
            'averages': {
                'cpu_1h': avg_cpu,
                'memory_1h': avg_mem
            },
            'alerts': alerts,
            'dashboard_processes': processes,
            'status': 'healthy' if not alerts else 'warning' if all(a['level'] == 'warning' for a in alerts) else 'critical'
        }


class ProjectMonitor:
    """Мониторинг проектов"""
    
    def __init__(self, projects_dir: str = 'projects'):
        self.projects_dir = Path(projects_dir)
    
    def get_project_stats(self, project_id: str) -> Dict:
        """Статистика проекта"""
        project_path = self.projects_dir / project_id
        
        if not project_path.exists():
            return {'error': 'Проект не найден'}
        
        # Размер
        total_size = sum(f.stat().st_size for f in project_path.rglob('*') if f.is_file())
        
        # Файлы
        files = list(project_path.rglob('*'))
        file_count = len([f for f in files if f.is_file()])
        dir_count = len([f for f in files if f.is_dir()])
        
        # Последнее изменение
        last_modified = max((f.stat().st_mtime for f in files if f.is_file()), default=0)
        
        return {
            'project_id': project_id,
            'size_mb': total_size / 1024 / 1024,
            'files': file_count,
            'directories': dir_count,
            'last_modified': datetime.fromtimestamp(last_modified).isoformat() if last_modified else None,
            'path': str(project_path)
        }
    
    def get_all_projects_stats(self) -> List[Dict]:
        """Статистика всех проектов"""
        if not self.projects_dir.exists():
            return []
        
        return [self.get_project_stats(d.name) for d in self.projects_dir.iterdir() if d.is_dir()]


# API для Flask
class MonitoringAPI:
    """API endpoints для мониторинга"""
    
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.project_monitor = ProjectMonitor()
    
    def get_dashboard_data(self) -> Dict:
        """Данные для Dashboard"""
        return {
            'system': self.system_monitor.get_system_stats(),
            'alerts': self.system_monitor.get_alerts(),
            'processes': self.system_monitor.get_dashboard_processes(),
            'projects': self.project_monitor.get_all_projects_stats()[:10]
        }
    
    def get_health_check(self) -> Dict:
        """Health check endpoint"""
        stats = self.system_monitor.get_system_stats()
        alerts = self.system_monitor.get_alerts()
        
        return {
            'status': 'healthy' if not alerts else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'checks': {
                'cpu': stats['cpu']['percent'] < 90,
                'memory': stats['memory']['percent'] < 95,
                'disk': stats['disk']['percent'] < 95
            }
        }


if __name__ == '__main__':
    # Тест мониторинга
    monitor = SystemMonitor()
    
    print("📊 System Stats:")
    print(json.dumps(monitor.get_system_stats(), indent=2, ensure_ascii=False))
    
    print("\n📊 Top Processes:")
    for proc in monitor.get_process_stats()[:5]:
        print(f"  {proc['name']}: CPU {proc['cpu_percent']}%")
    
    print("\n📊 Alerts:")
    for alert in monitor.get_alerts():
        print(f"  {alert['level'].upper()}: {alert['message']}")
