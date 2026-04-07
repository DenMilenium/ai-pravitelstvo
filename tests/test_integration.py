"""
🧪 Интеграционные тесты для AI Правительства
Тестируем полный цикл: создание проекта → задачи → выполнение → ZIP
"""
import unittest
import sys
import os
import tempfile
import zipfile

# Добавляем путь к orchestrator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.core.task_executor import TaskExecutor
from orchestrator.core.database import Database, Task, TaskStatus


class TestAgentExecution(unittest.TestCase):
    """Тесты выполнения задач агентами"""
    
    @classmethod
    def setUpClass(cls):
        """Инициализация перед всеми тестами"""
        cls.executor = TaskExecutor()
        print(f"\\n🚀 Загружено {len(cls.executor.executors)} агентов")
    
    def test_react_agent_creates_dashboard(self):
        """Тест: ReactAgent создает Dashboard"""
        print("\\n🧪 Тест ReactAgent...")
        
        # Создаем фейковую задачу
        class FakeTask:
            agent_type = 'react'
            title = 'Test Dashboard'
            description = 'Create admin dashboard'
        
        task = FakeTask()
        
        # Находим агента
        agent = None
        for a in self.executor.executors:
            if a.can_execute(task):
                agent = a
                break
        
        self.assertIsNotNone(agent, "ReactAgent не найден")
        print(f"✅ Найден агент: {agent.NAME}")
        
        # Выполняем
        result = agent.execute(task)
        
        self.assertTrue(result['success'])
        self.assertIn('artifacts', result)
        self.assertIn('Dashboard.js', result['artifacts'])
        print(f"✅ Создано файлов: {len(result['artifacts'])}")
    
    def test_django_agent_creates_api(self):
        """Тест: DjangoAgent создает API"""
        print("\\n🧪 Тест DjangoAgent...")
        
        class FakeTask:
            agent_type = 'django'
            title = 'Test API'
            description = 'Create blog API'
        
        task = FakeTask()
        
        agent = None
        for a in self.executor.executors:
            if a.can_execute(task):
                agent = a
                break
        
        self.assertIsNotNone(agent)
        result = agent.execute(task)
        
        self.assertTrue(result['success'])
        self.assertIn('views.py', result['artifacts'])
        print(f"✅ Django API создан, файлов: {len(result['artifacts'])}")
    
    def test_docker_agent_creates_files(self):
        """Тест: DockerAgent создает Dockerfile"""
        print("\\n🧪 Тест DockerAgent...")
        
        class FakeTask:
            agent_type = 'docker'
            title = 'Test Docker'
            description = 'Containerize app'
        
        task = FakeTask()
        
        agent = None
        for a in self.executor.executors:
            if a.can_execute(task):
                agent = a
                break
        
        self.assertIsNotNone(agent)
        result = agent.execute(task)
        
        self.assertTrue(result['success'])
        self.assertIn('Dockerfile', result['artifacts'])
        print(f"✅ Docker файлы созданы")
    
    def test_all_agents_have_required_attributes(self):
        """Тест: Все агенты имеют нужные атрибуты"""
        print("\\n🧪 Проверка атрибутов агентов...")
        
        required_attrs = ['NAME', 'EMOJI', 'AGENT_TYPE']
        
        for agent in self.executor.executors:
            for attr in required_attrs:
                self.assertTrue(
                    hasattr(agent, attr),
                    f"{agent.__class__.__name__} не имеет {attr}"
                )
        
        print(f"✅ Все {len(self.executor.executors)} агентов имеют нужные атрибуты")


class TestAgentsByCategory(unittest.TestCase):
    """Тесты агентов по категориям"""
    
    def setUp(self):
        self.executor = TaskExecutor()
    
    def test_frontend_agents(self):
        """Тест Frontend агентов"""
        print("\\n🧪 Тест Frontend агентов...")
        
        frontend_types = ['react', 'vue', 'angular', 'svelte', 'nextjs']
        
        for agent_type in frontend_types:
            class FakeTask:
                pass
            FakeTask.agent_type = agent_type
            
            found = any(a.can_execute(FakeTask()) for a in self.executor.executors)
            self.assertTrue(found, f"Агент {agent_type} не найден")
        
        print(f"✅ Все {len(frontend_types)} Frontend агента работают")
    
    def test_backend_agents(self):
        """Тест Backend агентов"""
        print("\\n🧪 Тест Backend агентов...")
        
        backend_types = ['django', 'fastapi', 'nodejs', 'go', 'laravel']
        
        for agent_type in backend_types:
            class FakeTask:
                pass
            FakeTask.agent_type = agent_type
            
            found = any(a.can_execute(FakeTask()) for a in self.executor.executors)
            self.assertTrue(found, f"Агент {agent_type} не найден")
        
        print(f"✅ Все {len(backend_types)} Backend агента работают")
    
    def test_cloud_agents(self):
        """Тест Cloud агентов"""
        print("\\n🧪 Тест Cloud агентов...")
        
        cloud_types = ['aws', 'docker', 'kubernetes', 'terraform']
        
        for agent_type in cloud_types:
            class FakeTask:
                pass
            FakeTask.agent_type = agent_type
            
            found = any(a.can_execute(FakeTask()) for a in self.executor.executors)
            self.assertTrue(found, f"Агент {agent_type} не найден")
        
        print(f"✅ Все {len(cloud_types)} Cloud агента работают")


class TestZIPCreation(unittest.TestCase):
    """Тест создания ZIP архивов"""
    
    def test_can_create_zip_from_artifacts(self):
        """Тест: Можно создать ZIP из артефактов"""
        print("\\n🧪 Тест создания ZIP...")
        
        # Создаем тестовые артефакты
        artifacts = {
            'index.html': '<html><body>Hello</body></html>',
            'style.css': 'body { color: blue; }',
            'app.js': 'console.log("Hello");'
        }
        
        # Создаем ZIP в памяти
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zf:
                for filename, content in artifacts.items():
                    zf.writestr(filename, content)
            
            # Проверяем ZIP
            with zipfile.ZipFile(tmp.name, 'r') as zf:
                self.assertEqual(len(zf.namelist()), 3)
                self.assertIn('index.html', zf.namelist())
        
        # Удаляем временный файл
        os.unlink(tmp.name)
        
        print("✅ ZIP создан успешно")


def run_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("🧪 ИНТЕГРАЦИОННЫЕ ТЕСТЫ AI ПРАВИТЕЛЬСТВА")
    print("=" * 60)
    
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    suite.addTests(loader.loadTestsFromTestCase(TestAgentExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentsByCategory))
    suite.addTests(loader.loadTestsFromTestCase(TestZIPCreation))
    
    # Запускаем
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим итог
    print("\\n" + "=" * 60)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    print(f"✅ Пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Ошибок: {len(result.errors)}")
    print(f"❌ Провалов: {len(result.failures)}")
    
    if result.wasSuccessful():
        print("\\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        return 0
    else:
        print("\\n⚠️ ЕСТЬ ПРОБЛЕМЫ!")
        return 1


if __name__ == '__main__':
    exit(run_tests())
