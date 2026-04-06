#!/usr/bin/env python3
"""
🌐 Nginx-Agent
Reverse Proxy & Load Balancer Specialist

Настройка веб-сервера, SSL, кэширование, балансировка.
"""

import argparse
from pathlib import Path
from typing import Dict


class NginxAgent:
    """
    🌐 Nginx-Agent
    
    Специализация: Web Server Configuration
    Задачи: Reverse proxy, SSL, Caching, Load balancing
    """
    
    NAME = "🌐 Nginx-Agent"
    ROLE = "Nginx Specialist"
    EXPERTISE = ["Nginx", "Reverse Proxy", "SSL/TLS", "Caching", "Load Balancing"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "nginx.conf": self._generate_main_config(),
            "site.conf": self._generate_site_config(),
            "ssl-params.conf": self._generate_ssl_config(),
            "proxy-params.conf": self._generate_proxy_params()
        }
    
    def _generate_main_config(self) -> str:
        return '''user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    # Include sites
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
'''
    
    def _generate_site_config(self) -> str:
        return '''# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/ssl-params.conf;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Logs
    access_log /var/log/nginx/example.access.log main;
    error_log /var/log/nginx/example.error.log;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location /media/ {
        alias /var/www/media/;
        expires 1M;
        access_log off;
    }

    # Proxy to application
    location / {
        include /etc/nginx/proxy-params.conf;
        proxy_pass http://app:8080;
        
        # Rate limiting
        limit_req zone=general burst=20 nodelay;
        limit_conn addr 10;
    }

    # Health check endpoint (no rate limit)
    location /health {
        access_log off;
        proxy_pass http://app:8080/health;
    }
}
'''
    
    def _generate_ssl_config(self) -> str:
        return '''# SSL Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# Diffie-Hellman parameter
ssl_dhparam /etc/nginx/dhparam.pem;
'''
    
    def _generate_proxy_params(self) -> str:
        return '''proxy_http_version 1.1;
proxy_cache_bypass $http_upgrade;

proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection 'upgrade';
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;

proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
proxy_busy_buffers_size 8k;
'''


def main():
    parser = argparse.ArgumentParser(description="🌐 Nginx-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = NginxAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🌐 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
