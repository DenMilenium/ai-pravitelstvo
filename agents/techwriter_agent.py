#!/usr/bin/env python3
"""
📚 TechWriter-Agent
Technical Writer агент

Создаёт:
- Документацию API
- README файлы
- User Guides
- Wiki статьи
"""

import argparse
from pathlib import Path
from typing import Dict


class TechWriterAgent:
    """
    📚 TechWriter-Agent
    
    Специализация: Technical Documentation
    Экспертиза: API docs, README, Guides, Markdown
    """
    
    NAME = "📚 TechWriter-Agent"
    ROLE = "Technical Writer"
    EXPERTISE = ["API Documentation", "README", "User Guides", "Wiki", "Markdown"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        request_lower = request.lower()
        files = {}
        
        if "readme" in request_lower:
            files = self._generate_readme(request)
        elif "api" in request_lower or "openapi" in request_lower:
            files = self._generate_api_docs(request)
        elif "guide" in request_lower or "руководство" in request_lower:
            files = self._generate_guide(request)
        elif "wiki" in request_lower:
            files = self._generate_wiki(request)
        elif "changelog" in request_lower:
            files = self._generate_changelog(request)
        else:
            files = self._generate_readme(request)
        
        return files
    
    def _generate_readme(self, project: str) -> Dict[str, str]:
        files = {}
        
        files["README.md"] = f"""# 🚀 {project}

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Version](https://img.shields.io/badge/version-1.0.0-orange)]()

> Краткое описание проекта - что он делает и зачем нужен.

---

## ✨ Features

- ✅ **Feature 1** - Описание возможности
- ✅ **Feature 2** - Описание возможности
- ✅ **Feature 3** - Описание возможности

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/username/{project.lower().replace(' ', '-')}.git
cd {project.lower().replace(' ', '-')}

# Install dependencies
npm install

# Run development server
npm run dev
```

### Usage

```javascript
import {{ MyLib }} from '{project.lower().replace(' ', '-')}';

const app = new MyLib();
app.run();
```

---

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [API Reference](docs/API.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

---

## 🛠️ Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS
- **Backend:** Node.js, Express
- **Database:** PostgreSQL
- **Deployment:** Docker, Kubernetes

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- [Library/Tool 1](link)
- [Library/Tool 2](link)

---

<div align="center">

Made with ❤️ by [Your Name](https://github.com/username)

</div>
"""
        
        return files
    
    def _generate_api_docs(self, api: str) -> Dict[str, str]:
        files = {}
        
        files["API.md"] = f"""# 📡 API Documentation: {api}

**Base URL:** `https://api.example.com/v1`  
**Authentication:** Bearer Token

---

## Authentication

All API requests require authentication using a Bearer token.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.example.com/v1/resource
```

---

## Endpoints

### GET /resource

Retrieve a list of resources.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Items per page (default: 10) |
| sort | string | No | Sort field (default: "created_at") |

**Response:**

```json
{{
  "data": [
    {{
      "id": "123",
      "name": "Example",
      "created_at": "2024-01-01T00:00:00Z"
    }}
  ],
  "meta": {{
    "page": 1,
    "total": 100,
    "pages": 10
  }}
}}
```

**Status Codes:**

- `200` - Success
- `401` - Unauthorized
- `403` - Forbidden
- `500` - Server Error

---

### POST /resource

Create a new resource.

**Request Body:**

```json
{{
  "name": "New Resource",
  "description": "Description here"
}}
```

**Response:**

```json
{{
  "id": "124",
  "name": "New Resource",
  "description": "Description here",
  "created_at": "2024-01-01T00:00:00Z"
}}
```

**Status Codes:**

- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized

---

### GET /resource/:id

Retrieve a specific resource.

**Response:**

```json
{{
  "id": "123",
  "name": "Example",
  "description": "Description",
  "created_at": "2024-01-01T00:00:00Z"
}}
```

---

### PUT /resource/:id

Update a resource.

**Request Body:**

```json
{{
  "name": "Updated Name",
  "description": "Updated description"
}}
```

---

### DELETE /resource/:id

Delete a resource.

**Response:** `204 No Content`

---

## Error Handling

All errors follow this format:

```json
{{
  "error": {{
    "code": "INVALID_REQUEST",
    "message": "The request is invalid",
    "details": [
      {{
        "field": "name",
        "message": "Name is required"
      }}
    ]
  }}
}}
```

---

## Rate Limiting

- 1000 requests per hour
- Rate limit headers included in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
"""
        
        files["openapi.yaml"] = """openapi: 3.0.0
info:
  title: API
  version: 1.0.0
  description: API Documentation

servers:
  - url: https://api.example.com/v1

paths:
  /resource:
    get:
      summary: List resources
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Resource'
    post:
      summary: Create resource
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResourceInput'
      responses:
        '201':
          description: Created

components:
  schemas:
    Resource:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        created_at:
          type: string
          format: date-time
    
    ResourceInput:
      type: object
      required:
        - name
      properties:
        name:
          type: string
        description:
          type: string
"""
        
        return files
    
    def _generate_guide(self, topic: str) -> Dict[str, str]:
        files = {}
        
        files["GUIDE.md"] = f"""# 📖 User Guide: {topic}

**Last Updated:** 2024-01-01  
**Version:** 1.0

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Concepts](#core-concepts)
4. [Advanced Usage](#advanced-usage)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

---

## Introduction

Welcome to {topic}! This guide will help you understand and use the system effectively.

### What You'll Learn

- How to set up your environment
- Core concepts and terminology
- Step-by-step tutorials
- Best practices
- Common troubleshooting

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Installation

Step-by-step installation instructions...

### First Steps

1. **Step One:** Description
   ```bash
   # Example command
   ```

2. **Step Two:** Description
   ```bash
   # Example command
   ```

---

## Core Concepts

### Concept 1

Explanation of concept 1...

### Concept 2

Explanation of concept 2...

---

## Advanced Usage

### Scenario 1

```javascript
// Example code
```

### Scenario 2

```javascript
// Example code
```

---

## Troubleshooting

### Problem: Common Issue

**Symptoms:** What you see

**Solution:**
1. Step 1
2. Step 2
3. Step 3

### Problem: Another Issue

**Symptoms:** What you see

**Solution:**
- Check this
- Verify that
- Try restarting

---

## FAQ

**Q: Question 1?**  
A: Answer 1

**Q: Question 2?**  
A: Answer 2

**Q: Question 3?**  
A: Answer 3

---

## Support

Need help? Contact us:

- 📧 Email: support@example.com
- 💬 Chat: [Discord](https://discord.gg/example)
- 🐛 Issues: [GitHub Issues](https://github.com/example/issues)

---

*This documentation is maintained by the TechWriter-Agent*
"""
        
        return files
    
    def _generate_wiki(self, topic: str) -> Dict[str, str]:
        files = {}
        
        files["wiki/Home.md"] = f"""# Welcome to {topic} Wiki

This is the central knowledge base for {topic}.

## Quick Links

- [[Getting Started]]
- [[Architecture Overview]]
- [[API Reference]]
- [[Deployment Guide]]
- [[Troubleshooting]]
- [[Changelog]]

## Contributing

To contribute to this wiki:
1. Clone the wiki repository
2. Make your changes
3. Submit a pull request

---

_Last updated: 2024_
"""
        
        return files
    
    def _generate_changelog(self, project: str) -> Dict[str, str]:
        files = {}
        
        files["CHANGELOG.md"] = f"""# Changelog: {project}

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature in development

### Changed
- Improvements being made

## [1.0.0] - 2024-01-01

### Added
- Initial release
- Core functionality
- API endpoints
- Documentation

### Security
- Basic authentication
- Input validation

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2024-01-01 | Initial release |
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="📚 TechWriter-Agent — Documentation")
    parser.add_argument("request", nargs="?", help="Что документировать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = TechWriterAgent()
    
    if args.request:
        print(f"📚 {agent.NAME} пишет: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)
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


if __name__ == "__main__":
    main()
