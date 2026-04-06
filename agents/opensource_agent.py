#!/usr/bin/env python3
"""
📦 OpenSource-Agent
Open Source Integration Specialist

Ищет, анализирует и внедряет open source решения.
Проверяет лицензии на коммерческое использование.
"""

import argparse
from pathlib import Path
from typing import Dict, List


class OpenSourceAgent:
    """
    📦 OpenSource-Agent
    
    Специализация: Open Source Integration
    Задачи: Поиск, анализ лицензий, внедрение OSS
    """
    
    NAME = "📦 OpenSource-Agent"
    ROLE = "Open Source Specialist"
    EXPERTISE = ["Open Source", "License Analysis", "Integration", "GitHub", "Repositories"]
    
    # База знаний популярных OSS проектов с лицензиями
    OSS_DATABASE = {
        "authentication": {
            "keycloak": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Identity and Access Management",
                "language": "Java",
                "stars": 17500
            },
            "authelia": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Single Sign-On and 2FA",
                "language": "Go",
                "stars": 18500
            },
            "casdoor": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Identity and Access Management",
                "language": "Go",
                "stars": 7500
            }
        },
        "databases": {
            "postgresql": {
                "license": "PostgreSQL License",
                "commercial": True,
                "description": "Advanced relational database",
                "language": "C",
                "stars": 12500
            },
            "mariadb": {
                "license": "GPL-2.0",
                "commercial": True,
                "description": "MySQL fork with enhancements",
                "language": "C",
                "stars": 5200
            },
            "redis": {
                "license": "BSD-3-Clause",
                "commercial": True,
                "description": "In-memory data structure store",
                "language": "C",
                "stars": 62000
            },
            "mongodb": {
                "license": "SSPL",
                "commercial": False,
                "description": "Document-oriented NoSQL database",
                "language": "C++",
                "stars": 24200
            }
        },
        "caching": {
            "varnish": {
                "license": "BSD-2-Clause",
                "commercial": True,
                "description": "HTTP accelerator and cache",
                "language": "C",
                "stars": 3200
            },
            "squid": {
                "license": "GPL-2.0",
                "commercial": True,
                "description": "Caching proxy server",
                "language": "C++",
                "stars": 1800
            }
        },
        "search": {
            "elasticsearch": {
                "license": "SSPL",
                "commercial": False,
                "description": "Distributed search and analytics",
                "language": "Java",
                "stars": 66000
            },
            "opensearch": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Elasticsearch fork - Apache licensed",
                "language": "Java",
                "stars": 7800
            },
            "meilisearch": {
                "license": "MIT",
                "commercial": True,
                "description": "Lightning-fast search engine",
                "language": "Rust",
                "stars": 42000
            },
            "typesense": {
                "license": "GPL-3.0",
                "commercial": True,
                "description": "Fast, typo-tolerant search engine",
                "language": "C++",
                "stars": 16500
            }
        },
        "monitoring": {
            "prometheus": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Monitoring and alerting",
                "language": "Go",
                "stars": 52000
            },
            "grafana": {
                "license": "AGPL-3.0",
                "commercial": True,
                "description": "Observability platform",
                "language": "TypeScript",
                "stars": 60000
            },
            "zabbix": {
                "license": "GPL-2.0",
                "commercial": True,
                "description": "Enterprise monitoring",
                "language": "C",
                "stars": 2100
            }
        },
        "logging": {
            "elk_stack": {
                "license": "SSPL/Apache-2.0",
                "commercial": False,
                "description": "Elasticsearch, Logstash, Kibana",
                "language": "Mixed",
                "stars": 66000
            },
            "loki": {
                "license": "AGPL-3.0",
                "commercial": True,
                "description": "Log aggregation system",
                "language": "Go",
                "stars": 21500
            },
            "fluentd": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Unified logging layer",
                "language": "Ruby",
                "stars": 12400
            }
        },
        "message_queue": {
            "apache_kafka": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Distributed streaming platform",
                "language": "Java/Scala",
                "stars": 26500
            },
            "rabbitmq": {
                "license": "MPL-2.0",
                "commercial": True,
                "description": "Message broker",
                "language": "Erlang",
                "stars": 11500
            },
            "nats": {
                "license": "Apache-2.0",
                "commercial": True,
                "description": "Cloud-native messaging",
                "language": "Go",
                "stars": 14000
            }
        },
        "cms": {
            "strapi": {
                "license": "MIT",
                "commercial": True,
                "description": "Headless CMS",
                "language": "JavaScript",
                "stars": 60000
            },
            "ghost": {
                "license": "MIT",
                "commercial": True,
                "description": "Professional publishing",
                "language": "JavaScript",
                "stars": 45000
            },
            "directus": {
                "license": "GPL-3.0",
                "commercial": True,
                "description": "Data platform",
                "language": "TypeScript",
                "stars": 25000
            }
        },
        "ecommerce": {
            "magento": {
                "license": "OSL-3.0",
                "commercial": True,
                "description": "E-commerce platform",
                "language": "PHP",
                "stars": 10800
            },
            "woocommerce": {
                "license": "GPL-3.0",
                "commercial": True,
                "description": "WordPress e-commerce",
                "language": "PHP",
                "stars": 8600
            },
            "prestashop": {
                "license": "OSL-3.0",
                "commercial": True,
                "description": "E-commerce solution",
                "language": "PHP",
                "stars": 7500
            }
        },
        "analytics": {
            "matomo": {
                "license": "GPL-3.0",
                "commercial": True,
                "description": "Web analytics platform",
                "language": "PHP",
                "stars": 19000
            },
            "plausible": {
                "license": "AGPL-3.0",
                "commercial": True,
                "description": "Privacy-friendly analytics",
                "language": "Elixir",
                "stars": 18000
            },
            "umami": {
                "license": "MIT",
                "commercial": True,
                "description": "Simple, fast analytics",
                "language": "TypeScript",
                "stars": 19000
            }
        }
    }
    
    # Лицензии, разрешающие коммерческое использование
    COMMERCIAL_FRIENDLY_LICENSES = [
        "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause",
        "ISC", "PostgreSQL License", "MPL-2.0"
    ]
    
    # Лицензии с оговорками
    COPYLEFT_LICENSES = [
        "GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0"
    ]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["opensource-report.md"] = self._generate_report()
        files["integration-guide.md"] = self._generate_integration_guide()
        files["license-checker.py"] = self._generate_license_checker()
        
        return files
    
    def find_solutions(self, category: str, commercial_only: bool = True) -> List[Dict]:
        """Найти OSS решения по категории"""
        solutions = []
        
        if category in self.OSS_DATABASE:
            for name, info in self.OSS_DATABASE[category].items():
                if commercial_only and not info["commercial"]:
                    continue
                solutions.append({
                    "name": name,
                    **info
                })
        
        return sorted(solutions, key=lambda x: x["stars"], reverse=True)
    
    def check_license(self, license_name: str) -> Dict:
        """Проверить лицензию на коммерческое использование"""
        license_upper = license_name.upper()
        
        if license_name in self.COMMERCIAL_FRIENDLY_LICENSES:
            return {
                "commercial_use": True,
                "restrictions": "Minimal",
                "requires_source_disclosure": False,
                "requires_same_license": False,
                "recommendation": "✅ Safe for commercial use"
            }
        elif license_name in self.COPYLEFT_LICENSES:
            return {
                "commercial_use": True,
                "restrictions": "High - Copyleft",
                "requires_source_disclosure": True,
                "requires_same_license": True,
                "recommendation": "⚠️ Commercial use allowed but requires open-sourcing derivative work"
            }
        else:
            return {
                "commercial_use": "Unknown",
                "restrictions": "Review required",
                "requires_source_disclosure": "Unknown",
                "requires_same_license": "Unknown",
                "recommendation": "❓ Manual license review required"
            }
    
    def _generate_report(self) -> str:
        report = """# Open Source Solutions Report
## Generated by OpenSource-Agent

### ✅ Recommended for Commercial Use

| Category | Project | License | Stars | Description |
|----------|---------|---------|-------|-------------|
"""
        
        for category, projects in self.OSS_DATABASE.items():
            for name, info in projects.items():
                if info["commercial"]:
                    report += f"| {category} | {name} | {info['license']} | {info['stars']}⭐ | {info['description']} |\n"
        
        report += """
### ⚠️ Requires Attention

| Project | License | Issue |
|---------|---------|-------|
| MongoDB | SSPL | Server Side Public License - commercial restrictions |
| Elasticsearch | SSPL | Use OpenSearch as Apache-2.0 alternative |

### License Guide

- **MIT/Apache-2.0/BSD** - Commercial use allowed, minimal restrictions
- **GPL/AGPL** - Commercial use allowed, but must open-source derivative work
- **SSPL** - Commercial restrictions, avoid for proprietary products

---
*Report generated: OpenSource-Agent v1.0*
"""
        return report
    
    def _generate_integration_guide(self) -> str:
        return """# Open Source Integration Guide

## Step 1: Choose the Right Solution

### Checklist:
- [ ] License allows commercial use
- [ ] Active community (recent commits)
- [ ] Good documentation
- [ ] Security track record
- [ ] Fits your tech stack

## Step 2: License Compliance

### MIT/Apache-2.0 Projects:
```
✅ Include license file in distribution
✅ Mention in NOTICE/Credits
```

### GPL Projects:
```
⚠️ Source code must be available
⚠️ Derivative work under same license
⚠️ Changes must be documented
```

## Step 3: Security Audit

```bash
# Check for vulnerabilities
npm audit
pip-audit
snyk test

# Check dependencies
license-checker --summary
cyclonedx-npm --output-file sbom.json
```

## Step 4: Integration

### Docker Compose Example:
```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    
  meilisearch:
    image: getmeili/meilisearch:latest
    restart: unless-stopped
    volumes:
      - meili_data:/meili_data
```

## Step 5: Monitoring

- Track security advisories
- Monitor license changes
- Keep dependencies updated
"""
    
    def _generate_license_checker(self) -> str:
        return '''#!/usr/bin/env python3
"""
License Checker Script
Checks dependencies for license compliance
"""

import subprocess
import json
import sys

COMMERCIAL_FRIENDLY = [
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause",
    "ISC", "PostgreSQL", "MPL-2.0", "CC0-1.0"
]

COPYLEFT = ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]

PROHIBITED = ["SSPL", "Commons Clause", "Elastic License"]

def check_node_licenses():
    """Check Node.js dependencies"""
    result = subprocess.run(
        ["license-checker", "--json"],
        capture_output=True,
        text=True
    )
    
    licenses = json.loads(result.stdout)
    issues = []
    
    for pkg, info in licenses.items():
        license_name = info.get("licenses", "UNKNOWN")
        
        if isinstance(license_name, list):
            license_name = license_name[0]
        
        if any(p in license_name for p in PROHIBITED):
            issues.append({
                "package": pkg,
                "license": license_name,
                "severity": "ERROR",
                "reason": "Commercial use restricted"
            })
        elif any(c in license_name for c in COPYLEFT):
            issues.append({
                "package": pkg,
                "license": license_name,
                "severity": "WARNING",
                "reason": "Copyleft - source disclosure required"
            })
    
    return issues

def main():
    print("🔍 Checking licenses...")
    issues = check_node_licenses()
    
    if issues:
        print(f"\\n⚠️  Found {len(issues)} license issues:")
        for issue in issues:
            print(f"  [{issue['severity']}] {issue['package']}: {issue['license']}")
            print(f"    → {issue['reason']}")
        sys.exit(1)
    else:
        print("✅ All licenses are commercial-friendly!")
        sys.exit(0)

if __name__ == "__main__":
    main()
'''


def main():
    parser = argparse.ArgumentParser(description="📦 OpenSource-Agent — OSS Solutions")
    parser.add_argument("request", nargs="?", help="Категория решений")
    parser.add_argument("--category", "-c", help="Категория для поиска")
    parser.add_argument("--commercial-only", action="store_true", help="Только коммерчески разрешенные")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = OpenSourceAgent()
    
    if args.category:
        print(f"📦 {agent.NAME} ищет решения в категории: {args.category}")
        solutions = agent.find_solutions(args.category, args.commercial_only)
        
        print(f"\nНайдено {len(solutions)} решений:")
        print("-" * 80)
        for sol in solutions:
            license_info = agent.check_license(sol["license"])
            status = "✅" if sol["commercial"] else "❌"
            print(f"{status} {sol['name']}")
            print(f"   License: {sol['license']}")
            print(f"   Stars: {sol['stars']}⭐")
            print(f"   Language: {sol['language']}")
            print(f"   {sol['description']}")
            print(f"   Recommendation: {license_info['recommendation']}")
            print()
    elif args.request:
        print(f"📦 {agent.NAME} анализирует: {args.request}")
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
        print(f"📦 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\nДоступные категории:")
        for cat in agent.OSS_DATABASE.keys():
            print(f"  - {cat}")


if __name__ == "__main__":
    main()
