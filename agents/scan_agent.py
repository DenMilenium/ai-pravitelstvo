#!/usr/bin/env python3
"""
🔍 Scan-Agent
Solution Finder & Security Scanner

Сканирует репозитории на наличие готовых решений.
Проверяет безопасность, лицензии, качество кода.
"""

import argparse
from pathlib import Path
from typing import Dict, List


class ScanAgent:
    """
    🔍 Scan-Agent
    
    Специализация: Solution Discovery & Security Scanning
    Задачи: Поиск решений, аудит безопасности, анализ кода
    """
    
    NAME = "🔍 Scan-Agent"
    ROLE = "Solution Scanner"
    EXPERTISE = ["Security Scanning", "Code Analysis", "Solution Discovery", "Vulnerability Detection"]
    
    # База известных уязвимостей и их альтернатив
    VULNERABILITIES = {
        "lodash": {
            "issues": ["Prototype pollution in versions < 4.17.21"],
            "recommendation": "Update to ^4.17.21 or use native alternatives",
            "alternatives": ["radash", "remeda", "native ES2020+"]
        },
        "moment": {
            "issues": ["Deprecated", "Large bundle size", "Mutable API"],
            "recommendation": "Migrate to date-fns or dayjs",
            "alternatives": ["date-fns", "dayjs"]
        },
        "request": {
            "issues": ["Deprecated", "Large bundle"],
            "recommendation": "Use axios, node-fetch, or undici",
            "alternatives": ["axios", "node-fetch", "undici"]
        },
        "crypto": {
            "issues": ["MD5 is insecure", "SHA1 is deprecated"],
            "recommendation": "Use SHA-256 or bcrypt for passwords",
            "alternatives": ["bcrypt", "argon2", "SHA-256"]
        }
    }
    
    # Рекомендуемые паттерны безопасности
    SECURITY_PATTERNS = {
        "nodejs": {
            "helmet": "Защита HTTP headers",
            "express-rate-limit": "Защита от brute force",
            "express-validator": "Валидация входных данных",
            "cors": "Настройка CORS",
            "csurf": "Защита от CSRF",
            "hpp": "Защита от HTTP Parameter Pollution"
        },
        "python": {
            "django-csp": "Content Security Policy",
            "django-ratelimit": "Rate limiting",
            "bandit": "Security linter",
            "safety": "Проверка зависимостей"
        }
    }
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["security-checklist.md"] = self._generate_security_checklist()
        files["scanner-config.yml"] = self._generate_scanner_config()
        files["snyk-policy.yml"] = self._generate_snyk_policy()
        
        return files
    
    def find_alternatives(self, package_name: str) -> Dict:
        """Найти альтернативы проблемному пакету"""
        if package_name in self.VULNERABILITIES:
            return self.VULNERABILITIES[package_name]
        return None
    
    def scan_repository(self, repo_url: str) -> List[Dict]:
        """Сканировать репозиторий на наличие решений"""
        findings = []
        
        # Проверка лицензии
        findings.append({
            "type": "license",
            "status": "check_required",
            "message": "Verify LICENSE file exists and allows commercial use"
        })
        
        # Проверка безопасности
        findings.append({
            "type": "security",
            "status": "check_required",
            "message": "Run npm audit / pip-audit / cargo audit"
        })
        
        # Проверка активности
        findings.append({
            "type": "maintenance",
            "status": "check_required",
            "message": "Check last commit date and issue response time"
        })
        
        return findings
    
    def _generate_security_checklist(self) -> str:
        return """# Security Checklist for Open Source Solutions

## 🔍 Pre-Integration Checklist

### 1. License Compliance
- [ ] LICENSE file exists
- [ ] License allows commercial use
- [ ] No GPL/AGPL for proprietary products
- [ ] Attribution requirements understood

### 2. Security Assessment
- [ ] No known CVEs
- [ ] Regular security updates
- [ ] Uses secure dependencies
- [ ] Input validation present
- [ ] No hardcoded secrets

### 3. Code Quality
- [ ] Test coverage > 70%
- [ ] CI/CD pipeline active
- [ ] Code review process
- [ ] Linting configured

### 4. Maintenance
- [ ] Last commit < 6 months
- [ ] Maintainers respond to issues
- [ ] Version releases regular
- [ ] Documentation current

### 5. Integration
- [ ] Compatible with tech stack
- [ ] API stability (semver)
- [ ] Migration path exists
- [ ] Performance acceptable

## 🛠️ Security Tools to Run

```bash
# JavaScript/TypeScript
npm audit
snyk test
semgrep --config=auto

# Python
bandit -r .
pip-audit
safety check

# Go
gosec ./...
nancy sleuth

# General
trivy fs .
docker scan image:tag
```

## 🚨 Red Flags

- No LICENSE file
- No activity > 1 year
- Critical CVEs not fixed
- Single maintainer
- No tests
- Hardcoded credentials
"""
    
    def _generate_scanner_config(self) -> str:
        return """# ScanAgent Configuration
# Tool configurations for security scanning

# Semgrep rules
semgrep:
  rules:
    - p/owasp-top-ten
    - p/cwe-top-25
    - p/security-audit
    - p/secrets
  exclude:
    - "*.test.js"
    - "*_test.go"
  severity:
    - ERROR
    - WARNING

# Trivy scanner
trivy:
  scan:
    - vulnerabilities
    - misconfigurations
    - secrets
  severity:
    - HIGH
    - CRITICAL
  ignore-unfixed: true

# SonarQube (if available)
sonarqube:
  coverage:
    minimum: 70
  duplication:
    maximum: 3
  issues:
    severity: MAJOR
"""
    
    def _generate_snyk_policy(self) -> str:
        return """# Snyk Security Policy
# Ignore rules for known acceptable risks

version: v1.25.0
ignore:
  # Example: Ignore low severity dev dependency issue
  SNYK-JS-LODASH-567890:
    - '* > dev-utils':
        reason: 'Dev dependency only, not used in production'
        expires: 2024-12-31T00:00:00.000Z
        created: 2024-01-01T00:00:00.000Z

patch: {}
"""
    
    def generate_report(self, findings: List[Dict]) -> str:
        """Генерация отчёта о сканировании"""
        report = """# Repository Scan Report
## Generated by Scan-Agent

## Findings Summary

| Type | Count | Status |
|------|-------|--------|
"""
        
        by_type = {}
        for finding in findings:
            t = finding["type"]
            by_type[t] = by_type.get(t, 0) + 1
        
        for t, count in by_type.items():
            report += f"| {t} | {count} | ⚠️ |\n"
        
        report += """
## Detailed Findings

"""
        
        for i, finding in enumerate(findings, 1):
            report += f"### {i}. {finding['type'].upper()}\n"
            report += f"- Status: {finding['status']}\n"
            report += f"- Message: {finding['message']}\n\n"
        
        report += """
## Recommendations

1. Fix all CRITICAL and HIGH severity issues
2. Review MEDIUM severity issues
3. Document accepted risks for LOW severity
4. Schedule regular security audits

---
*Scan completed: Scan-Agent v1.0*
"""
        return report


def main():
    parser = argparse.ArgumentParser(description="🔍 Scan-Agent — Security Scanning")
    parser.add_argument("request", nargs="?", help="Репозиторий или пакет для сканирования")
    parser.add_argument("--find-alternatives", "-a", help="Найти альтернативы пакету")
    parser.add_argument("--scan", "-s", help="URL репозитория для сканирования")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = ScanAgent()
    
    if args.find_alternatives:
        print(f"🔍 {agent.NAME} ищет альтернативы: {args.find_alternatives}")
        alt = agent.find_alternatives(args.find_alternatives)
        
        if alt:
            print(f"\n⚠️  Проблемы с {args.find_alternatives}:")
            for issue in alt["issues"]:
                print(f"   - {issue}")
            print(f"\n💡 Рекомендация: {alt['recommendation']}")
            print(f"\n🔄 Альтернативы: {', '.join(alt['alternatives'])}")
        else:
            print(f"ℹ️  Информация о {args.find_alternatives} не найдена")
    
    elif args.scan:
        print(f"🔍 {agent.NAME} сканирует: {args.scan}")
        findings = agent.scan_repository(args.scan)
        report = agent.generate_report(findings)
        print(report)
    
    elif args.request:
        print(f"🔍 {agent.NAME} создаёт: {args.request}")
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
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"🔍 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\nКоманды:")
        print(f"  --find-alternatives PACKAGE  Найти альтернативы проблемному пакету")
        print(f"  --scan REPO_URL              Сканировать репозиторий")
        print(f"\nПримеры проблемных пакетов:")
        for pkg in agent.VULNERABILITIES.keys():
            print(f"  - {pkg}")


if __name__ == "__main__":
    main()
