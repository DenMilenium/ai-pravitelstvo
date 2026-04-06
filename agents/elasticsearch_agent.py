#!/usr/bin/env python3
"""
🔎 Elasticsearch-Agent
Search & Analytics Specialist

Полнотекстовый поиск, аналитика, логирование.
"""

import argparse
from pathlib import Path
from typing import Dict


class ElasticsearchAgent:
    """
    🔎 Elasticsearch-Agent
    
    Специализация: Search Engine
    Задачи: Full-text search, Analytics, Log aggregation
    """
    
    NAME = "🔎 Elasticsearch-Agent"
    ROLE = "Elasticsearch Specialist"
    EXPERTISE = ["Elasticsearch", "Full-text Search", "ELK Stack", "Analytics"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "docker-compose.yml": self._generate_docker_compose(),
            "search-client.py": self._generate_search_client(),
            "index-mapping.json": self._generate_mapping(),
            "log-shipper.py": self._generate_log_shipper()
        }
    
    def _generate_docker_compose(self) -> str:
        return '''version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    restart: unless-stopped
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    restart: unless-stopped
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    restart: unless-stopped
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

volumes:
  es_data:
'''
    
    def _generate_search_client(self) -> str:
        return '''from elasticsearch import Elasticsearch
from typing import List, Dict, Optional

class SearchClient:
    """Клиент для Elasticsearch"""
    
    def __init__(self, hosts=['localhost:9200']):
        self.es = Elasticsearch(hosts)
    
    def create_index(self, index: str, mapping: Dict):
        """Создать индекс с маппингом"""
        if not self.es.indices.exists(index=index):
            self.es.indices.create(index=index, body={'mappings': mapping})
            print(f"✅ Index {index} created")
    
    def index_document(self, index: str, doc: Dict, doc_id: str = None):
        """Добавить документ"""
        return self.es.index(index=index, id=doc_id, body=doc)
    
    def search(self, index: str, query: str, fields: List[str], size: int = 10) -> List[Dict]:
        """Полнотекстовый поиск"""
        body = {
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': fields,
                    'type': 'best_fields',
                    'fuzziness': 'AUTO'
                }
            },
            'highlight': {
                'fields': {
                    '*': {}
                }
            }
        }
        
        result = self.es.search(index=index, body=body, size=size)
        return [hit['_source'] for hit in result['hits']['hits']]
    
    def autocomplete(self, index: str, field: str, prefix: str, size: int = 5) -> List[str]:
        """Автодополнение"""
        body = {
            'suggest': {
                'suggestions': {
                    'prefix': prefix,
                    'completion': {
                        'field': field,
                        'size': size
                    }
                }
            }
        }
        
        result = self.es.search(index=index, body=body)
        suggestions = result['suggest']['suggestions'][0]['options']
        return [opt['text'] for opt in suggestions]


# Пример: поиск по товарам
if __name__ == '__main__':
    client = SearchClient()
    
    # Создать индекс товаров
    mapping = {
        'properties': {
            'name': {'type': 'text', 'analyzer': 'russian'},
            'description': {'type': 'text', 'analyzer': 'russian'},
            'category': {'type': 'keyword'},
            'price': {'type': 'float'},
            'suggest': {'type': 'completion'}
        }
    }
    
    client.create_index('products', mapping)
    
    # Добавить товар
    client.index_document('products', {
        'name': 'iPhone 15 Pro',
        'description': 'Новейший смартфон Apple',
        'category': 'phones',
        'price': 99990,
        'suggest': ['iphone', 'apple', 'смартфон']
    })
    
    # Поиск
    results = client.search('products', 'смартфон', ['name', 'description'])
    print(results)
'''
    
    def _generate_mapping(self) -> str:
        return '''{
  "settings": {
    "analysis": {
      "analyzer": {
        "russian": {
          "tokenizer": "standard",
          "filter": ["lowercase", "russian_stop", "russian_stemmer"]
        }
      },
      "filter": {
        "russian_stop": {
          "type": "stop",
          "stopwords": "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "russian",
        "fields": {
          "keyword": {"type": "keyword"}
        }
      },
      "content": {
        "type": "text",
        "analyzer": "russian"
      },
      "tags": {
        "type": "keyword"
      },
      "created_at": {
        "type": "date"
      },
      "suggest": {
        "type": "completion"
      }
    }
  }
}
'''
    
    def _generate_log_shipper(self) -> str:
        return '''from elasticsearch import Elasticsearch
import json
from datetime import datetime
import logging

class LogShipper:
    """Отправка логов в Elasticsearch"""
    
    def __init__(self, hosts=['localhost:9200'], index_prefix='logs'):
        self.es = Elasticsearch(hosts)
        self.index_prefix = index_prefix
    
    def ship(self, level: str, message: str, **extra):
        """Отправить лог"""
        doc = {
            '@timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message,
            **extra
        }
        
        index = f"{self.index_prefix}-{datetime.utcnow():%Y.%m.%d}"
        self.es.index(index=index, body=doc)
    
    def info(self, message: str, **extra):
        self.ship('INFO', message, **extra)
    
    def error(self, message: str, **extra):
        self.ship('ERROR', message, **extra)


# Интеграция с logging
class ElasticsearchHandler(logging.Handler):
    def __init__(self, hosts=['localhost:9200']):
        super().__init__()
        self.shipper = LogShipper(hosts)
    
    def emit(self, record):
        self.shipper.ship(
            record.levelname,
            record.getMessage(),
            logger=record.name,
            file=record.pathname,
            line=record.lineno
        )


# Пример
if __name__ == '__main__':
    logger = LogShipper()
    logger.info('Application started', app='myapp', version='1.0.0')
    logger.error('Database connection failed', retry=3)
'''


def main():
    parser = argparse.ArgumentParser(description="🔎 Elasticsearch-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = ElasticsearchAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🔎 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
