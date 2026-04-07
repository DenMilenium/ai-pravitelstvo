"""
🚀 AutoDeploy Agent - Автоматический деплой проектов
Поддерживает: VPS (SSH), GitHub Pages, Vercel, Netlify
"""
import subprocess
import os
import json
import tempfile
import shutil
from pathlib import Path


class AutoDeployer:
    """Автоматический деплойер проектов"""
    
    DEPLOY_TARGETS = {
        'vps': 'VPS через SSH',
        'github-pages': 'GitHub Pages',
        'vercel': 'Vercel',
        'netlify': 'Netlify',
        'surge': 'Surge.sh',
        'firebase': 'Firebase Hosting'
    }
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.config_file = self.project_path / '.deploy.json'
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Загрузка конфигурации деплоя"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """Сохранение конфигурации"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def detect_project_type(self) -> str:
        """Определение типа проекта"""
        files = list(self.project_path.iterdir())
        
        if (self.project_path / 'package.json').exists():
            with open(self.project_path / 'package.json') as f:
                pkg = json.load(f)
                deps = pkg.get('dependencies', {})
                
                if 'next' in deps:
                    return 'nextjs'
                if 'react' in deps:
                    return 'react'
                if 'vue' in deps:
                    return 'vue'
                if 'nuxt' in deps:
                    return 'nuxt'
                return 'nodejs'
        
        if (self.project_path / 'requirements.txt').exists():
            return 'python'
        
        if (self.project_path / 'Cargo.toml').exists():
            return 'rust'
        
        if (self.project_path / 'go.mod').exists():
            return 'go'
        
        return 'static'
    
    def build_project(self) -> dict:
        """Сборка проекта"""
        project_type = self.detect_project_type()
        build_commands = {
            'react': ['npm', 'install', '&&', 'npm', 'run', 'build'],
            'nextjs': ['npm', 'install', '&&', 'npm', 'run', 'build'],
            'vue': ['npm', 'install', '&&', 'npm', 'run', 'build'],
            'nuxt': ['npm', 'install', '&&', 'npm', 'run', 'generate'],
            'nodejs': ['npm', 'install'],
            'static': []
        }
        
        commands = build_commands.get(project_type, [])
        
        if not commands:
            return {'success': True, 'message': 'Статический проект - сборка не требуется'}
        
        try:
            result = subprocess.run(
                ' '.join(commands),
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': '✅ Сборка завершена',
                    'output': result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': f'Ошибка сборки: {result.stderr[-500:]}'
                }
        
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': '⏱️ Таймаут сборки (5 минут)'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def deploy_to_vps(self, config: dict) -> dict:
        """Деплой на VPS через SSH"""
        host = config.get('host')
        user = config.get('user', 'root')
        path = config.get('path', '/var/www/app')
        key_file = config.get('key_file', '~/.ssh/id_rsa')
        
        if not host:
            return {'success': False, 'error': 'Не указан хост VPS'}
        
        try:
            # Создаем архив
            archive_path = tempfile.mktemp(suffix='.tar.gz')
            
            # Определяем что деплоить (dist, build или всё)
            deploy_dir = self.project_path
            for d in ['dist', 'build', 'out', '_site']:
                if (self.project_path / d).exists():
                    deploy_dir = self.project_path / d
                    break
            
            # Архивируем
            shutil.make_archive(archive_path.replace('.tar.gz', ''), 'gztar', deploy_dir)
            
            # Копируем на сервер
            scp_cmd = f'scp -i {key_file} -o StrictHostKeyChecking=no {archive_path} {user}@{host}:/tmp/'
            subprocess.run(scp_cmd, shell=True, check=True)
            
            # Распаковываем на сервере
            ssh_cmd = f'''
                ssh -i {key_file} -o StrictHostKeyChecking=no {user}@{host} '
                    mkdir -p {path} && \
                    tar -xzf /tmp/{os.path.basename(archive_path)} -C {path} && \
                    rm /tmp/{os.path.basename(archive_path)} && \
                    echo "✅ Деплой завершён на {host}"
                '
            '''
            result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
            
            # Удаляем временный архив
            os.unlink(archive_path)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': f'✅ Деплой на {host} успешен',
                    'url': f'http://{host}'
                }
            else:
                return {'success': False, 'error': result.stderr}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def deploy_to_github_pages(self, config: dict) -> dict:
        """Деплой на GitHub Pages"""
        repo = config.get('repo')
        branch = config.get('branch', 'gh-pages')
        
        if not repo:
            return {'success': False, 'error': 'Не указан репозиторий'}
        
        try:
            # Создаем временную директорию
            with tempfile.TemporaryDirectory() as tmpdir:
                # Клонируем repo
                clone_cmd = f'git clone --single-branch --branch {branch} {repo} {tmpdir}/gh-pages 2>&1 || git clone {repo} {tmpdir}/gh-pages'
                subprocess.run(clone_cmd, shell=True, check=True, cwd=self.project_path)
                
                # Копируем файлы
                deploy_dir = self.project_path
                for d in ['dist', 'build', 'out', '_site']:
                    if (self.project_path / d).exists():
                        deploy_dir = self.project_path / d
                        break
                
                # Очищаем и копируем
                gh_pages_dir = Path(tmpdir) / 'gh-pages'
                for item in gh_pages_dir.iterdir():
                    if item.name != '.git':
                        if item.is_file():
                            item.unlink()
                        else:
                            shutil.rmtree(item)
                
                for item in deploy_dir.iterdir():
                    if item.is_file():
                        shutil.copy2(item, gh_pages_dir)
                    else:
                        shutil.copytree(item, gh_pages_dir / item.name)
                
                # Коммит и пуш
                subprocess.run('git add .', shell=True, check=True, cwd=gh_pages_dir)
                subprocess.run('git commit -m "Deploy from AI Dashboard" || true', 
                             shell=True, check=True, cwd=gh_pages_dir)
                subprocess.run('git push origin HEAD', shell=True, check=True, cwd=gh_pages_dir)
                
                return {
                    'success': True,
                    'message': '✅ Деплой на GitHub Pages успешен',
                    'url': f'https://{repo.split(":")[-1].replace(".git", "").replace("github.com/", "")}.github.io'
                }
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def deploy_to_vercel(self, config: dict) -> dict:
        """Деплой на Vercel"""
        try:
            # Проверяем наличие vercel CLI
            result = subprocess.run(['which', 'vercel'], capture_output=True)
            if result.returncode != 0:
                return {
                    'success': False, 
                    'error': 'Vercel CLI не установлен. Установите: npm i -g vercel'
                }
            
            # Деплой
            cmd = ['vercel', '--yes', '--prod']
            if config.get('token'):
                cmd.extend(['--token', config['token']])
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Извлекаем URL из вывода
                url = None
                for line in result.stdout.split('\n'):
                    if 'https://' in line and 'vercel.app' in line:
                        url = line.strip().split()[-1]
                        break
                
                return {
                    'success': True,
                    'message': '✅ Деплой на Vercel успешен',
                    'url': url or 'См. вывод команды'
                }
            else:
                return {'success': False, 'error': result.stderr}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def deploy(self, target: str, config: dict = None) -> dict:
        """Главный метод деплоя"""
        if target not in self.DEPLOY_TARGETS:
            return {'success': False, 'error': f'Неизвестный таргет: {target}'}
        
        # Сначала собираем
        build_result = self.build_project()
        if not build_result['success']:
            return build_result
        
        # Затем деплоим
        deploy_methods = {
            'vps': self.deploy_to_vps,
            'github-pages': self.deploy_to_github_pages,
            'vercel': self.deploy_to_vercel,
            'netlify': lambda c: {'success': False, 'error': 'Netlify пока не реализован'},
            'surge': lambda c: {'success': False, 'error': 'Surge пока не реализован'},
            'firebase': lambda c: {'success': False, 'error': 'Firebase пока не реализован'}
        }
        
        return deploy_methods[target](config or {})
    
    def get_deploy_status(self) -> dict:
        """Получение статуса последнего деплоя"""
        status_file = self.project_path / '.deploy-status.json'
        if status_file.exists():
            with open(status_file) as f:
                return json.load(f)
        return {'status': 'unknown', 'last_deploy': None}


# CLI интерфейс
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Правительство - AutoDeploy')
    parser.add_argument('project_path', help='Путь к проекту')
    parser.add_argument('--target', '-t', required=True, 
                       choices=list(AutoDeployer.DEPLOY_TARGETS.keys()),
                       help='Цель деплоя')
    parser.add_argument('--config', '-c', help='JSON конфигурация')
    
    args = parser.parse_args()
    
    deployer = AutoDeployer(args.project_path)
    config = json.loads(args.config) if args.config else {}
    
    result = deployer.deploy(args.target, config)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    exit(0 if result['success'] else 1)
