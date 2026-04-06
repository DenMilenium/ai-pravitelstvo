#!/usr/bin/env python3
"""
📚 Library-Agent
Library Selector & Integration Specialist

Подбирает и внедряет лучшие библиотеки для проектов.
Проверяет безопасность, лицензии, активность.
"""

import argparse
from pathlib import Path
from typing import Dict, List


class LibraryAgent:
    """
    📚 Library-Agent
    
    Специализация: Library Selection
    Задачи: Подбор библиотек, проверка безопасности, внедрение
    """
    
    NAME = "📚 Library-Agent"
    ROLE = "Library Specialist"
    EXPERTISE = ["Package Management", "Library Selection", "Security Audit", "Best Practices"]
    
    # База данных рекомендуемых библиотек
    LIBRARIES = {
        "javascript": {
            "http_client": {
                "axios": {
                    "version": "^1.6.0",
                    "description": "Promise-based HTTP client",
                    "weekly_downloads": "35M+",
                    "license": "MIT",
                    "alternative_to": ["fetch", "request"]
                }
            },
            "validation": {
                "zod": {
                    "version": "^3.22.0",
                    "description": "TypeScript-first schema validation",
                    "weekly_downloads": "3M+",
                    "license": "MIT",
                    "alternative_to": ["yup", "joi", "class-validator"]
                },
                "joi": {
                    "version": "^17.11.0",
                    "description": "Powerful data validation",
                    "weekly_downloads": "8M+",
                    "license": "BSD-3-Clause",
                    "alternative_to": ["yup", "zod"]
                }
            },
            "dates": {
                "date-fns": {
                    "version": "^3.0.0",
                    "description": "Modern date utility library",
                    "weekly_downloads": "12M+",
                    "license": "MIT",
                    "alternative_to": ["moment", "dayjs"]
                },
                "dayjs": {
                    "version": "^1.11.0",
                    "description": "2KB immutable date library",
                    "weekly_downloads": "7M+",
                    "license": "MIT",
                    "alternative_to": ["moment", "date-fns"]
                }
            },
            "testing": {
                "vitest": {
                    "version": "^1.0.0",
                    "description": "Next generation testing framework",
                    "weekly_downloads": "1.5M+",
                    "license": "MIT",
                    "alternative_to": ["jest", "mocha"]
                },
                "playwright": {
                    "version": "^1.40.0",
                    "description": "E2E testing framework",
                    "weekly_downloads": "3M+",
                    "license": "Apache-2.0",
                    "alternative_to": ["cypress", "selenium"]
                }
            },
            "ui_components": {
                "shadcn/ui": {
                    "version": "latest",
                    "description": "Re-usable components built with Radix UI",
                    "weekly_downloads": "N/A",
                    "license": "MIT",
                    "alternative_to": ["Material-UI", "Ant Design"]
                },
                "radix-ui": {
                    "version": "^1.0.0",
                    "description": "Unstyled, accessible components",
                    "weekly_downloads": "2M+",
                    "license": "MIT",
                    "alternative_to": ["Headless UI", "Reach UI"]
                }
            },
            "state_management": {
                "zustand": {
                    "version": "^4.4.0",
                    "description": "Small, fast state management",
                    "weekly_downloads": "2M+",
                    "license": "MIT",
                    "alternative_to": ["redux", "mobx"]
                },
                "jotai": {
                    "version": "^2.5.0",
                    "description": "Primitive and flexible state management",
                    "weekly_downloads": "500K+",
                    "license": "MIT",
                    "alternative_to": ["recoil", "zustand"]
                }
            },
            "forms": {
                "react-hook-form": {
                    "version": "^7.48.0",
                    "description": "Performant forms with easy validation",
                    "weekly_downloads": "6M+",
                    "license": "MIT",
                    "alternative_to": ["formik", "final-form"]
                }
            },
            "animation": {
                "framer-motion": {
                    "version": "^10.16.0",
                    "description": "Production-ready motion library",
                    "weekly_downloads": "5M+",
                    "license": "MIT",
                    "alternative_to": ["react-spring", "gsap"]
                }
            },
            "charts": {
                "recharts": {
                    "version": "^2.10.0",
                    "description": "Composable charting library",
                    "weekly_downloads": "1.5M+",
                    "license": "MIT",
                    "alternative_to": ["chart.js", "d3"]
                },
                "chart.js": {
                    "version": "^4.4.0",
                    "description": "Simple yet flexible charts",
                    "weekly_downloads": "4M+",
                    "license": "MIT",
                    "alternative_to": ["recharts", "d3"]
                }
            }
        },
        "python": {
            "http": {
                "httpx": {
                    "version": "^0.25.0",
                    "description": "Next generation HTTP client",
                    "license": "BSD-3-Clause",
                    "alternative_to": ["requests", "aiohttp"]
                },
                "requests": {
                    "version": "^2.31.0",
                    "description": "HTTP library for humans",
                    "license": "Apache-2.0",
                    "alternative_to": ["httpx", "urllib"]
                }
            },
            "data_validation": {
                "pydantic": {
                    "version": "^2.5.0",
                    "description": "Data validation using Python type hints",
                    "license": "MIT",
                    "alternative_to": ["marshmallow", "attrs"]
                },
                "marshmallow": {
                    "version": "^3.20.0",
                    "description": "Object serialization/deserialization",
                    "license": "MIT",
                    "alternative_to": ["pydantic", "dataclasses"]
                }
            },
            "web_framework": {
                "fastapi": {
                    "version": "^0.104.0",
                    "description": "Modern, fast web framework",
                    "license": "MIT",
                    "alternative_to": ["flask", "django"]
                },
                "flask": {
                    "version": "^3.0.0",
                    "description": "Lightweight WSGI web framework",
                    "license": "BSD-3-Clause",
                    "alternative_to": ["fastapi", "django"]
                }
            },
            "database_orm": {
                "sqlalchemy": {
                    "version": "^2.0.0",
                    "description": "SQL toolkit and ORM",
                    "license": "MIT",
                    "alternative_to": ["peewee", "tortoise-orm"]
                }
            },
            "testing": {
                "pytest": {
                    "version": "^7.4.0",
                    "description": "Testing framework",
                    "license": "MIT",
                    "alternative_to": ["unittest", "nose"]
                }
            },
            "cli": {
                "typer": {
                    "version": "^0.9.0",
                    "description": "Build CLI apps with type hints",
                    "license": "MIT",
                    "alternative_to": ["click", "argparse"]
                },
                "rich": {
                    "version": "^13.7.0",
                    "description": "Rich text and beautiful formatting",
                    "license": "MIT",
                    "alternative_to": ["colorama", "termcolor"]
                }
            }
        },
        "go": {
            "web": {
                "gin": {
                    "version": "v1.9.0",
                    "description": "HTTP web framework",
                    "license": "MIT",
                    "alternative_to": ["echo", "fiber"]
                },
                "echo": {
                    "version": "v4.11.0",
                    "description": "High performance web framework",
                    "license": "MIT",
                    "alternative_to": ["gin", "fiber"]
                }
            },
            "database": {
                "gorm": {
                    "version": "v1.25.0",
                    "description": "ORM library for Golang",
                    "license": "MIT",
                    "alternative_to": ["sqlx", "ent"]
                }
            },
            "config": {
                "viper": {
                    "version": "v1.17.0",
                    "description": "Configuration management",
                    "license": "MIT",
                    "alternative_to": ["koanf", "envconfig"]
                }
            }
        },
        "rust": {
            "web": {
                "axum": {
                    "version": "^0.7.0",
                    "description": "Ergonomic and modular web framework",
                    "license": "MIT",
                    "alternative_to": ["actix-web", "rocket"]
                }
            },
            "cli": {
                "clap": {
                    "version": "^4.4.0",
                    "description": "Command line argument parser",
                    "license": "MIT OR Apache-2.0",
                    "alternative_to": ["structopt", "argh"]
                }
            }
        }
    }
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["recommended-packages.json"] = self._generate_packages_json()
        files["package-audit.sh"] = self._generate_audit_script()
        files["library-guide.md"] = self._generate_guide()
        
        return files
    
    def recommend(self, language: str, category: str) -> List[Dict]:
        """Рекомендовать библиотеки"""
        results = []
        
        if language in self.LIBRARIES and category in self.LIBRARIES[language]:
            for name, info in self.LIBRARIES[language][category].items():
                results.append({
                    "name": name,
                    **info
                })
        
        return results
    
    def _generate_packages_json(self) -> str:
        import json
        return json.dumps(self.LIBRARIES, indent=2, ensure_ascii=False)
    
    def _generate_audit_script(self) -> str:
        return """#!/bin/bash
# Library Security Audit Script

echo "🔍 Running security audit..."

# Node.js projects
if [ -f "package.json" ]; then
    echo "📦 Checking npm packages..."
    npm audit
    
    echo "📊 Checking outdated packages..."
    npm outdated
    
    echo "🔐 Checking for known vulnerabilities..."
    npx audit-ci --moderate
fi

# Python projects
if [ -f "requirements.txt" ]; then
    echo "🐍 Checking Python packages..."
    pip-audit
    
    echo "📊 Checking for updates..."
    pip list --outdated
fi

# Go projects
if [ -f "go.mod" ]; then
    echo "🐹 Checking Go packages..."
    go list -json -m all | nancy sleuth
fi

echo "✅ Audit complete!"
"""
    
    def _generate_guide(self) -> str:
        return """# Library Selection Guide

## Selection Criteria

### 1. License
- ✅ MIT/Apache-2.0/BSD - Commercial safe
- ⚠️ GPL - Copyleft considerations
- ❌ SSPL/Commons Clause - Avoid for commercial use

### 2. Maintenance
- Last commit < 3 months
- Open issues < 100
- Active maintainers

### 3. Popularity
- Weekly downloads > 100K
- GitHub stars > 1000
- Used by major projects

### 4. Security
- No known vulnerabilities
- Regular security updates
- Security policy exists

## Installation Best Practices

### Pin Versions
```json
{
  "dependencies": {
    "library": "^1.2.3"  // Use exact or caret
  }
}
```

### Lock Files
Always commit lock files:
- `package-lock.json` (npm)
- `yarn.lock` (yarn)
- `poetry.lock` (poetry)
- `go.sum` (Go)

### Regular Updates
```bash
# Check outdated
npm outdated
pip list --outdated

# Update with care
npm update
pip install --upgrade package
```
"""


def main():
    parser = argparse.ArgumentParser(description="📚 Library-Agent — Library Selection")
    parser.add_argument("request", nargs="?", help="Категория библиотек")
    parser.add_argument("--language", "-l", default="javascript", help="Язык программирования")
    parser.add_argument("--category", "-c", help="Категория")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = LibraryAgent()
    
    if args.category:
        print(f"📚 {agent.NAME} рекомендует библиотеки:")
        print(f"Язык: {args.language}")
        print(f"Категория: {args.category}")
        print("-" * 50)
        
        libraries = agent.recommend(args.language, args.category)
        
        if libraries:
            for lib in libraries:
                print(f"\n📦 {lib['name']}@{lib['version']}")
                print(f"   {lib['description']}")
                print(f"   License: {lib['license']}")
                if 'weekly_downloads' in lib:
                    print(f"   Downloads: {lib['weekly_downloads']}")
                print(f"   Alternatives: {', '.join(lib['alternative_to'])}")
        else:
            print("Библиотеки не найдены")
    elif args.request:
        print(f"📚 {agent.NAME} создаёт: {args.request}")
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
        print(f"📚 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\nДоступные языки:")
        for lang in agent.LIBRARIES.keys():
            print(f"  - {lang}")


if __name__ == "__main__":
    main()
