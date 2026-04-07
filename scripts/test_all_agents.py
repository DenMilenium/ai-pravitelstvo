#!/usr/bin/env python3
"""
🧪 Agents Productivity Test - Массовое тестирование всех агентов
Тестирует всех 106 агентов и выводит статистику продуктивности
"""
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict
import statistics

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.core.task_executor import TaskExecutor
from orchestrator.core.database import Task, TaskStatus


@dataclass
class AgentTestResult:
    """Результат тестирования агента"""
    agent_type: str
    agent_name: str
    emoji: str
    success: bool
    execution_time_ms: float
    artifacts_count: int
    error_message: str = None
    artifact_types: List[str] = None


class AgentsProductivityTester:
    """Тестер продуктивности агентов"""
    
    def __init__(self):
        self.executor = TaskExecutor()
        self.results: List[AgentTestResult] = []
        self.start_time = None
        self.end_time = None
    
    def create_fake_task(self, agent_type: str) -> Task:
        """Создание фейковой задачи для агента"""
        return Task(
            id=f"test-{agent_type}-{int(time.time())}",
            project_id="test-project",
            title=f"Test task for {agent_type}",
            description=f"Testing {agent_type} agent functionality",
            agent_type=agent_type,
            status=TaskStatus.PENDING,
            priority=1,
            dependencies=[],
            artifacts={},
            created_at=datetime.now().isoformat()
        )
    
    def test_agent(self, executor) -> AgentTestResult:
        """Тестирование одного агента"""
        agent_type = executor.AGENT_TYPE
        agent_name = getattr(executor, 'NAME', agent_type)
        emoji = getattr(executor, 'EMOJI', '🤖')
        
        # Создаём задачу
        task = self.create_fake_task(agent_type)
        
        # Проверяем может ли агент выполнить
        if not executor.can_execute(task):
            return AgentTestResult(
                agent_type=agent_type,
                agent_name=agent_name,
                emoji=emoji,
                success=False,
                execution_time_ms=0,
                artifacts_count=0,
                error_message="Agent cannot execute this task type"
            )
        
        # Замеряем время
        start = time.time()
        
        try:
            result = executor.execute(task)
            execution_time = (time.time() - start) * 1000  # мс
            
            artifacts = result.get('artifacts', {})
            artifact_types = [f.split('.')[-1] if '.' in f else 'unknown' 
                           for f in artifacts.keys()]
            
            return AgentTestResult(
                agent_type=agent_type,
                agent_name=agent_name,
                emoji=emoji,
                success=result.get('success', False),
                execution_time_ms=round(execution_time, 2),
                artifacts_count=len(artifacts),
                error_message=result.get('message') if not result.get('success') else None,
                artifact_types=list(set(artifact_types))
            )
            
        except Exception as e:
            execution_time = (time.time() - start) * 1000
            return AgentTestResult(
                agent_type=agent_type,
                agent_name=agent_name,
                emoji=emoji,
                success=False,
                execution_time_ms=round(execution_time, 2),
                artifacts_count=0,
                error_message=str(e)
            )
    
    def run_all_tests(self) -> Dict:
        """Запуск тестирования всех агентов"""
        print("🧪 AGENTS PRODUCTIVITY TEST")
        print("=" * 80)
        print(f"Testing {len(self.executor.executors)} agents...\n")
        
        self.start_time = time.time()
        
        for i, executor in enumerate(self.executor.executors, 1):
            agent_name = getattr(executor, 'NAME', executor.AGENT_TYPE)
            emoji = getattr(executor, 'EMOJI', '🤖')
            
            print(f"[{i:3d}/{len(self.executor.executors)}] Testing {emoji} {agent_name}...", end=' ')
            
            result = self.test_agent(executor)
            self.results.append(result)
            
            status = "✅" if result.success else "❌"
            print(f"{status} {result.execution_time_ms:.0f}ms | {result.artifacts_count} files")
        
        self.end_time = time.time()
        
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Генерация отчёта о продуктивности"""
        total = len(self.results)
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        # Статистика по времени
        exec_times = [r.execution_time_ms for r in successful]
        avg_time = statistics.mean(exec_times) if exec_times else 0
        median_time = statistics.median(exec_times) if exec_times else 0
        min_time = min(exec_times) if exec_times else 0
        max_time = max(exec_times) if exec_times else 0
        
        # Статистика по артефактам
        artifacts_counts = [r.artifacts_count for r in successful]
        avg_artifacts = statistics.mean(artifacts_counts) if artifacts_counts else 0
        total_artifacts = sum(artifacts_counts)
        
        # Топ быстрых/медленных
        by_speed = sorted(successful, key=lambda x: x.execution_time_ms)
        fastest = by_speed[:5]
        slowest = by_speed[-5:]
        
        # Топ продуктивных (по количеству артефактов)
        by_productivity = sorted(successful, key=lambda x: x.artifacts_count, reverse=True)
        most_productive = by_productivity[:5]
        
        # По категориям
        categories = {}
        category_map = {
            'react': 'Frontend', 'vue': 'Frontend', 'angular': 'Frontend', 'svelte': 'Frontend',
            'nextjs': 'Frontend', 'nuxt': 'Frontend', 'remix': 'Frontend', 'gatsby': 'Frontend',
            'hugo': 'Frontend', 'jekyll': 'Frontend', 'astro': 'Frontend', 'wordpress': 'Frontend',
            'shopify': 'Frontend', 'preact': 'Frontend', 'alpine': 'Frontend', 'lit': 'Frontend',
            'stimulus': 'Frontend', 'solid': 'Frontend', 'qwik': 'Frontend',
            
            'django': 'Backend', 'fastapi': 'Backend', 'nodejs': 'Backend', 'go': 'Backend',
            'laravel': 'Backend', 'ruby': 'Backend', 'java': 'Backend', 'csharp': 'Backend',
            'rust': 'Backend',
            
            'flutter': 'Mobile', 'ios': 'Mobile', 'android': 'Mobile', 'react-native': 'Mobile', 'pwa': 'Mobile',
            
            'docker': 'Cloud', 'kubernetes': 'Cloud', 'aws': 'Cloud', 'azure': 'Cloud', 'gcp': 'Cloud',
            'terraform': 'Cloud', 'github-actions': 'Cloud', 'gitlab-ci': 'Cloud', 'jenkins': 'Cloud',
            'nginx': 'Cloud', 'apache': 'Cloud', 'cdn': 'Cloud', 'ssl': 'Cloud',
            
            'postgres': 'Database', 'mongodb': 'Database', 'redis': 'Database', 'mysql': 'Database',
            'elasticsearch': 'Database', 'graphql': 'Database', 'kafka': 'Database', 'rabbitmq': 'Database',
            
            'prometheus': 'Monitoring', 'grafana': 'Monitoring', 'sentry': 'Monitoring', 'logrocket': 'Monitoring',
            'testing': 'Testing', 'jest': 'Testing', 'cypress': 'Testing', 'playwright': 'Testing',
            'chromatic': 'Testing',
        }
        
        for r in successful:
            cat = category_map.get(r.agent_type, 'Other')
            if cat not in categories:
                categories[cat] = {'count': 0, 'avg_time': [], 'total_artifacts': 0}
            categories[cat]['count'] += 1
            categories[cat]['avg_time'].append(r.execution_time_ms)
            categories[cat]['total_artifacts'] += r.artifacts_count
        
        # Форматируем категории
        category_stats = []
        for cat, data in sorted(categories.items(), key=lambda x: -x[1]['count']):
            category_stats.append({
                'category': cat,
                'agents_count': data['count'],
                'avg_time_ms': round(statistics.mean(data['avg_time']), 2),
                'total_artifacts': data['total_artifacts']
            })
        
        report = {
            'test_date': datetime.now().isoformat(),
            'duration_seconds': round(self.end_time - self.start_time, 2),
            'summary': {
                'total_agents': total,
                'successful': len(successful),
                'failed': len(failed),
                'success_rate': round(len(successful) / total * 100, 2)
            },
            'performance': {
                'avg_execution_time_ms': round(avg_time, 2),
                'median_execution_time_ms': round(median_time, 2),
                'min_time_ms': round(min_time, 2),
                'max_time_ms': round(max_time, 2),
                'avg_artifacts_per_agent': round(avg_artifacts, 2),
                'total_artifacts_generated': total_artifacts
            },
            'top_performers': {
                'fastest': [
                    {'name': r.agent_name, 'emoji': r.emoji, 'time_ms': r.execution_time_ms}
                    for r in fastest
                ],
                'slowest': [
                    {'name': r.agent_name, 'emoji': r.emoji, 'time_ms': r.execution_time_ms}
                    for r in slowest
                ],
                'most_productive': [
                    {'name': r.agent_name, 'emoji': r.emoji, 'artifacts': r.artifacts_count}
                    for r in most_productive
                ]
            },
            'category_stats': category_stats,
            'failed_agents': [
                {'name': r.agent_name, 'emoji': r.emoji, 'error': r.error_message}
                for r in failed
            ],
            'detailed_results': [asdict(r) for r in self.results]
        }
        
        return report


def print_report(report: Dict):
    """Красивый вывод отчёта"""
    print("\n" + "=" * 80)
    print("📊 PRODUCTIVITY REPORT")
    print("=" * 80)
    
    print(f"\n🗓️  Test Date: {report['test_date']}")
    print(f"⏱️  Total Duration: {report['duration_seconds']:.2f} seconds")
    
    # Summary
    print("\n" + "-" * 80)
    print("📈 SUMMARY")
    print("-" * 80)
    s = report['summary']
    print(f"   Total Agents:    {s['total_agents']}")
    print(f"   ✅ Successful:    {s['successful']}")
    print(f"   ❌ Failed:        {s['failed']}")
    print(f"   📊 Success Rate:  {s['success_rate']}%")
    
    # Performance
    print("\n" + "-" * 80)
    print("⚡ PERFORMANCE METRICS")
    print("-" * 80)
    p = report['performance']
    print(f"   Avg Execution Time:    {p['avg_execution_time_ms']:.2f} ms")
    print(f"   Median Execution Time: {p['median_execution_time_ms']:.2f} ms")
    print(f"   Min Time:              {p['min_time_ms']:.2f} ms")
    print(f"   Max Time:              {p['max_time_ms']:.2f} ms")
    print(f"   Avg Artifacts/Agent:   {p['avg_artifacts_per_agent']:.1f}")
    print(f"   Total Artifacts:       {p['total_artifacts_generated']}")
    
    # Top Performers
    print("\n" + "-" * 80)
    print("🏆 TOP PERFORMERS")
    print("-" * 80)
    
    print("\n   ⚡ Fastest Agents:")
    for i, agent in enumerate(report['top_performers']['fastest'], 1):
        print(f"      {i}. {agent['emoji']} {agent['name']}: {agent['time_ms']:.2f} ms")
    
    print("\n   📦 Most Productive:")
    for i, agent in enumerate(report['top_performers']['most_productive'], 1):
        print(f"      {i}. {agent['emoji']} {agent['name']}: {agent['artifacts']} files")
    
    print("\n   🐌 Slowest Agents:")
    for i, agent in enumerate(report['top_performers']['slowest'], 1):
        print(f"      {i}. {agent['emoji']} {agent['name']}: {agent['time_ms']:.2f} ms")
    
    # Categories
    print("\n" + "-" * 80)
    print("📊 PERFORMANCE BY CATEGORY")
    print("-" * 80)
    for cat in report['category_stats']:
        print(f"   {cat['category']:15s} | Agents: {cat['agents_count']:2d} | "
              f"Avg: {cat['avg_time_ms']:7.2f} ms | Files: {cat['total_artifacts']:3d}")
    
    # Failed
    if report['failed_agents']:
        print("\n" + "-" * 80)
        print("❌ FAILED AGENTS")
        print("-" * 80)
        for agent in report['failed_agents']:
            error = agent['error'][:60] + '...' if len(agent['error']) > 60 else agent['error']
            print(f"   {agent['emoji']} {agent['name']}: {error}")
    
    print("\n" + "=" * 80)
    
    # Productivity Score
    success_rate = report['summary']['success_rate']
    avg_time = report['performance']['avg_execution_time_ms']
    
    if success_rate >= 95 and avg_time < 100:
        grade = "🏆 EXCELLENT"
    elif success_rate >= 90 and avg_time < 200:
        grade = "✅ GOOD"
    elif success_rate >= 80:
        grade = "⚠️  ACCEPTABLE"
    else:
        grade = "❌ NEEDS IMPROVEMENT"
    
    print(f"\n🎯 OVERALL PRODUCTIVITY GRADE: {grade}")
    print("=" * 80)


def save_report(report: Dict, filename: str = None):
    """Сохранение отчёта в JSON"""
    if not filename:
        filename = f"agents_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    filepath = Path(__file__).parent.parent / 'reports' / filename
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Report saved to: {filepath}")


if __name__ == '__main__':
    tester = AgentsProductivityTester()
    report = tester.run_all_tests()
    
    print_report(report)
    save_report(report)
    
    # Exit code based on success rate
    if report['summary']['success_rate'] < 80:
        print("\n⚠️  Warning: Success rate below 80%!")
        sys.exit(1)
    else:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
