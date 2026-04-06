"""
📦 Project Manager
Управление проектами и сборка артефактов
"""

import os
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from orchestrator.core.database import Database, ProjectStatus


class ProjectManager:
    """
    📦 Project Manager
    
    Управляет жизненным циклом проекта:
    - Сбор артефактов
    - Создание ZIP-архива
    - Деплой на сервер
    """
    
    def __init__(self, db: Database = None, projects_dir: str = "orchestrator/projects"):
        self.db = db or Database()
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def build_project(self, project_id: str) -> Dict:
        """
        Собирает проект: собирает все артефакты в ZIP
        
        Returns:
            Dict с путём к ZIP-файлу
        """
        project = self.db.get_project(project_id)
        if not project:
            return {'error': 'Проект не найден'}
        
        # Проверяем статус
        if project.status != ProjectStatus.COMPLETED:
            return {'error': f'Проект не завершён. Статус: {project.status.value}'}
        
        # Создаём папку проекта
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        # Очищаем старые файлы
        for item in project_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        
        # Получаем все артефакты
        artifacts = self.db.get_project_artifacts(project_id)
        
        if not artifacts:
            return {'error': 'Нет артефактов для сборки'}
        
        # Создаём структуру папок
        for artifact in artifacts:
            file_path = project_dir / artifact['file_name']
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Сохраняем контент
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(artifact['content'])
        
        # Создаём README если нет
        readme_path = project_dir / "README.md"
        if not readme_path.exists():
            self._create_readme(project, readme_path, artifacts)
        
        # Создаём ZIP-архив
        zip_path = self.projects_dir / f"{project_id}.zip"
        self._create_zip(project_dir, zip_path)
        
        # Обновляем проект
        with self.db:
            cursor = self.db._get_connection().cursor()
            cursor.execute(
                'UPDATE projects SET output_zip = ? WHERE id = ?',
                (str(zip_path), project_id)
            )
            cursor.connection.commit()
        
        return {
            'success': True,
            'project_id': project_id,
            'project_name': project.name,
            'zip_path': str(zip_path),
            'files_count': len(artifacts),
            'download_url': f'/api/projects/{project_id}/download'
        }
    
    def _create_readme(self, project, readme_path: Path, artifacts: List[Dict]):
        """Создаёт README.md для проекта"""
        readme_content = f"""# {project.name}

## Описание
{project.description}

## Техническое задание
{project.tz_text}

## Структура проекта
"""
        
        # Группируем файлы по папкам
        files_by_type = {}
        for art in artifacts:
            ext = art['file_name'].split('.')[-1] if '.' in art['file_name'] else 'other'
            if ext not in files_by_type:
                files_by_type[ext] = []
            files_by_type[ext].append(art['file_name'])
        
        for ext, files in sorted(files_by_type.items()):
            readme_content += f"\n### .{ext} файлы\n"
            for f in sorted(files):
                readme_content += f"- `{f}`\n"
        
        readme_content += f"""

## Установка и запуск

```bash
# Разархивировать
unzip {project.id}.zip

# Перейти в папку
cd {project.id}

# Установить зависимости (если есть requirements.txt или package.json)
pip install -r requirements.txt
# или
npm install

# Запустить
```

## Создано
Дата: {project.created_at}
Система: AI Правительство 🤖🏛️
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def _create_zip(self, source_dir: Path, zip_path: Path):
        """Создаёт ZIP-архив"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
    
    def deploy_to_hosting(self, project_id: str, hosting_config: Dict) -> Dict:
        """
        Деплоит проект на хостинг (Reg.ru или другой)
        
        Args:
            hosting_config: {
                'type': 'ftp' | 'ssh' | 'local',
                'host': '...',
                'username': '...',
                'password': '...',
                'remote_path': '...'
            }
        """
        project = self.db.get_project(project_id)
        if not project:
            return {'error': 'Проект не найден'}
        
        # Проверяем что проект собран
        zip_path = self.projects_dir / f"{project_id}.zip"
        if not zip_path.exists():
            # Собираем
            result = self.build_project(project_id)
            if 'error' in result:
                return result
        
        # Деплой через SSH (для Reg.ru VPS)
        if hosting_config.get('type') == 'ssh':
            return self._deploy_ssh(project_id, hosting_config)
        
        # Деплой через FTP
        elif hosting_config.get('type') == 'ftp':
            return self._deploy_ftp(project_id, hosting_config)
        
        # Локальный деплой (для теста)
        elif hosting_config.get('type') == 'local':
            return self._deploy_local(project_id, hosting_config)
        
        else:
            return {'error': 'Неизвестный тип хостинга'}
    
    def _deploy_ssh(self, project_id: str, config: Dict) -> Dict:
        """Деплой через SSH/SCP"""
        import subprocess
        
        zip_path = self.projects_dir / f"{project_id}.zip"
        remote_path = config.get('remote_path', '/var/www/html')
        
        try:
            # Копируем ZIP на сервер
            scp_cmd = [
                'scp', '-o', 'StrictHostKeyChecking=no',
                str(zip_path),
                f"{config['username']}@{config['host']}:{remote_path}/"
            ]
            
            result = subprocess.run(scp_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {'error': f'SCP ошибка: {result.stderr}'}
            
            # Распаковываем на сервере
            ssh_cmd = [
                'ssh', '-o', 'StrictHostKeyChecking=no',
                f"{config['username']}@{config['host']}",
                f"cd {remote_path} && unzip -o {project_id}.zip && rm {project_id}.zip"
            ]
            
            result = subprocess.run(ssh_cmd, capture_output=True, text=True)
            
            return {
                'success': True,
                'message': f'✅ Проект {project_id} задеплоен на {config["host"]}',
                'url': f"http://{config.get('domain', config['host'])}"
            }
            
        except Exception as e:
            return {'error': f'Ошибка деплоя: {str(e)}'}
    
    def _deploy_ftp(self, project_id: str, config: Dict) -> Dict:
        """Деплой через FTP"""
        from ftplib import FTP
        
        try:
            ftp = FTP(config['host'])
            ftp.login(config['username'], config['password'])
            
            # Переходим в целевую папку
            if config.get('remote_path'):
                ftp.cwd(config['remote_path'])
            
            # Загружаем файлы
            project_dir = self.projects_dir / project_id
            for file_path in project_dir.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(project_dir)
                    
                    # Создаём папки если нужно
                    parent = relative_path.parent
                    if str(parent) != '.':
                        try:
                            ftp.mkd(str(parent))
                        except:
                            pass
                        ftp.cwd(str(parent))
                    
                    # Загружаем файл
                    with open(file_path, 'rb') as f:
                        ftp.storbinary(f'STOR {relative_path.name}', f)
                    
                    # Возвращаемся в корень
                    if str(parent) != '.':
                        ftp.cwd('..' * len(parent.parts))
            
            ftp.quit()
            
            return {
                'success': True,
                'message': f'✅ Проект {project_id} задеплоен по FTP',
                'url': f"http://{config.get('domain', config['host'])}"
            }
            
        except Exception as e:
            return {'error': f'FTP ошибка: {str(e)}'}
    
    def _deploy_local(self, project_id: str, config: Dict) -> Dict:
        """Локальный деплой (для теста)"""
        target_dir = Path(config.get('remote_path', '/tmp/deploy'))
        target_dir.mkdir(parents=True, exist_ok=True)
        
        project_dir = self.projects_dir / project_id
        
        # Копируем файлы
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(project_dir)
                target_file = target_dir / relative_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, target_file)
        
        return {
            'success': True,
            'message': f'✅ Проект скопирован в {target_dir}',
            'path': str(target_dir)
        }
    
    def list_builds(self) -> List[Dict]:
        """Список собранных проектов"""
        builds = []
        
        for zip_file in self.projects_dir.glob('*.zip'):
            project_id = zip_file.stem
            stat = zip_file.stat()
            
            builds.append({
                'project_id': project_id,
                'file_name': zip_file.name,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'download_url': f'/api/projects/{project_id}/download'
            })
        
        return sorted(builds, key=lambda x: x['created'], reverse=True)
