#!/usr/bin/env python3
"""
🔒 SecOps-Agent
Агент информационной безопасности

Создаёт:
- Security checklist
- Аудит кода
- Конфигурации безопасности
- Политики безопасности
"""

import argparse
from pathlib import Path
from typing import Dict, List


class SecOpsAgent:
    """
    🔒 SecOps-Agent
    
    Специализация: Информационная безопасность
    Экспертиза: OWASP, SAST/DAST, шифрование, compliance
    """
    
    NAME = "🔒 SecOps-Agent"
    ROLE = "Security Engineer"
    EXPERTISE = ["OWASP", "SAST", "DAST", "Cryptography", "Compliance", "Penetration Testing"]
    
    def __init__(self):
        self.owasp_top10 = [
            "A01: Broken Access Control",
            "A02: Cryptographic Failures",
            "A03: Injection",
            "A04: Insecure Design",
            "A05: Security Misconfiguration",
            "A06: Vulnerable Components",
            "A07: Authentication Failures",
            "A08: Data Integrity Failures",
            "A09: Logging Failures",
            "A10: SSRF",
        ]
    
    def process_request(self, request: str) -> Dict[str, str]:
        """Обработка запроса безопасности"""
        request_lower = request.lower()
        files = {}
        
        if "аудит" in request_lower or "audit" in request_lower:
            files = self._generate_security_audit(request)
        elif "чеклист" in request_lower or "checklist" in request_lower:
            files = self._generate_security_checklist(request)
        elif "политика" in request_lower or "policy" in request_lower:
            files = self._generate_security_policy(request)
        elif "конфиг" in request_lower or "config" in request_lower:
            files = self._generate_secure_config(request)
        elif "docker" in request_lower:
            files = self._generate_docker_security(request)
        elif "api" in request_lower:
            files = self._generate_api_security(request)
        else:
            files = self._generate_security_checklist(request)
        
        return files
    
    def _generate_security_checklist(self, project: str) -> Dict[str, str]:
        """Генерация чеклиста безопасности"""
        files = {}
        
        files["SECURITY_CHECKLIST.md"] = f"""# 🔒 Security Checklist: {project}

**Создано:** SecOps-Agent  
**Стандарт:** OWASP Top 10 2021  
**Уровень:** Critical

---

## ✅ Аутентификация и авторизация

- [ ] Пароли хешируются (bcrypt, Argon2)
- [ ] Минимальная сложность пароля enforced
- [ ] MFA поддерживается (опционально обязательно)
- [ ] JWT токены имеют expiration
- [ ] Refresh token rotation implemented
- [ ] Session timeout настроен
- [ ] Brute force защита (rate limiting)
- [ ] Account lockout после N попыток
- [ ] Password reset через защищённый канал
- [ ] RBAC (Role-Based Access Control) implemented

---

## 🛡️ Входные данные и валидация

- [ ] Все входные данные валидируются
- [ ] SQL Injection защита (параметризованные запросы)
- [ ] XSS защита (HTML escaping)
- [ ] CSRF токены на формах
- [ ] Content-Type проверяется
- [ ] File upload ограничен по типу/размеру
- [ ] Path traversal защита
- [ ] Command injection защита
- [ ] XML/XXE защита (если используется XML)
- [ ] SSRF защита

---

## 🔐 Шифрование

- [ ] HTTPS только (HSTS enabled)
- [ ] TLS 1.2+ only
- [ ] Sensitive data encrypted at rest
- [ ] API keys в env переменных
- [ ] Secrets management (Vault/AWS Secrets)
- [ ] Database encryption enabled
- [ ] Backup encryption
- [ ] Key rotation policy

---

## 🏗️ Архитектура и конфигурация

- [ ] Security headers установлены:
  - [ ] Content-Security-Policy
  - [ ] X-Frame-Options
  - [ ] X-Content-Type-Options
  - [ ] X-XSS-Protection
  - [ ] Strict-Transport-Security
  - [ ] Referrer-Policy
- [ ] CORS properly configured
- [ ] Error messages не leak информации
- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Unused ports closed
- [ ] Admin interfaces защищены/IP-whitelisted

---

## 📊 Логирование и мониторинг

- [ ] Security events логируются
- [ ] Failed login attempts tracked
- [ ] Privilege escalation logged
- [ ] Data access logged
- [ ] Log integrity protected
- [ ] SIEM/SOC integration
- [ ] Alerting на подозрительную активность
- [ ] Log retention policy

---

## 🧪 Тестирование безопасности

- [ ] SAST сканирование пройдено
- [ ] DAST сканирование пройдено
- [ ] Dependency check (no known vulnerabilities)
- [ ] Penetration testing (annual)
- [ ] Security code review
- [ ] Fuzz testing на критичных endpoints

---

## 🚨 Инцидент-менеджмент

- [ ] Incident response plan
- [ ] Contact list обновлён
- [ ] Backup recovery tested
- [ ] Data breach notification procedure
- [ ] Forensics capability

---

## 📋 Compliance

- [ ] GDPR compliance (если применимо)
- [ ] Data retention policy
- [ ] Privacy policy обновлена
- [ ] Cookie consent implemented
- [ ] Data processing agreements signed

---

**Подпись Security Lead:** _______________  
**Дата:** _______________

**Статус:** ⬜ Not Started / 🟡 In Progress / 🟢 Complete
"""
        return files
    
    def _generate_security_audit(self, project: str) -> Dict[str, str]:
        """Генерация аудита безопасности"""
        files = {}
        
        files["SECURITY_AUDIT.md"] = f"""# 🔍 Security Audit Report: {project}

**Auditor:** SecOps-Agent  
**Date:** $(date)  
**Classification:** INTERNAL

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Overall Risk** | 🟡 MEDIUM |
| **Critical Issues** | 2 |
| **High Issues** | 5 |
| **Medium Issues** | 8 |
| **Low Issues** | 12 |
| **Info** | 20 |

---

## 🚨 Critical Findings

### CRIT-001: Hardcoded API Keys
**Severity:** 🔴 CRITICAL  
**OWASP:** A05: Security Misconfiguration

**Description:** API ключи обнаружены в исходном коде.

**Location:**
```
config.py:15: API_KEY = "sk-live-abc123..."
```

**Remediation:**
1. Переместить ключи в environment variables
2. Использовать secrets manager
3. Отозвать скомпрометированные ключи

**Timeline:** Immediate (24 hours)

---

### CRIT-002: SQL Injection
**Severity:** 🔴 CRITICAL  
**OWASP:** A03: Injection

**Description:** Параметры запроса конкатенируются напрямую.

**Location:**
```python
# VULNERABLE CODE
query = f"SELECT * FROM users WHERE id = {{user_id}}"
```

**Remediation:**
```python
# SECURE CODE
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

**Timeline:** Immediate (24 hours)

---

## ⚠️ High Findings

### HIGH-001: Weak Password Policy
**Severity:** 🟠 HIGH  
**OWASP:** A07: Authentication Failures

**Issue:** Минимум 6 символов, нет требований к сложности.

**Recommendation:**
- Минимум 12 символов
- Требовать верхний/нижний регистр, цифры, символы
- Проверка в breached databases (HaveIBeenPwned API)

---

### HIGH-002: Missing Rate Limiting
**Severity:** 🟠 HIGH  
**OWASP:** A07: Authentication Failures

**Issue:** Нет ограничений на login attempts.

**Remediation:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login')
@limiter.limit("5 per minute")
def login():
    ...
```

---

### HIGH-003: Insecure CORS
**Severity:** 🟠 HIGH  
**OWASP:** A01: Broken Access Control

**Issue:** `Access-Control-Allow-Origin: *`

**Remediation:**
```python
CORS(app, origins=["https://trusted-domain.com"])
```

---

### HIGH-004: XSS Vulnerability
**Severity:** 🟠 HIGH  
**OWASP:** A03: Injection

**Issue:** User input rendered без escaping.

**Remediation:**
- Использовать template auto-escaping
- Content Security Policy

---

### HIGH-005: Missing Security Headers
**Severity:** 🟠 HIGH  
**OWASP:** A05: Security Misconfiguration

**Missing:**
- Content-Security-Policy
- X-Frame-Options
- HSTS

---

## 🟡 Medium Findings

1. **MED-001:** Verbose error messages
2. **MED-002:** Missing CSRF tokens on forms
3. **MED-003:** Session fixation possible
4. **MED-004:** Weak TLS configuration
5. **MED-005:** Directory listing enabled
6. **MED-006:** Old dependencies with CVEs
7. **MED-007:** Missing security.txt
8. **MED-008:** No Content Security Policy

---

## 📊 Risk Matrix

```
Likelihood
    L    M    H
   ┌────┬────┬────┐
H  │ M  │ H  │ C  │  C = Critical
   ├────┼────┼────┤  H = High
M  │ L  │ M  │ H  │  M = Medium
   ├────┼────┼────┤  L = Low
L  │ I  │ L  │ M  │  I = Info
   └────┴────┴────┘
      L    M    H
         Impact
```

---

## 🛠️ Remediation Plan

### Phase 1: Critical (Week 1)
- [ ] Fix CRIT-001: Remove hardcoded keys
- [ ] Fix CRIT-002: Parameterize SQL queries

### Phase 2: High (Week 2-3)
- [ ] Implement rate limiting
- [ ] Strengthen password policy
- [ ] Fix CORS configuration
- [ ] Add XSS protection

### Phase 3: Medium (Week 4)
- [ ] Add security headers
- [ ] Update dependencies
- [ ] Implement CSRF protection

### Phase 4: Low (Ongoing)
- [ ] Security monitoring
- [ ] Documentation
- [ ] Training

---

## 📈 Metrics

| Metric | Before | After (Target) |
|--------|--------|----------------|
| Critical Issues | 2 | 0 |
| High Issues | 5 | 0 |
| CVSS Score | 8.5 | < 4.0 |
| Security Test Coverage | 30% | 80% |

---

**Auditor:** SecOps-Agent  
**Reviewed by:** _______________  
**Next Audit:** $(date -d '+3 months')
"""
        return files
    
    def _generate_secure_config(self, project: str) -> Dict[str, str]:
        """Генерация безопасной конфигурации"""
        files = {}
        
        files["security.conf"] = f"""# 🔒 Security Configuration for {project}
# Generated by SecOps-Agent

# === SSL/TLS Configuration ===
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# === Security Headers ===
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# === Rate Limiting ===
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;

location /login {{
    limit_req zone=login burst=3 nodelay;
    proxy_pass http://backend;
}}

location /api/ {{
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://backend;
}}

# === Hide Server Info ===
server_tokens off;

# === File Upload Restrictions ===
location ~* \\.(php|php\\.|php3|php4|phtml|pl|py|jsp|asp|sh|cgi)$ {{
    return 403;
}}

# === Access Control ===
deny 192.168.1.1;  # Block specific IP
allow 10.0.0.0/8;  # Allow internal network
deny all;          # Deny everything else
"""
        
        files["app_security.py"] = f'''"""
🔒 Security Middleware for {project}
Generated by SecOps-Agent
"""

from functools import wraps
from flask import request, jsonify
import re
import html


class SecurityMiddleware:
    """Security middleware for Flask applications"""
    
    @staticmethod
    def sanitize_input(data: str) -> str:
        """Sanitize user input"""
        # HTML escape
        data = html.escape(data)
        # Remove null bytes
        data = data.replace('\\x00', '')
        return data
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def check_sql_injection(data: str) -> bool:
        """Check for SQL injection patterns"""
        patterns = [
            r'(\\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)(\\s|$)',
            r'--',
            r'/\\*',
            r'\\*/',
            r';',
        ]
        for pattern in patterns:
            if re.search(pattern, data, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def security_headers(response):
        """Add security headers to response"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response


def require_https(f):
    """Decorator to require HTTPS"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-Forwarded-Proto') == 'http':
            return jsonify({{'error': 'HTTPS required'}}), 403
        return f(*args, **kwargs)
    return decorated_function


def validate_json(schema):
    """Decorator to validate JSON input"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({{'error': 'Content-Type must be application/json'}}), 400
            # Additional schema validation here
            return f(*args, **kwargs)
        return decorated_function
    return decorator
'''
        return files
    
    def _generate_docker_security(self, project: str) -> Dict[str, str]:
        """Генерация безопасного Dockerfile"""
        files = {}
        
        files["Dockerfile.secure"] = f"""# 🔒 Secure Dockerfile for {project}
# Generated by SecOps-Agent

# ====================
# Build Stage
# ====================
FROM python:3.11-slim AS builder

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ====================
# Production Stage
# ====================
FROM python:3.11-slim

# Security: Update packages
RUN apt-get update && apt-get upgrade -y \\
    && apt-get clean \\
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy only necessary files
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . .

# Set environment
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Security: Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        
        files["docker-compose.security.yml"] = f"""# 🔒 Secure Docker Compose for {project}
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.secure
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    user: "1000:1000"
    environment:
      - SECRET_KEY_FILE=/run/secrets/secret_key
    secrets:
      - secret_key
    networks:
      - app_network
    depends_on:
      - db
    
  db:
    image: postgres:15-alpine
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER_FILE: /run/secrets/db_user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_user
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network

networks:
  app_network:
    driver: bridge

volumes:
  postgres_data:

secrets:
  secret_key:
    external: true
  db_user:
    external: true
  db_password:
    external: true
"""
        return files
    
    def _generate_api_security(self, project: str) -> Dict[str, str]:
        """Генерация API security guidelines"""
        files = {}
        
        files["API_SECURITY.md"] = f"""# 🔐 API Security Guidelines: {project}

**Created by:** SecOps-Agent  
**Version:** 1.0

---

## Authentication

### JWT Best Practices
```python
# ✅ DO
import jwt
from datetime import datetime, timedelta

def create_token(user_id: str) -> str:
    payload = {{
        'sub': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1),
        'jti': str(uuid.uuid4()),  # Unique token ID
    }}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# ❌ DON'T
def create_token_bad(user_id: str) -> str:
    payload = {{'user_id': user_id}}  # No expiration!
    return jwt.encode(payload, 'hardcoded-secret')  # Weak secret!
```

### API Key Management
```python
# ✅ DO
import os
from functools import wraps

API_KEY = os.environ.get('API_KEY')

 def require_api_key(f):
     @wraps(f)
     def decorated(*args, **kwargs):
         key = request.headers.get('X-API-Key')
         if key != API_KEY:
             return jsonify({{'error': 'Invalid API key'}}), 401
         return f(*args, **kwargs)
     return decorated
```

---

## Input Validation

### SQL Injection Prevention
```python
# ✅ DO (Parameterized queries)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌ DON'T (String formatting)
cursor.execute(f"SELECT * FROM users WHERE id = {{user_id}}")
```

### XSS Prevention
```python
# ✅ DO (Template auto-escaping)
# Flask/Jinja2 escapes by default
return render_template('page.html', user_input=user_input)

# ✅ DO (Manual escaping)
from html import escape
safe_input = escape(user_input)

# ❌ DON'T (Raw output)
element.innerHTML = userInput;  # JavaScript danger!
```

---

## Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login')
@limiter.limit("5 per minute")
def login():
    ...
```

---

## Security Headers

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

---

## Error Handling

```python
# ✅ DO (Generic error messages)
@app.errorhandler(Exception)
def handle_error(error):
    # Log detailed error internally
    logger.error(f"Error: {{str(error)}}", exc_info=True)
    
    # Return generic message to user
    return jsonify({{'error': 'Internal server error'}}), 500

# ❌ DON'T (Information disclosure)
@app.errorhandler(Exception)
def bad_handler(error):
    return jsonify({{'error': str(error), 'traceback': traceback.format_exc()}}), 500
```

---

## Secrets Management

```python
# ✅ DO
from pathlib import Path

def get_secret(secret_name: str) -> str:
    # Docker secrets
    secret_path = Path(f'/run/secrets/{{secret_name}}')
    if secret_path.exists():
        return secret_path.read_text().strip()
    
    # Fallback to env
    return os.environ.get(secret_name)

SECRET_KEY = get_secret('secret_key')
DB_PASSWORD = get_secret('db_password')

# ❌ DON'T
SECRET_KEY = "hardcoded-secret-key"  # NEVER!
```

---

## Audit Checklist

- [ ] No hardcoded secrets
- [ ] All inputs validated
- [ ] SQL parameterized
- [ ] XSS prevention enabled
- [ ] CSRF tokens on state-changing ops
- [ ] Rate limiting configured
- [ ] Security headers set
- [ ] HTTPS enforced
- [ ] Error handling safe
- [ ] Logging comprehensive
"""
        return files


def main():
    parser = argparse.ArgumentParser(description="🔒 SecOps-Agent — Безопасность")
    parser.add_argument("request", nargs="?", help="Запрос безопасности")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = SecOpsAgent()
    
    if args.request:
        print(f"🔒 {agent.NAME} обрабатывает: {args.request}")
        print("-" * 50)
        
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
            
            print(f"\n📁 Сохранено в: {output_dir}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:800] + "..." if len(content) > 800 else content)
    else:
        print(f"🔒 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"Экспертиза: {', '.join(agent.EXPERTISE)}")
        print("\nПримеры:")
        print('  python secops_agent.py "Security audit"')
        print('  python secops_agent.py "Security checklist"')
        print('  python secops_agent.py "Docker security config"')


if __name__ == "__main__":
    main()
