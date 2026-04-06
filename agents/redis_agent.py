#!/usr/bin/env python3
"""
🔴 Redis-Agent
Redis Cache & Queue Specialist

Кэширование, очереди, сессии, Pub/Sub.
"""

import argparse
from pathlib import Path
from typing import Dict


class RedisAgent:
    """
    🔴 Redis-Agent
    
    Специализация: Redis Operations
    Задачи: Caching, Sessions, Queues, Pub/Sub
    """
    
    NAME = "🔴 Redis-Agent"
    ROLE = "Redis Specialist"
    EXPERTISE = ["Redis", "Caching", "Session Store", "Message Queue", "Pub/Sub"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "redis-config.yml": self._generate_config(),
            "cache-client.py": self._generate_cache_client(),
            "session-store.js": self._generate_session_store(),
            "queue-worker.py": self._generate_queue_worker()
        }
    
    def _generate_config(self) -> str:
        return '''version: '3.8'
services:
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: redis-server /usr/local/etc/redis/redis.conf
    
  redis-commander:
    image: rediscommander/redis-commander:latest
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      - REDIS_HOSTS=local:redis:6379
    depends_on:
      - redis

volumes:
  redis_data:
'''
    
    def _generate_cache_client(self) -> str:
        return '''import redis
import json
from typing import Any, Optional
from functools import wraps

class RedisCache:
    """Клиент кэширования Redis"""
    
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша"""
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Сохранить в кэш"""
        return self.client.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str) -> bool:
        """Удалить из кэша"""
        return bool(self.client.delete(key))
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Инвалидировать по паттерну"""
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0


def cached(ttl=3600, key_prefix='cache'):
    """Декоратор для кэширования функций"""
    def decorator(func):
        cache = RedisCache()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Проверяем кэш
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Вызываем функцию
            result = func(*args, **kwargs)
            
            # Сохраняем в кэш
            cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


# Пример использования
@cached(ttl=300, key_prefix='users')
def get_user(user_id: int):
    # Долгий запрос к БД
    return {"id": user_id, "name": "John"}
'''
    
    def _generate_session_store(self) -> str:
        return '''const Redis = require('ioredis');

class RedisSessionStore {
  constructor(redisUrl = 'redis://localhost:6379') {
    this.redis = new Redis(redisUrl);
    this.prefix = 'session:';
  }
  
  async get(sessionId) {
    const data = await this.redis.get(this.prefix + sessionId);
    return data ? JSON.parse(data) : null;
  }
  
  async set(sessionId, data, ttl = 86400) {
    await this.redis.setex(
      this.prefix + sessionId,
      ttl,
      JSON.stringify(data)
    );
  }
  
  async destroy(sessionId) {
    await this.redis.del(this.prefix + sessionId);
  }
  
  // Express middleware
  middleware(ttl = 86400) {
    return async (req, res, next) => {
      const sessionId = req.cookies?.sessionId || this.generateId();
      
      req.session = await this.get(sessionId) || {};
      
      res.on('finish', async () => {
        await this.set(sessionId, req.session, ttl);
        res.cookie('sessionId', sessionId, { httpOnly: true, maxAge: ttl * 1000 });
      });
      
      next();
    };
  }
  
  generateId() {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  }
}

module.exports = RedisSessionStore;
'''
    
    def _generate_queue_worker(self) -> str:
        return '''import redis
import json
import time
from typing import Callable

class RedisQueue:
    """Очередь задач на Redis"""
    
    def __init__(self, name: str, host='localhost', port=6379):
        self.name = name
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
    
    def enqueue(self, task: dict) -> bool:
        """Добавить задачу в очередь"""
        return self.client.lpush(self.name, json.dumps(task))
    
    def dequeue(self, timeout: int = 0) -> dict:
        """Получить задачу из очереди (блокирующе)"""
        result = self.client.brpop(self.name, timeout=timeout)
        if result:
            return json.loads(result[1])
        return None
    
    def size(self) -> int:
        """Размер очереди"""
        return self.client.llen(self.name)


class Worker:
    """Worker для обработки очереди"""
    
    def __init__(self, queue: RedisQueue):
        self.queue = queue
        self.handlers = {}
        self.running = False
    
    def register(self, task_type: str, handler: Callable):
        """Регистрация обработчика"""
        self.handlers[task_type] = handler
    
    def start(self):
        """Запуск worker"""
        self.running = True
        print(f"Worker started for queue: {self.queue.name}")
        
        while self.running:
            task = self.queue.dequeue(timeout=5)
            
            if task:
                task_type = task.get('type')
                handler = self.handlers.get(task_type)
                
                if handler:
                    try:
                        handler(task['payload'])
                        print(f"✅ Task {task_type} completed")
                    except Exception as e:
                        print(f"❌ Task {task_type} failed: {e}")
                else:
                    print(f"⚠️ No handler for {task_type}")
    
    def stop(self):
        """Остановка worker"""
        self.running = False


# Пример
if __name__ == '__main__':
    queue = RedisQueue('emails')
    worker = Worker(queue)
    
    @worker.register('send_email')
    def handle_email(payload):
        print(f"Sending email to {payload['to']}")
        time.sleep(1)
    
    worker.start()
'''


def main():
    parser = argparse.ArgumentParser(description="🔴 Redis-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = RedisAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🔴 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
