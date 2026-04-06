#!/usr/bin/env python3
"""
🐰 RabbitMQ-Agent
Message Queue Specialist

Очереди сообщений, микросервисы, надёжная доставка.
"""

import argparse
from pathlib import Path
from typing import Dict


class RabbitMQAgent:
    """
    🐰 RabbitMQ-Agent
    
    Специализация: Message Queue Architecture
    Задачи: Queues, Exchanges, Routing, RPC
    """
    
    NAME = "🐰 RabbitMQ-Agent"
    ROLE = "RabbitMQ Specialist"
    EXPERTISE = ["RabbitMQ", "AMQP", "Message Queue", "Pub/Sub", "RPC"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "docker-compose.yml": self._generate_docker_compose(),
            "producer.py": self._generate_producer(),
            "consumer.py": self._generate_consumer(),
            "rpc-client.py": self._generate_rpc()
        }
    
    def _generate_docker_compose(self) -> str:
        return '''version: '3.8'
services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    restart: unless-stopped
    ports:
      - "5672:5672"    # AMQP
      - "15672:15672"  # Management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
      - ./rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: secure_password
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 30s
      retries: 3

volumes:
  rabbitmq_data:
'''
    
    def _generate_producer(self) -> str:
        return '''import pika
import json
from typing import Dict

class MessageProducer:
    """Продюсер сообщений RabbitMQ"""
    
    def __init__(self, host='localhost', username='admin', password='secure_password'):
        self.credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            credentials=self.credentials,
            connection_attempts=3,
            retry_delay=5
        )
        self.connection = None
        self.channel = None
        self.connect()
    
    def connect(self):
        """Подключение к RabbitMQ"""
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
    
    def send_task(self, queue: str, task: Dict, persistent=True):
        """Отправить задачу в очередь"""
        self.channel.queue_declare(queue=queue, durable=True)
        
        properties = pika.BasicProperties(
            delivery_mode=2 if persistent else 1  # 2 = persistent
        )
        
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(task).encode(),
            properties=properties
        )
        
        print(f"✅ Sent to {queue}: {task}")
    
    def publish_event(self, exchange: str, routing_key: str, event: Dict):
        """Опубликовать событие"""
        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type='topic',
            durable=True
        )
        
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(event).encode(),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
        print(f"✅ Published to {exchange}/{routing_key}: {event}")
    
    def close(self):
        """Закрыть соединение"""
        if self.connection:
            self.connection.close()


# Пример использования
if __name__ == '__main__':
    producer = MessageProducer()
    
    # Отправка задачи
    producer.send_task('email_queue', {
        'to': 'user@example.com',
        'subject': 'Welcome',
        'body': 'Hello!'
    })
    
    # Публикация события
    producer.publish_event(
        exchange='orders',
        routing_key='order.created',
        event={'order_id': 123, 'amount': 5000}
    )
    
    producer.close()
'''
    
    def _generate_consumer(self) -> str:
        return '''import pika
import json
import time
from typing import Callable

class MessageConsumer:
    """Consumer сообщений RabbitMQ"""
    
    def __init__(self, host='localhost', username='admin', password='secure_password'):
        self.credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            credentials=self.credentials
        )
        self.connection = None
        self.channel = None
        self.handlers = {}
    
    def connect(self):
        """Подключение"""
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)  # Fair dispatch
    
    def consume_queue(self, queue: str, handler: Callable):
        """Подписаться на очередь"""
        self.channel.queue_declare(queue=queue, durable=True)
        
        def callback(ch, method, properties, body):
            try:
                task = json.loads(body)
                handler(task)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"❌ Error processing: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        self.channel.basic_consume(queue=queue, on_message_callback=callback)
        print(f"🐰 Consuming from {queue}...")
    
    def consume_topic(self, exchange: str, routing_key: str, handler: Callable):
        """Подписаться на топик"""
        self.channel.exchange_declare(exchange=exchange, exchange_type='topic')
        
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        
        self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
        
        def callback(ch, method, properties, body):
            event = json.loads(body)
            handler(event)
        
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print(f"🐰 Consuming from {exchange}/{routing_key}...")
    
    def start(self):
        """Запуск consumer"""
        self.connect()
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()


# Пример
if __name__ == '__main__':
    consumer = MessageConsumer()
    
    @lambda task: print(f"📧 Email: {task}")
    def handle_email(task):
        time.sleep(1)  # Имитация работы
        print(f"✉️ Sent to {task['to']}")
    
    consumer.consume_queue('email_queue', handle_email)
    consumer.start()
'''
    
    def _generate_rpc(self) -> str:
        return '''import pika
import json
import uuid

class RpcClient:
    """RPC клиент через RabbitMQ"""
    
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host)
        )
        self.channel = self.connection.channel()
        
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        
        self.response = None
        self.corr_id = None
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
    
    def call(self, method: str, params: dict) -> dict:
        """Вызов RPC метода"""
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        message = {'method': method, 'params': params}
        
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)
        )
        
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        
        return self.response


# Пример использования
if __name__ == '__main__':
    client = RpcClient()
    result = client.call('calculate', {'a': 10, 'b': 20})
    print(f"Result: {result}")
'''


def main():
    parser = argparse.ArgumentParser(description="🐰 RabbitMQ-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = RabbitMQAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🐰 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
