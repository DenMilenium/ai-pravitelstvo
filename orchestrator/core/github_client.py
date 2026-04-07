"""
🔗 GitHub Integration
Интеграция с GitHub API для управления задачами и проектами
"""

import os
import requests
from typing import Dict, List, Optional


class GitHubClient:
    """
    Клиент для работы с GitHub API
    """
    
    def __init__(self, token: str = None, repo: str = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.repo = repo or os.environ.get('GITHUB_REPO', 'DenMilenium/ai-pravitelstvo')
        self.api_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Выполняет запрос к GitHub API"""
        url = f"{self.api_url}{endpoint}"
        response = requests.request(
            method, 
            url, 
            headers=self.headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    # ========== Issues ==========
    
    def create_issue(self, title: str, body: str, labels: List[str] = None, assignee: str = None) -> dict:
        """Создаёт issue (задачу) в репозитории"""
        data = {
            "title": title,
            "body": body,
            "labels": labels or [],
        }
        if assignee:
            data["assignee"] = assignee
        
        return self._request(
            "POST", 
            f"/repos/{self.repo}/issues",
            data
        )
    
    def list_issues(self, state: str = "open") -> List[dict]:
        """Получает список задач"""
        return self._request(
            "GET",
            f"/repos/{self.repo}/issues?state={state}"
        )
    
    def update_issue(self, issue_number: int, state: str = None, body: str = None) -> dict:
        """Обновляет задачу"""
        data = {}
        if state:
            data["state"] = state
        if body:
            data["body"] = body
        
        return self._request(
            "PATCH",
            f"/repos/{self.repo}/issues/{issue_number}",
            data
        )
    
    def add_comment(self, issue_number: int, body: str) -> dict:
        """Добавляет комментарий к задаче"""
        return self._request(
            "POST",
            f"/repos/{self.repo}/issues/{issue_number}/comments",
            {"body": body}
        )
    
    # ========== Projects (Beta) ==========
    
    def list_projects(self) -> List[dict]:
        """Получает список проектов репозитория"""
        return self._request(
            "GET",
            f"/repos/{self.repo}/projects"
        )
    
    def create_project(self, name: str, body: str = None) -> dict:
        """Создаёт проект в GitHub Projects"""
        # Требуется header для Projects API
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.inertia-preview+json"
        
        url = f"{self.api_url}/repos/{self.repo}/projects"
        response = requests.post(
            url,
            headers=headers,
            json={"name": name, "body": body},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def add_issue_to_project(self, project_id: int, issue_id: int) -> dict:
        """Добавляет задачу в проект"""
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.inertia-preview+json"
        
        # Сначала получаем колонки проекта
        columns_url = f"{self.api_url}/projects/{project_id}/columns"
        columns_resp = requests.get(columns_url, headers=headers, timeout=30)
        columns_resp.raise_for_status()
        columns = columns_resp.json()
        
        if not columns:
            raise ValueError("У проекта нет колонок")
        
        # Добавляем в первую колонку (To Do)
        card_url = f"{self.api_url}/projects/columns/{columns[0]['id']}/cards"
        response = requests.post(
            card_url,
            headers=headers,
            json={"content_id": issue_id, "content_type": "Issue"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    # ========== Repository Contents ==========
    
    def create_or_update_file(self, path: str, content: str, message: str, branch: str = "main") -> dict:
        """Создаёт или обновляет файл в репозитории"""
        import base64
        
        # Проверяем существование файла
        try:
            existing = self._request("GET", f"/repos/{self.repo}/contents/{path}?ref={branch}")
            sha = existing.get("sha")
        except:
            sha = None
        
        data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch
        }
        if sha:
            data["sha"] = sha
        
        return self._request(
            "PUT",
            f"/repos/{self.repo}/contents/{path}",
            data
        )
    
    def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> dict:
        """Создаёт Pull Request"""
        return self._request(
            "POST",
            f"/repos/{self.repo}/pulls",
            {"title": title, "body": body, "head": head, "base": base}
        )
    
    # ========== Sync with Orchestrator ==========
    
    def sync_task_to_issue(self, task: dict) -> dict:
        """Синхронизирует задачу из Orchestrator в GitHub Issue"""
        title = f"[{task['agent_type'].upper()}] {task['title']}"
        body = f"""## 🎯 Задача

**ID:** {task['id']}  
**Агент:** {task['agent_type']}  
**Статус:** {task['status']}  
**Приоритет:** {task.get('priority', 'normal')}

## 📝 Описание
{task.get('description', 'Нет описания')}

## 🔗 Связь
- Orchestrator Task ID: `{task['id']}`
- Project ID: `{task.get('project_id', 'N/A')}`

---
*Сгенерировано AI Правительством 🤖🏛️*
"""
        labels = [task['agent_type'], task['status']]
        if task.get('priority') == 'critical':
            labels.append('critical')
        
        return self.create_issue(title, body, labels=labels)
    
    def sync_project_to_github(self, project: dict, tasks: List[dict]) -> dict:
        """Создаёт GitHub Project и добавляет туда задачи как issues"""
        # Создаём проект
        gh_project = self.create_project(
            name=project['name'],
            body=f"{project.get('description', '')}\n\nСоздано через AI Правительство Dashboard"
        )
        
        project_id = gh_project['id']
        created_issues = []
        
        # Создаём issues для задач и добавляем в проект
        for task in tasks:
            issue = self.sync_task_to_issue(task)
            created_issues.append(issue)
            
            # Добавляем issue в проект
            try:
                self.add_issue_to_project(project_id, issue['id'])
            except Exception as e:
                print(f"⚠️ Не удалось добавить в проект: {e}")
        
        return {
            'project': gh_project,
            'issues': created_issues,
            'total': len(created_issues)
        }


# Singleton instance
github_client = None

def get_github_client() -> GitHubClient:
    """Получает или создаёт клиент GitHub"""
    global github_client
    if github_client is None:
        github_client = GitHubClient()
    return github_client


if __name__ == "__main__":
    # Тест
    client = get_github_client()
    print("GitHub клиент создан")
    print(f"Репозиторий: {client.repo}")
    
    # Получаем список issues
    try:
        issues = client.list_issues()
        print(f"Открытых задач: {len(issues)}")
    except Exception as e:
        print(f"Ошибка: {e}")
