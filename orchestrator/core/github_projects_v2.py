"""
🔗 GitHub Projects v2 (GraphQL) Integration
Новое поколение GitHub Projects с автоматизацией
"""

import os
import requests
from typing import Dict, List, Optional


class GitHubProjectsV2:
    """
    🚀 GitHub Projects v2 (GraphQL API)
    
    Возможности:
    - Создание Project v2 (новый формат)
    - Автоматизация колонок (Todo → In Progress → Done)
    - Кастомные поля (Priority, Status, Assignee)
    - Связь Issues с Project items
    """
    
    def __init__(self, token: str = None, org: str = None, repo: str = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.org = org or 'DenMilenium'
        self.repo = repo or 'ai-pravitelstvo'
        
        self.api_url = "https://api.github.com/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def _graphql_query(self, query: str, variables: dict = None) -> dict:
        """Выполняет GraphQL запрос"""
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"query": query, "variables": variables or {}},
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"GraphQL Error: {response.status_code} - {response.text}")
        
        data = response.json()
        if 'errors' in data:
            raise Exception(f"GraphQL Errors: {data['errors']}")
        
        return data['data']
    
    def get_repository_id(self) -> str:
        """Получает ID репозитория для GraphQL"""
        query = """
        query($owner: String!, $repo: String!) {
            repository(owner: $owner, name: $repo) {
                id
            }
        }
        """
        result = self._graphql_query(query, {"owner": self.org, "repo": self.repo})
        return result['repository']['id']
    
    def create_project_v2(self, title: str, description: str = None) -> dict:
        """
        Создаёт Project v2
        
        Args:
            title: Название проекта
            description: Описание
            
        Returns:
            Dict с id, url, fields
        """
        # Сначала получаем ID владельца (организации или пользователя)
        query_owner = """
        query($login: String!) {
            user(login: $login) {
                id
            }
            organization(login: $login) {
                id
            }
        }
        """
        
        owner_result = self._graphql_query(query_owner, {"login": self.org})
        
        # Определяем, это организация или пользователь
        if owner_result.get('organization'):
            owner_id = owner_result['organization']['id']
        else:
            owner_id = owner_result['user']['id']
        
        # Создаём проект
        mutation = """
        mutation($ownerId: ID!, $title: String!, $description: String) {
            createProjectV2(
                input: {
                    ownerId: $ownerId
                    title: $title
                    description: $description
                }
            ) {
                projectV2 {
                    id
                    title
                    url
                    number
                    createdAt
                }
            }
        }
        """
        
        result = self._graphql_query(mutation, {
            "ownerId": owner_id,
            "title": title,
            "description": description or f"AI Правительство - {title}"
        })
        
        return result['createProjectV2']['projectV2']
    
    def add_custom_fields(self, project_id: str) -> dict:
        """
        Добавляет кастомные поля в проект:
        - Priority (High/Medium/Low)
        - Status (Backlog/Todo/In Progress/Done)
        - Agent Type (frontend/backend/etc)
        """
        fields = {}
        
        # 1. Поле Priority
        priority_mutation = """
        mutation($projectId: ID!, $name: String!) {
            createProjectV2Field(
                input: {
                    projectId: $projectId
                    dataType: SINGLE_SELECT
                    name: $name
                    singleSelectOptions: [
                        {name: "🔴 High", color: RED},
                        {name: "🟡 Medium", color: YELLOW},
                        {name: "🟢 Low", color: GREEN}
                    ]
                }
            ) {
                projectV2Field {
                    id
                    name
                }
            }
        }
        """
        
        priority_result = self._graphql_query(priority_mutation, {
            "projectId": project_id,
            "name": "Priority"
        })
        fields['priority'] = priority_result['createProjectV2Field']['projectV2Field']
        
        # 2. Поле Agent Type
        agent_mutation = """
        mutation($projectId: ID!, $name: String!) {
            createProjectV2Field(
                input: {
                    projectId: $projectId
                    dataType: SINGLE_SELECT
                    name: $name
                    singleSelectOptions: [
                        {name: "🎨 Frontend", color: BLUE},
                        {name: "⚙️ Backend", color: PURPLE},
                        {name: "📱 Mobile", color: GREEN},
                        {name: "💻 Desktop", color: GRAY},
                        {name: "🚀 DevOps", color: ORANGE},
                        {name: "☁️ Cloud", color: BLUE},
                        {name: "🧠 AI/ML", color: PINK},
                        {name: "🔒 Security", color: RED},
                        {name: "📝 Content", color: YELLOW}
                    ]
                }
            ) {
                projectV2Field {
                    id
                    name
                }
            }
        }
        """
        
        agent_result = self._graphql_query(agent_mutation, {
            "projectId": project_id,
            "name": "Agent Type"
        })
        fields['agent_type'] = agent_result['createProjectV2Field']['projectV2Field']
        
        # 3. Текстовое поле для Project ID
        text_mutation = """
        mutation($projectId: ID!, $name: String!) {
            createProjectV2Field(
                input: {
                    projectId: $projectId
                    dataType: TEXT
                    name: $name
                }
            ) {
                projectV2Field {
                    id
                    name
                }
            }
        }
        """
        
        text_result = self._graphql_query(text_mutation, {
            "projectId": project_id,
            "name": "AI Project ID"
        })
        fields['ai_project_id'] = text_result['createProjectV2Field']['projectV2Field']
        
        return fields
    
    def create_issue_and_add_to_project(
        self,
        project_id: str,
        title: str,
        body: str,
        priority: str = "Medium",
        agent_type: str = None,
        ai_project_id: str = None
    ) -> dict:
        """
        Создаёт Issue и добавляет в Project v2
        """
        # Получаем ID репозитория
        repo_id = self.get_repository_id()
        
        # Создаём Issue
        issue_mutation = """
        mutation($repositoryId: ID!, $title: String!, $body: String) {
            createIssue(
                input: {
                    repositoryId: $repositoryId
                    title: $title
                    body: $body
                }
            ) {
                issue {
                    id
                    number
                    url
                }
            }
        }
        """
        
        issue_result = self._graphql_query(issue_mutation, {
            "repositoryId": repo_id,
            "title": title,
            "body": body
        })
        
        issue = issue_result['createIssue']['issue']
        
        # Добавляем в Project
        add_mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
            addProjectV2ItemById(
                input: {
                    projectId: $projectId
                    contentId: $contentId
                }
            ) {
                item {
                    id
                }
            }
        }
        """
        
        add_result = self._graphql_query(add_mutation, {
            "projectId": project_id,
            "contentId": issue['id']
        })
        
        item_id = add_result['addProjectV2ItemById']['item']['id']
        
        # TODO: Установить кастомные поля (Priority, Agent Type)
        # Требуется дополнительная мутация updateProjectV2ItemFieldValue
        
        return {
            'issue': issue,
            'project_item_id': item_id
        }
    
    def update_item_status(self, project_id: str, item_id: str, status: str) -> dict:
        """
        Обновляет статус item в проекте
        status: "Todo" | "In Progress" | "Done"
        """
        # Получаем ID поля Status
        fields_query = """
        query($projectId: ID!) {
            node(id: $projectId) {
                ... on ProjectV2 {
                    fields(first: 20) {
                        nodes {
                            ... on ProjectV2SingleSelectField {
                                id
                                name
                                options {
                                    id
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        fields_result = self._graphql_query(fields_query, {"projectId": project_id})
        
        # Находим поле Status и нужную опцию
        status_field = None
        status_option = None
        
        for field in fields_result['node']['fields']['nodes']:
            if field.get('name') == 'Status':
                status_field = field
                for opt in field.get('options', []):
                    if opt['name'] == status:
                        status_option = opt
                        break
                break
        
        if not status_field or not status_option:
            raise Exception(f"Status field or option '{status}' not found")
        
        # Обновляем поле
        mutation = """
        mutation(
            $projectId: ID!
            $itemId: ID!
            $fieldId: ID!
            $optionId: String!
        ) {
            updateProjectV2ItemFieldValue(
                input: {
                    projectId: $projectId
                    itemId: $itemId
                    fieldId: $fieldId
                    value: {
                        singleSelectOptionId: $optionId
                    }
                }
            ) {
                projectV2Item {
                    id
                }
            }
        }
        """
        
        result = self._graphql_query(mutation, {
            "projectId": project_id,
            "itemId": item_id,
            "fieldId": status_field['id'],
            "optionId": status_option['id']
        })
        
        return result['updateProjectV2ItemFieldValue']['projectV2Item']
    
    def sync_project_with_github(
        self,
        ai_project_id: str,
        ai_project_name: str,
        tasks: List[dict]
    ) -> dict:
        """
        Полная синхронизация AI проекта с GitHub Projects v2
        
        Args:
            ai_project_id: ID проекта в нашей системе
            ai_project_name: Название проекта
            tasks: Список задач [{title, description, agent_type, priority}]
            
        Returns:
            Dict с url проекта и списком созданных issues
        """
        # 1. Создаём Project v2
        project = self.create_project_v2(
            title=f"🤖 {ai_project_name}",
            description=f"AI Правительство проект: {ai_project_name}\n\nID: {ai_project_id}"
        )
        
        # 2. Добавляем кастомные поля
        fields = self.add_custom_fields(project['id'])
        
        # 3. Создаём issues для каждой задачи
        created_issues = []
        for task in tasks:
            issue_data = self.create_issue_and_add_to_project(
                project_id=project['id'],
                title=task['title'],
                body=task.get('description', ''),
                priority=task.get('priority', 'Medium'),
                agent_type=task.get('agent_type'),
                ai_project_id=ai_project_id
            )
            created_issues.append(issue_data)
        
        return {
            'project_url': project['url'],
            'project_number': project['number'],
            'issues_created': len(created_issues),
            'issues': created_issues
        }


if __name__ == "__main__":
    # Тест
    import os
    
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("❌ Укажи GITHUB_TOKEN")
        exit(1)
    
    client = GitHubProjectsV2(token=token)
    
    print("🚀 Тест GitHub Projects v2")
    
    try:
        # Получаем ID репозитория
        repo_id = client.get_repository_id()
        print(f"✅ Repository ID: {repo_id[:20]}...")
        
        # Создаём тестовый проект
        project = client.create_project_v2(
            title="🧪 Тестовый проект v2",
            description="Тест создания Project v2 через GraphQL"
        )
        print(f"✅ Project created: {project['url']}")
        print(f"   Number: {project['number']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
