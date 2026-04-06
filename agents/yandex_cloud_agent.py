#!/usr/bin/env python3
"""
☁️ YandexCloud-Agent
Yandex Cloud Infrastructure Specialist

Инфраструктура в облаке Яндекс.
Compute, Storage, Kubernetes, Serverless.
"""

import argparse
from pathlib import Path
from typing import Dict


class YandexCloudAgent:
    """
    ☁️ YandexCloud-Agent
    
    Специализация: Yandex Cloud Infrastructure
    Задачи: VM, K8s, Storage, Serverless, Networking
    """
    
    NAME = "☁️ YandexCloud-Agent"
    ROLE = "Yandex Cloud Specialist"
    EXPERTISE = ["Yandex Cloud", "Compute", "Kubernetes", "Object Storage", "Serverless"]
    
    API_ENDPOINT = "https://cloud-api.yandex.net"
    
    # Регионы Яндекс Облака
    REGIONS = {
        "ru-central1": {"name": "Центральный регион", "zones": ["ru-central1-a", "ru-central1-b", "ru-central1-c"]},
        "ru-northwestern": {"name": "Северо-Запад", "zones": ["ru-northwestern-a"]}
    }
    
    # Шаблоны инстансов
    INSTANCE_PRESETS = {
        "small": {"cores": 2, "memory": 2, "disk": 20, "price_hour": 1.5},
        "medium": {"cores": 4, "memory": 8, "disk": 50, "price_hour": 4.5},
        "large": {"cores": 8, "memory": 16, "disk": 100, "price_hour": 9.0},
        "xl": {"cores": 16, "memory": 32, "disk": 200, "price_hour": 18.0}
    }
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["terraform-yandex.tf"] = self._generate_terraform()
        files["yc-cli-cheatsheet.md"] = self._generate_cli_cheatsheet()
        files["serverless-function.py"] = self._generate_serverless()
        files["k8s-deployment.yml"] = self._generate_k8s_config()
        files["bucket-policy.json"] = self._generate_bucket_policy()
        
        return files
    
    def _generate_terraform(self) -> str:
        return '''# Yandex Cloud Infrastructure as Code
# Terraform конфигурация для Яндекс Облака

terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

# Провайдер
provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = "ru-central1-a"
}

# Сеть
resource "yandex_vpc_network" "main" {
  name = "main-network"
}

# Подсеть
resource "yandex_vpc_subnet" "subnet_a" {
  name           = "subnet-a"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.main.id
  v4_cidr_blocks = ["10.0.1.0/24"]
}

resource "yandex_vpc_subnet" "subnet_b" {
  name           = "subnet-b"
  zone           = "ru-central1-b"
  network_id     = yandex_vpc_network.main.id
  v4_cidr_blocks = ["10.0.2.0/24"]
}

# Группа безопасности
resource "yandex_vpc_security_group" "web" {
  name        = "web-security-group"
  network_id  = yandex_vpc_network.main.id

  # HTTP
  ingress {
    protocol       = "TCP"
    port           = 80
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    protocol       = "TCP"
    port           = 443
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH (только из офиса/VPN)
  ingress {
    protocol       = "TCP"
    port           = 22
    v4_cidr_blocks = ["YOUR_OFFICE_IP/32"]
  }

  # Исходящий трафик
  egress {
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}

# Образ Ubuntu 22.04
data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}

# Виртуальная машина (веб-сервер)
resource "yandex_compute_instance" "web" {
  name        = "web-server"
  platform_id = "standard-v3"
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 30
      type     = "network-ssd"
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.subnet_a.id
    nat                = true
    security_group_ids = [yandex_vpc_security_group.web.id]
  }

  metadata = {
    user-data = templatefile("cloud-init.yml", {
      ssh_key = file("~/.ssh/id_rsa.pub")
    })
  }
}

# Виртуальная машина (база данных)
resource "yandex_compute_instance" "db" {
  name        = "db-server"
  platform_id = "standard-v3"
  zone        = "ru-central1-b"

  resources {
    cores  = 4
    memory = 8
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 50
      type     = "network-ssd"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet_b.id
    nat       = false  # Без публичного IP
  }

  metadata = {
    user-data = templatefile("cloud-init-db.yml", {
      ssh_key = file("~/.ssh/id_rsa.pub")
    })
  }
}

# Object Storage Bucket
resource "yandex_storage_bucket" "assets" {
  bucket = "my-app-assets-${random_string.bucket_suffix.result}"
  acl    = "public-read"
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# Managed Kubernetes
resource "yandex_kubernetes_cluster" "main" {
  name        = "main-cluster"
  description = "Production Kubernetes cluster"

  network_id = yandex_vpc_network.main.id

  master {
    regional {
      region = "ru-central1"

      location {
        zone      = yandex_vpc_subnet.subnet_a.zone
        subnet_id = yandex_vpc_subnet.subnet_a.id
      }

      location {
        zone      = yandex_vpc_subnet.subnet_b.zone
        subnet_id = yandex_vpc_subnet.subnet_b.id
      }
    }

    public_ip = true

    maintenance_policy {
      auto_upgrade = true
      
      maintenance_window {
        start_time = "02:00"
        duration   = "3h"
      }
    }
  }

  service_account_id      = yandex_iam_service_account.k8s.id
  node_service_account_id = yandex_iam_service_account.k8s.id

  depends_on = [
    yandex_resourcemanager_folder_iam_binding.k8s
  ]
}

# Node Group
resource "yandex_kubernetes_node_group" "main" {
  cluster_id = yandex_kubernetes_cluster.main.id
  name       = "main-nodes"

  instance_template {
    platform_id = "standard-v3"

    resources {
      memory = 8
      cores  = 4
    }

    boot_disk {
      type = "network-ssd"
      size = 64
    }

    network_interface {
      nat        = true
      subnet_ids = [yandex_vpc_subnet.subnet_a.id]
    }

    metadata = {
      ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
    }
  }

  scale_policy {
    auto_scale {
      min     = 2
      max     = 10
      initial = 2
    }
  }

  allocation_policy {
    location {
      zone = "ru-central1-a"
    }
  }
}

# Service Account для Kubernetes
resource "yandex_iam_service_account" "k8s" {
  name        = "k8s-sa"
  description = "Service account for Kubernetes"
}

resource "yandex_resourcemanager_folder_iam_binding" "k8s" {
  folder_id = var.yc_folder_id
  role      = "editor"
  members   = ["serviceAccount:${yandex_iam_service_account.k8s.id}"]
}

# PostgreSQL (Managed)
resource "yandex_mdb_postgresql_cluster" "db" {
  name        = "main-postgres"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.main.id

  config {
    version = "15"
    resources {
      resource_preset_id = "s2.micro"
      disk_type_id       = "network-ssd"
      disk_size          = 20
    }
  }

  host {
    zone      = "ru-central1-a"
    subnet_id = yandex_vpc_subnet.subnet_a.id
  }
}

# Redis (Managed)
resource "yandex_mdb_redis_cluster" "cache" {
  name        = "main-redis"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.main.id

  config {
    version = "7.0"
    resources {
      resource_preset_id = "hm2.nano"
      disk_size          = 16
    }
  }

  host {
    zone      = "ru-central1-a"
    subnet_id = yandex_vpc_subnet.subnet_a.id
  }
}

# Выводы
output "web_server_ip" {
  value = yandex_compute_instance.web.network_interface[0].nat_ip_address
}

output "kubeconfig_command" {
  value = "yc managed-kubernetes cluster get-credentials ${yandex_kubernetes_cluster.main.name} --external"
}

output "bucket_name" {
  value = yandex_storage_bucket.assets.bucket
}
'''
    
    def _generate_cli_cheatsheet(self) -> str:
        return '''# Yandex Cloud CLI Cheatsheet

## Установка

```bash
# macOS
brew install yandex-cloud-cli

# Linux
curl https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Windows
# Скачать с https://cloud.yandex.ru/docs/cli/quickstart
```

## Инициализация

```bash
# Авторизация
yc init

# Или с токеном
yc config set token YOUR_OAUTH_TOKEN
yc config set cloud-id YOUR_CLOUD_ID
yc config set folder-id YOUR_FOLDER_ID
```

## Compute (Виртуальные машины)

```bash
# Список ВМ
yc compute instance list

# Создать ВМ
yc compute instance create \\
  --name web-server \\
  --zone ru-central1-a \\
  --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4 \\
  --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2204-lts \\
  --ssh-key ~/.ssh/id_rsa.pub

# Подключиться к ВМ
yc compute ssh --name web-server

# Остановить/запустить
yc compute instance stop web-server
yc compute instance start web-server

# Удалить
yc compute instance delete web-server
```

## Kubernetes

```bash
# Список кластеров
yc managed-kubernetes cluster list

# Получить kubeconfig
yc managed-kubernetes cluster get-credentials my-cluster --external

# Список node groups
yc managed-kubernetes node-group list

# Масштабирование
yc managed-kubernetes node-group update my-nodes --fixed-size 5
```

## Object Storage (S3)

```bash
# Список бакетов
yc storage bucket list

# Создать бакет
yc storage bucket create --name my-bucket

# Загрузить файл
yc storage bucket put --name my-bucket --key file.txt ./local-file.txt

# Скачать файл
yc storage bucket get --name my-bucket --key file.txt ./local-file.txt

# Удалить файл
yc storage bucket delete-object --name my-bucket --key file.txt
```

## Базы данных

```bash
# PostgreSQL
yc managed-postgresql cluster list
yc managed-postgresql hosts list --cluster-name my-postgres

# Создать пользователя
yc managed-postgresql user create john \\
  --cluster-name my-postgres \\
  --password SecurePass123

# Создать БД
yc managed-postgresql database create mydb --cluster-name my-postgres
```

## Serverless

```bash
# Список функций
yc serverless function list

# Создать функцию
yc serverless function create --name my-function

# Создать версию
yc serverless function version create \\
  --function-name my-function \\
  --runtime python311 \\
  --entrypoint main.handler \\
  --memory 128m \\
  --execution-timeout 3s \\
  --source-path ./function.zip

# Вызвать функцию
yc serverless function invoke my-function
```

## API Gateway

```bash
# Список API Gateway
yc serverless api-gateway list

# Создать
yc serverless api-gateway create --name my-api --spec ./api-spec.yaml
```

## Container Registry

```bash
# Список реестров
yc container registry list

# Создать реестр
yc container registry create --name my-registry

# Docker login
yc container registry configure-docker

# Push образа
docker tag my-image cr.yandex/YOUR_REGISTRY_ID/my-image:latest
docker push cr.yandex/YOUR_REGISTRY_ID/my-image:latest
```

## IAM

```bash
# Список сервисных аккаунтов
yc iam service-account list

# Создать
yc iam service-account create --name my-sa

# Назначить роль
yc resource-manager folder add-access-binding \\
  --id YOUR_FOLDER_ID \\
  --role editor \\
  --service-account-id YOUR_SA_ID

# Создать ключ доступа
yc iam access-key create --service-account-name my-sa
```

## Полезные команды

```bash
# Информация о текущей конфигурации
yc config list

# Список зон
yc compute zone list

# Список образов
yc compute image list --folder-id standard-images

# Квоты
yc resource-manager folder list-quotas --id YOUR_FOLDER_ID

# Логи аудита
yc logging read --group-name default --since 1h
```

## Автодополнение

```bash
# bash
echo 'source /Users/$(whoami)/yandex-cloud/completion.bash.inc' >> ~/.bashrc

# zsh
echo 'source /Users/$(whoami)/yandex-cloud/completion.zsh.inc' >> ~/.zshrc
```
'''
    
    def _generate_serverless(self) -> str:
        return '''"""
Yandex Cloud Serverless Function
Пример функции для Yandex Cloud Functions
"""

import json
import os
import boto3
from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Обработчик serverless функции
    
    Args:
        event: Событие, вызвавшее функцию
        context: Контекст выполнения
        
    Returns:
        HTTP ответ
    """
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    query_params = event.get('queryStringParameters', {}) or {}
    body = event.get('body', '{}')
    
    try:
        body_json = json.loads(body) if body else {}
    except:
        body_json = {}
    
    # Маршрутизация
    routes = {
        ('GET', '/'): lambda: get_info(),
        ('GET', '/health'): lambda: get_health(),
        ('POST', '/process'): lambda: process_data(body_json),
        ('GET', '/storage'): lambda: list_storage(),
        ('POST', '/upload'): lambda: upload_file(body_json),
    }
    
    handler_func = routes.get((http_method, path))
    
    if handler_func:
        try:
            result = handler_func()
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result, ensure_ascii=False)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
    
    return {
        'statusCode': 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Not found'})
    }


def get_info() -> Dict:
    """Информация о функции"""
    return {
        'service': 'Yandex Cloud Serverless Function',
        'version': '1.0.0',
        'endpoints': [
            {'method': 'GET', 'path': '/', 'description': 'Информация'},
            {'method': 'GET', 'path': '/health', 'description': 'Проверка здоровья'},
            {'method': 'POST', 'path': '/process', 'description': 'Обработка данных'},
            {'method': 'GET', 'path': '/storage', 'description': 'Список файлов'},
        ]
    }


def get_health() -> Dict:
    """Проверка здоровья"""
    return {
        'status': 'healthy',
        'timestamp': json.dumps(None)  # Will be updated
    }


def process_data(data: Dict) -> Dict:
    """Обработка данных"""
    # Пример обработки
    name = data.get('name', 'Anonymous')
    
    return {
        'processed': True,
        'message': f'Hello, {name}!',
        'input': data
    }


def get_s3_client():
    """Получить клиент S3"""
    return boto3.client(
        's3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )


def list_storage() -> Dict:
    """Список файлов в бакете"""
    bucket = os.getenv('BUCKET_NAME')
    if not bucket:
        return {'error': 'BUCKET_NAME not set'}
    
    try:
        s3 = get_s3_client()
        response = s3.list_objects_v2(Bucket=bucket, MaxKeys=10)
        
        files = [
            {
                'key': obj['Key'],
                'size': obj['Size'],
                'modified': obj['LastModified'].isoformat()
            }
            for obj in response.get('Contents', [])
        ]
        
        return {'files': files, 'bucket': bucket}
    except Exception as e:
        return {'error': str(e)}


def upload_file(data: Dict) -> Dict:
    """Загрузка файла"""
    bucket = os.getenv('BUCKET_NAME')
    if not bucket:
        return {'error': 'BUCKET_NAME not set'}
    
    key = data.get('key')
    content = data.get('content')
    
    if not key or not content:
        return {'error': 'key and content required'}
    
    try:
        s3 = get_s3_client()
        s3.put_object(Bucket=bucket, Key=key, Body=content)
        return {'uploaded': True, 'key': key}
    except Exception as e:
        return {'error': str(e)}


# Для локального тестирования
if __name__ == '__main__':
    # Тестовый вызов
    test_event = {
        'httpMethod': 'GET',
        'path': '/',
        'queryStringParameters': {},
        'body': '{}'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2, ensure_ascii=False))
'''
    
    def _generate_k8s_config(self) -> str:
        return '''# Kubernetes Deployment для Yandex Cloud
# Файл: k8s-deployment.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: production
---
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  DATABASE_URL: "postgres://user:pass@postgres:5432/myapp"
  REDIS_URL: "redis://redis:6379"
  LOG_LEVEL: "info"
---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
stringData:
  JWT_SECRET: "your-jwt-secret-here"
  API_KEY: "your-api-key-here"
---
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web
        image: cr.yandex/YOUR_REGISTRY_ID/web-app:latest
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
# Service
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  namespace: production
spec:
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
---
# Ingress (требуется установить Ingress Controller)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt"
spec:
  tls:
  - hosts:
    - app.yourdomain.ru
    secretName: app-tls
  rules:
  - host: app.yourdomain.ru
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
---
# CronJob (для фоновых задач)
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-report
  namespace: production
spec:
  schedule: "0 6 * * *"  # Каждый день в 6:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: report
            image: cr.yandex/YOUR_REGISTRY_ID/report-job:latest
            envFrom:
            - configMapRef:
                name: app-config
            command: ["python", "generate_report.py"]
          restartPolicy: OnFailure
'''
    
    def _generate_bucket_policy(self) -> str:
        return '''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForAssets",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::my-app-assets/*"]
    },
    {
      "Sid": "AllowUploadFromApp",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_FOLDER_ID:user/my-app-sa"
      },
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": ["arn:aws:s3:::my-app-assets/uploads/*"]
    },
    {
      "Sid": "DenyUnencryptedUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": ["s3:PutObject"],
      "Resource": ["arn:aws:s3:::my-app-assets/*"],
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "AES256"
        }
      }
    }
  ]
}
'''


def main():
    parser = argparse.ArgumentParser(description="☁️ YandexCloud-Agent")
    parser.add_argument("request", nargs="?", help="Задача")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = YandexCloudAgent()
    
    if args.request:
        print(f"☁️ {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"☁️ {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\\nРегионы:")
        for region_id, region_info in agent.REGIONS.items():
            print(f"  - {region_id}: {region_info['name']}")
        print(f"\\nПресеты инстансов:")
        for name, spec in agent.INSTANCE_PRESETS.items():
            print(f"  - {name}: {spec['cores']} CPU, {spec['memory']} GB RAM, ~{spec['price_hour']}₽/час")


if __name__ == "__main__":
    main()
