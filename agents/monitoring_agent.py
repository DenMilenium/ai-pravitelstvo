#!/usr/bin/env python3
"""
📈 Monitoring-Agent
Prometheus & Grafana Specialist

Мониторинг, алерты, дашборды.
"""

import argparse
from pathlib import Path
from typing import Dict


class MonitoringAgent:
    """
    📈 Monitoring-Agent
    
    Специализация: Infrastructure Monitoring
    Задачи: Metrics, Alerts, Dashboards
    """
    
    NAME = "📈 Monitoring-Agent"
    ROLE = "Monitoring Specialist"
    EXPERTISE = ["Prometheus", "Grafana", "Alerting", "Metrics", "Observability"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "docker-compose.yml": self._generate_docker_compose(),
            "prometheus.yml": self._generate_prometheus_config(),
            "alerts.yml": self._generate_alerts(),
            "custom-metrics.py": self._generate_custom_metrics()
        }
    
    def _generate_docker_compose(self) -> str:
        return '''version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  node-exporter:
    image: prom/node-exporter:latest
    restart: unless-stopped
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'

  alertmanager:
    image: prom/alertmanager:latest
    restart: unless-stopped
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml

volumes:
  prometheus_data:
  grafana_data:
'''
    
    def _generate_prometheus_config(self) -> str:
        return '''global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
    metrics_path: /metrics
'''
    
    def _generate_alerts(self) -> str:
        return '''groups:
  - name: system
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% for 5 minutes"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 85% for 5 minutes"

      - alert: DiskFull
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 10
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Disk almost full on {{ $labels.instance }}"
          description: "Less than 10% disk space remaining"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Service has been down for more than 1 minute"
'''
    
    def _generate_custom_metrics(self) -> str:
        return '''from prometheus_client import Counter, Histogram, Gauge, start_http_server
import random
import time

# Метрики
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')
ACTIVE_CONNECTIONS = Gauge('app_active_connections', 'Active connections')
QUEUE_SIZE = Gauge('app_queue_size', 'Queue size')

class MetricsMiddleware:
    """Middleware для сбора метрик"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        
        REQUEST_COUNT.labels(method=method, endpoint=path).inc()
        ACTIVE_CONNECTIONS.inc()
        
        with REQUEST_DURATION.time():
            response = self.app(environ, start_response)
        
        ACTIVE_CONNECTIONS.dec()
        return response


# Запустить сервер метрик
if __name__ == '__main__':
    start_http_server(8000)
    print("Metrics server on :8000/metrics")
    
    while True:
        # Имитация работы
        QUEUE_SIZE.set(random.randint(0, 100))
        time.sleep(5)
'''


def main():
    parser = argparse.ArgumentParser(description="📈 Monitoring-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = MonitoringAgent()
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
