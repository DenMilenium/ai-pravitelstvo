#!/usr/bin/env python3
"""
🧪 APITesting-Agent
API Testing & Documentation Specialist

Тестирование API, документация, Postman/Newman.
"""

import argparse
from pathlib import Path
from typing import Dict


class APITestingAgent:
    """
    🧪 APITesting-Agent
    
    Специализация: API Quality Assurance
    Задачи: Testing, Documentation, Validation
    """
    
    NAME = "🧪 APITesting-Agent"
    ROLE = "API Testing Specialist"
    EXPERTISE = ["API Testing", "Postman", "OpenAPI", "Contract Testing"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "api-tests.yml": self._generate_github_action(),
            "postman-collection.json": self._generate_postman_collection(),
            "contract-tests.py": self._generate_contract_tests()
        }
    
    def _generate_github_action(self) -> str:
        return '''name: API Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Start application
      run: docker-compose up -d app
    
    - name: Wait for service
      run: sleep 10
    
    - name: Run Postman tests
      uses: anthonyvscode/newman-action@v1
      with:
        collection: postman/api-collection.json
        environment: postman/test-environment.json
        reporters: cli,htmlextra
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: newman/
'''
    
    def _generate_postman_collection(self) -> str:
        return '''{
  "info": {
    "name": "API Test Collection",
    "description": "Automated API tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/health",
          "host": ["{{base_url}}"],
          "path": ["health"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 200', function () {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "pm.test('Response time is less than 500ms', function () {",
              "    pm.expect(pm.response.responseTime).to.be.below(500);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Get Users",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{auth_token}}"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/users",
          "host": ["{{base_url}}"],
          "path": ["api", "users"]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 200', function () {",
              "    pm.response.to.have.status(200);",
              "});",
              "",
              "pm.test('Response is array', function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData).to.be.an('array');",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
'''
    
    def _generate_contract_tests(self) -> str:
        return '''import requests
import pytest
from schemathesis import from_path

# Загрузка OpenAPI спецификации
schema = from_path("openapi.yaml")

# Автоматические тесты по схеме
@schema.parametrize()
def test_api_contract(case):
    """Тестирование API по контракту"""
    case.call_and_validate()


# Ручные тесты
BASE_URL = "http://localhost:8080"

class TestUsersAPI:
    """Тесты API пользователей"""
    
    def test_get_users(self):
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_user(self):
        data = {"name": "Test User", "email": "test@example.com"}
        response = requests.post(f"{BASE_URL}/api/users", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == data["name"]
    
    def test_get_user_by_id(self):
        response = requests.get(f"{BASE_URL}/api/users/1")
        assert response.status_code == 200
        assert "id" in response.json()
    
    def test_update_user(self):
        data = {"name": "Updated Name"}
        response = requests.patch(f"{BASE_URL}/api/users/1", json=data)
        assert response.status_code == 200
    
    def test_delete_user(self):
        response = requests.delete(f"{BASE_URL}/api/users/1")
        assert response.status_code == 204
    
    def test_invalid_user_returns_404(self):
        response = requests.get(f"{BASE_URL}/api/users/99999")
        assert response.status_code == 404


class TestAuthAPI:
    """Тесты аутентификации"""
    
    def test_login_success(self):
        data = {"email": "test@example.com", "password": "password"}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        assert response.status_code == 200
        assert "token" in response.json()
    
    def test_login_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrong"}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        assert response.status_code == 401
    
    def test_protected_endpoint_without_token(self):
        response = requests.get(f"{BASE_URL}/api/profile")
        assert response.status_code == 401
'''


def main():
    parser = argparse.ArgumentParser(description="🧪 APITesting-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = APITestingAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🧪 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
