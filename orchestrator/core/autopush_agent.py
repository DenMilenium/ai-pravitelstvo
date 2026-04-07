"""
📤 AutoPush Agent
Автоматический push кода в GitHub после выполнения задачи
"""

import os
import base64
import requests
from typing import Dict, List, Optional
from datetime import datetime


class AutoPushAgent:
    """
    🤖 AutoPush Agent
    
    Автоматически:
    1. Создаёт коммит с кодом из артефактов
    2. Пушит в ветку agent-task-<task_id>
    3. Создаёт Pull Request
    4. Обновляет статус задачи со ссылкой на PR
    """
    
    def __init__(self, token: str = None, repo: str = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.repo = repo or os.environ.get('GITHUB_REPO', 'DenMilenium/ai-pravitelstvo')
        self.api_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_default_branch(self) -> str:
        """Получает дефолтную ветку (main/master)"""
        response = requests.get(
            f"{self.api_url}/repos/{self.repo}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['default_branch']
    
    def get_latest_commit_sha(self, branch: str = None) -> str:
        """Получает SHA последнего коммита в ветке"""
        branch = branch or self.get_default_branch()
        response = requests.get(
            f"{self.api_url}/repos/{self.repo}/git/ref/heads/{branch}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['object']['sha']
    
    def create_branch(self, branch_name: str, base_branch: str = None) -> dict:
        """Создаёт новую ветку от базовой"""
        base_sha = self.get_latest_commit_sha(base_branch)
        
        response = requests.post(
            f"{self.api_url}/repos/{self.repo}/git/refs",
            headers=self.headers,
            json={
                "ref": f"refs/heads/{branch_name}",
                "sha": base_sha
            }
        )
        response.raise_for_status()
        return response.json()
    
    def create_or_update_file(
        self,
        branch: str,
        file_path: str,
        content: str,
        message: str,
        task_id: str = None
    ) -> dict:
        """
        Создаёт или обновляет файл в репозитории
        
        Args:
            branch: Название ветки
            file_path: Путь к файлу (например, "projects/task-001/index.html")
            content: Содержимое файла
            message: Сообщение коммита
            task_id: ID задачи для отслеживания
        """
        # Кодируем контент в base64
        content_b64 = base64.b64encode(content.encode()).decode()
        
        # Проверяем, существует ли файл
        get_response = requests.get(
            f"{self.api_url}/repos/{self.repo}/contents/{file_path}?ref={branch}",
            headers=self.headers
        )
        
        file_data = {
            "message": message,
            "content": content_b64,
            "branch": branch
        }
        
        # Если файл существует, добавляем sha для обновления
        if get_response.status_code == 200:
            file_data["sha"] = get_response.json()["sha"]
        
        response = requests.put(
            f"{self.api_url}/repos/{self.repo}/contents/{file_path}",
            headers=self.headers,
            json=file_data
        )
        response.raise_for_status()
        return response.json()
    
    def push_artifacts(
        self,
        task_id: str,
        task_title: str,
        artifacts: Dict[str, str],
        project_name: str = None
    ) -> dict:
        """
        Пушит все артефакты задачи в GitHub
        
        Args:
            task_id: ID задачи
            task_title: Название задачи
            artifacts: Словарь {filename: content}
            project_name: Название проекта
            
        Returns:
            Dict с branch_name, commit_url, files_pushed
        """
        # Создаём ветку
        branch_name = f"agent-task-{task_id}"
        base_branch = self.get_default_branch()
        
        try:
            self.create_branch(branch_name, base_branch)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                # Ветка уже существует — используем её
                pass
            else:
                raise
        
        # Пушим каждый файл
        files_pushed = []
        project_folder = project_name.lower().replace(' ', '-') if project_name else 'unnamed-project'
        
        for filename, content in artifacts.items():
            # Формируем путь: projects/<project-name>/task-<id>/<filename>
            file_path = f"generated-projects/{project_folder}/task-{task_id}/{filename}"
            
            commit_msg = f"🤖 [{task_id}] {task_title}: {filename}"
            
            result = self.create_or_update_file(
                branch=branch_name,
                file_path=file_path,
                content=content,
                message=commit_msg,
                task_id=task_id
            )
            
            files_pushed.append({
                'filename': filename,
                'path': file_path,
                'commit_url': result['commit']['html_url']
            })
        
        return {
            'branch_name': branch_name,
            'base_branch': base_branch,
            'files_pushed': files_pushed,
            'files_count': len(files_pushed)
        }
    
    def create_pull_request(
        self,
        branch_name: str,
        task_id: str,
        task_title: str,
        task_description: str = None,
        agent_type: str = None
    ) -> dict:
        """
        Создаёт Pull Request для ветки с кодом
        """
        base_branch = self.get_default_branch()
        
        # Формируем заголовок и описание PR
        title = f"🤖 [{agent_type.upper() if agent_type else 'AGENT'}] {task_title}"
        
        body = f"""## 🤖 Автоматически сгенерированный код

**Задача:** {task_title}  
**ID:** `{task_id}`  
**Агент:** {agent_type or 'Unknown'}  
**Время генерации:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Описание
{task_description or 'Код сгенерирован AI агентом в рамках проекта AI Правительство.'}

### Проверка
- [ ] Код протестирован
- [ ] Нет уязвимостей
- [ ] Соответствует стандартам

---
*Этот PR создан автоматически. Для обсуждения используйте комментарии.*
"""
        
        response = requests.post(
            f"{self.api_url}/repos/{self.repo}/pulls",
            headers=self.headers,
            json={
                "title": title,
                "body": body,
                "head": branch_name,
                "base": base_branch
            }
        )
        response.raise_for_status()
        return response.json()
    
    def auto_push_task(
        self,
        task_id: str,
        task_title: str,
        task_description: str,
        agent_type: str,
        artifacts: Dict[str, str],
        project_name: str = None
    ) -> dict:
        """
        Полный цикл автопуша:
        1. Создать ветку
        2. Запушить артефакты
        3. Создать PR
        
        Returns:
            Dict с ссылками на branch, commits, PR
        """
        # 1. Пушим артефакты
        push_result = self.push_artifacts(
            task_id=task_id,
            task_title=task_title,
            artifacts=artifacts,
            project_name=project_name
        )
        
        # 2. Создаём PR
        pr_result = self.create_pull_request(
            branch_name=push_result['branch_name'],
            task_id=task_id,
            task_title=task_title,
            task_description=task_description,
            agent_type=agent_type
        )
        
        return {
            'success': True,
            'task_id': task_id,
            'branch_name': push_result['branch_name'],
            'base_branch': push_result['base_branch'],
            'files_pushed': push_result['files_count'],
            'pr_number': pr_result['number'],
            'pr_url': pr_result['html_url'],
            'pr_created_at': pr_result['created_at'],
            'commits': [f['commit_url'] for f in push_result['files_pushed']]
        }


if __name__ == "__main__":
    # Тест
    import os
    
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ Укажи GITHUB_TOKEN")
        exit(1)
    
    agent = AutoPushAgent(token=token)
    
    print("🚀 Тест AutoPush Agent")
    
    # Тест: создать ветку и запушить файл
    try:
        result = agent.push_artifacts(
            task_id="test-001",
            task_title="Тестовая задача",
            artifacts={
                "README.md": "# Тест\n\nЭто тестовый файл."
            },
            project_name="Test Project"
        )
        print(f"✅ Файлы запушены в ветку: {result['branch_name']}")
        print(f"   Количество файлов: {result['files_count']}")
        
        # Создать PR
        pr = agent.create_pull_request(
            branch_name=result['branch_name'],
            task_id="test-001",
            task_title="Тестовая задача",
            agent_type="test"
        )
        print(f"✅ PR создан: {pr['html_url']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
