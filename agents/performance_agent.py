#!/usr/bin/env python3
"""
⚡ Performance-Agent
Performance Optimization Specialist

Оптимизация скорости, профилирование, нагрузочное тестирование.
"""

import argparse
from pathlib import Path
from typing import Dict


class PerformanceAgent:
    """
    ⚡ Performance-Agent
    
    Специализация: Speed Optimization
    Задачи: Profiling, Load Testing, Optimization
    """
    
    NAME = "⚡ Performance-Agent"
    ROLE = "Performance Specialist"
    EXPERTISE = ["Performance", "Profiling", "Load Testing", "Optimization"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "load-test.js": self._generate_load_test(),
            "profiling.py": self._generate_profiling(),
            "web-vitals.js": self._generate_web_vitals()
        }
    
    def _generate_load_test(self) -> str:
        return '''import http from 'k6/http';
import { check, sleep } from 'k6';

// Настройка нагрузки
export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Steady state
    { duration: '2m', target: 200 },  // Ramp up
    { duration: '5m', target: 200 },  // Steady state
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% запросов быстрее 500ms
    http_req_failed: ['rate<0.01'],    // Менее 1% ошибок
  },
};

export default function () {
  const res = http.get('https://example.com/api/users');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
'''
    
    def _generate_profiling(self) -> str:
        return '''import cProfile
import pstats
import io
from functools import wraps
import time


def profile(func):
    """Декоратор для профилирования функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        
        result = func(*args, **kwargs)
        
        pr.disable()
        
        # Вывод статистики
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(20)
        print(s.getvalue())
        
        return result
    
    return wrapper


def benchmark(iterations=100):
    """Декоратор для бенчмарка"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = []
            
            for _ in range(iterations):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                times.append(end - start)
            
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"Benchmark: {func.__name__}")
            print(f"  Iterations: {iterations}")
            print(f"  Avg: {avg_time*1000:.2f}ms")
            print(f"  Min: {min_time*1000:.2f}ms")
            print(f"  Max: {max_time*1000:.2f}ms")
            
            return result
        
        return wrapper
    return decorator


# Пример
@profile
@benchmark(iterations=10)
def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total


if __name__ == '__main__':
    slow_function()
'''
    
    def _generate_web_vitals(self) -> str:
        return '''import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// Отправка метрик
function sendToAnalytics(metric) {
  const body = JSON.stringify(metric);
  
  // Отправка на сервер или Google Analytics
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/analytics/vitals', body);
  } else {
    fetch('/analytics/vitals', {
      body,
      method: 'POST',
      keepalive: true,
    });
  }
}

// Регистрация метрик
getCLS(sendToAnalytics);  // Cumulative Layout Shift
getFID(sendToAnalytics);  // First Input Delay
getFCP(sendToAnalytics);  // First Contentful Paint
getLCP(sendToAnalytics);  // Largest Contentful Paint
getTTFB(sendToAnalytics); // Time to First Byte

// Целевые значения:
// LCP: < 2.5s (Good), < 4s (Needs Improvement)
// FID: < 100ms (Good), < 300ms (Needs Improvement)
// CLS: < 0.1 (Good), < 0.25 (Needs Improvement)
'''


def main():
    parser = argparse.ArgumentParser(description="⚡ Performance-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = PerformanceAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"⚡ {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
