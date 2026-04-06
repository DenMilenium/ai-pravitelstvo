#!/usr/bin/env python3
"""
🛡️ SecurityScanner-Agent
Security Audit & Vulnerability Scanner

Сканирование уязвимостей, аудит безопасности.
"""

import argparse
from pathlib import Path
from typing import Dict


class SecurityScannerAgent:
    """
    🛡️ SecurityScanner-Agent
    
    Специализация: Security Assessment
    Задачи: Vulnerability scanning, Security audit
    """
    
    NAME = "🛡️ SecurityScanner-Agent"
    ROLE = "Security Scanner"
    EXPERTISE = ["Security Audit", "Vulnerability Scanning", "Penetration Testing"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "security-checklist.md": self._generate_checklist(),
            "github-security.yml": self._generate_github_security(),
            "security-headers.conf": self._generate_headers()
        }
    
    def _generate_checklist(self) -> str:
        return '''# Security Checklist

## 🔒 Authentication & Authorization
- [ ] Use strong password policies
- [ ] Implement MFA where possible
- [ ] Use JWT with expiration
- [ ] Rate limit authentication attempts
- [ ] Secure password reset flow

## 🌐 Web Security
- [ ] HTTPS everywhere
- [ ] Security headers (HSTS, CSP, X-Frame-Options)
- [ ] Input validation & sanitization
- [ ] Output encoding
- [ ] CSRF protection
- [ ] SQL injection prevention (use ORM/prepared statements)

## 📦 Dependencies
- [ ] Regular dependency updates
- [ ] Vulnerability scanning (Snyk, Dependabot)
- [ ] License compliance check
- [ ] Remove unused dependencies

## 🗄️ Data Protection
- [ ] Encrypt sensitive data at rest
- [ ] Encrypt data in transit (TLS 1.2+)
- [ ] Secure key management
- [ ] Data retention policies
- [ ] PII handling compliance

## 📝 Logging & Monitoring
- [ ] Security event logging
- [ ] Failed login attempts tracking
- [ ] Anomaly detection
- [ ] Regular log review

## 🔧 Infrastructure
- [ ] Firewall configuration
- [ ] Network segmentation
- [ ] Regular backups
- [ ] Disaster recovery plan
- [ ] Container security scanning
'''
    
    def _generate_github_security(self) -> str:
        return '''name: Security Audit

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    # Node.js security
    - name: Run npm audit
      run: npm audit --audit-level=moderate
      continue-on-error: true
    
    # Python security
    - name: Run Bandit
      uses: PyCQA/bandit@main
      with:
        args: "-r . -f json -o bandit-report.json || true"
    
    # Dependency check
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    # Secret scanning
    - name: Secret Detection
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
        head: HEAD
        extra_args: --debug --only-verified
'''
    
    def _generate_headers(self) -> str:
        return '''# Security Headers for Nginx

# HSTS (HTTP Strict Transport Security)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https:; frame-ancestors 'none'; base-uri 'self'; form-action 'self';" always;

# X-Frame-Options
add_header X-Frame-Options "SAMEORIGIN" always;

# X-Content-Type-Options
add_header X-Content-Type-Options "nosniff" always;

# X-XSS-Protection
add_header X-XSS-Protection "1; mode=block" always;

# Referrer Policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Permissions Policy
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=()" always;
'''


def main():
    parser = argparse.ArgumentParser(description="🛡️ SecurityScanner-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = SecurityScannerAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🛡️ {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
