"""
🚀 Deploy Agent
Автоматический деплой проектов на сервер
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from orchestrator.core.database import Database, TaskStatus


class DeployAgent:
    """
    Агент деплоя проектов
    Разворачивает собранные проекты на сервере
    """
    
    def __init__(self, db: Database = None):
        self.db = db or Database()
        self.projects_dir = Path("/var/www/ai-pravitelstvo/public/projects")
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def deploy_project(self, project_id: str) -> Dict:
        """
        Деплой проекта на сервер
        
        Returns:
            {
                'success': bool,
                'url': str,
                'message': str,
                'files_deployed': int
            }
        """
        # Получаем проект
        project = self.db.get_project(project_id)
        if not project:
            return {'success': False, 'message': 'Проект не найден'}
        
        # Проверяем что проект завершён
        if project.status != 'completed':
            return {'success': False, 'message': 'Проект ещё не завершён. Сначала соберите ZIP.'}
        
        # Получаем все артефакты проекта
        artifacts = self.db.get_project_artifacts(project_id)
        if not artifacts:
            return {'success': False, 'message': 'Нет артефактов для деплоя'}
        
        # Создаём папку для проекта
        deploy_dir = self.projects_dir / project_id
        deploy_dir.mkdir(exist_ok=True)
        
        # Очищаем старые файлы
        for item in deploy_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        
        # Разворачиваем файлы
        files_deployed = 0
        for artifact in artifacts:
            file_path = deploy_dir / artifact.file_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(artifact.content or '')
            
            files_deployed += 1
        
        # Создаём .htaccess для Apache/nginx
        self._create_web_config(deploy_dir)
        
        # Обновляем статус проекта
        self.db.update_project(project_id, status='deployed')
        
        # Формируем URL
        domain = os.environ.get('DEPLOY_DOMAIN', '194.67.66.120')
        url = f"http://{domain}/projects/{project_id}/"
        
        return {
            'success': True,
            'url': url,
            'message': f'✅ Проект опубликован!',
            'files_deployed': files_deployed,
            'deploy_dir': str(deploy_dir)
        }
    
    def _create_web_config(self, deploy_dir: Path):
        """Создаёт конфигурацию веб-сервера"""
        # .htaccess для Apache
        htaccess = deploy_dir / '.htaccess'
        htaccess.write_text('''# Apache config
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^ index.html [L]
</IfModule>

# Кэширование статики
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 week"
    ExpiresByType application/javascript "access plus 1 week"
    ExpiresByType image/* "access plus 1 month"
</IfModule>
''')
        
        # nginx.conf для Nginx
        nginx_conf = deploy_dir / 'nginx.conf'
        nginx_conf.write_text(f'''# Nginx config for {deploy_dir.name}
server {{
    listen 80;
    server_name _;
    root {deploy_dir};
    index index.html;
    
    location / {{
        try_files $uri $uri/ /index.html;
    }}
    
    # Сжатие
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
}}''')
    
    def get_deployed_projects(self) -> List[Dict]:
        """Получить список развёрнутых проектов"""
        deployed = []
        
        for project_dir in self.projects_dir.iterdir():
            if project_dir.is_dir():
                index_file = project_dir / 'index.html'
                if index_file.exists():
                    deployed.append({
                        'project_id': project_dir.name,
                        'url': f'/projects/{project_dir.name}/',
                        'last_modified': datetime.fromtimestamp(
                            index_file.stat().st_mtime
                        ).isoformat()
                    })
        
        return deployed
    
    def undeploy_project(self, project_id: str) -> Dict:
        """Удалить деплой проекта"""
        deploy_dir = self.projects_dir / project_id
        
        if not deploy_dir.exists():
            return {'success': False, 'message': 'Проект не был развёрнут'}
        
        # Удаляем папку
        shutil.rmtree(deploy_dir)
        
        # Обновляем статус
        self.db.update_project(project_id, status='completed')
        
        return {
            'success': True,
            'message': '✅ Проект снят с публикации'
        }


# ========== Методы для интеграции с Flask API ==========

def deploy_project_api(project_id: str, db: Database = None) -> Dict:
    """API-обёртка для деплоя"""
    agent = DeployAgent(db)
    return agent.deploy_project(project_id)


def get_deployed_projects_api(db: Database = None) -> List[Dict]:
    """API-обёртка для получения списка"""
    agent = DeployAgent(db)
    return agent.get_deployed_projects()


def undeploy_project_api(project_id: str, db: Database = None) -> Dict:
    """API-обёртка для удаления деплоя"""
    agent = DeployAgent(db)
    return agent.undeploy_project(project_id)
