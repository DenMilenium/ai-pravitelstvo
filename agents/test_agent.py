#!/usr/bin/env python3
"""
🧪 Test-Agent
Агент-тестировщик QA

Создаёт:
- Тест-планы
- Тест-кейсы
- Автотесты (pytest, jest)
- Отчёты о тестировании
"""

import argparse
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class TestCase:
    id: str
    title: str
    steps: List[str]
    expected: str
    priority: str


class TestAgent:
    """
    🧪 Test-Agent
    
    Специализация: QA и тестирование
    Инструменты: pytest, jest, selenium, playwright
    """
    
    NAME = "🧪 Test-Agent"
    ROLE = "QA Engineer"
    EXPERTISE = ["Manual Testing", "Test Cases", "Bug Reports", "Test Plans", "Acceptance Criteria"]
    
    def __init__(self):
        self.test_types = {
            "unit": "Unit Tests",
            "integration": "Integration Tests",
            "e2e": "End-to-End Tests",
            "api": "API Tests",
            "ui": "UI Tests",
            "security": "Security Tests",
            "performance": "Performance Tests",
        }
    
    def process_request(self, request: str, test_type: str = "unit") -> Dict[str, str]:
        """Обработка запроса на тестирование"""
        request_lower = request.lower()
        files = {}
        
        if "тест-план" in request_lower or "test plan" in request_lower:
            files = self._generate_test_plan(request)
        elif "тест-кейс" in request_lower or "test case" in request_lower:
            files = self._generate_test_cases(request)
        elif "api" in request_lower:
            files = self._generate_api_tests(request)
        elif "ui" in request_lower or "interface" in request_lower:
            files = self._generate_ui_tests(request)
        elif "python" in request_lower or "pytest" in request_lower:
            files = self._generate_python_tests(request)
        elif "javascript" in request_lower or "jest" in request_lower:
            files = self._generate_js_tests(request)
        else:
            files = self._generate_test_cases(request)
        
        return files
    
    def _generate_test_plan(self, feature: str) -> Dict[str, str]:
        """Генерация тест-плана"""
        files = {}
        
        files["TEST_PLAN.md"] = f"""# 📋 Тест-план: {feature}

**Создано:** Test-Agent  
**Дата:** $(date)  
**Версия:** 1.0

---

## 1. Общая информация

### Цель
Провести полное тестирование функционала: **{feature}**

### Объём тестирования
- Функциональное тестирование
- API тестирование
- UI/UX тестирование
- Кроссбраузерное тестирование

### Критерии входа
- [ ] Код разработан и задеплоен на тестовое окружение
- [ ] Документация обновлена
- [ ] Smoke tests пройдены

### Критерии выхода
- [ ] Все critical/high тест-кейсы пройдены
- [ ] Нет открытых critical/high багов
- [ ] Отчёт о тестировании одобрен

---

## 2. Тестовые сценарии

### 2.1 Позитивные сценарии
| ID | Сценарий | Приоритет | Статус |
|----|----------|-----------|--------|
| TC-001 | Базовый функционал | Critical | ⬜ |
| TC-002 | Альтернативный путь | High | ⬜ |
| TC-003 | Граничные значения | Medium | ⬜ |

### 2.2 Негативные сценарии
| ID | Сценарий | Приоритет | Статус |
|----|----------|-----------|--------|
| TC-004 | Невалидные данные | High | ⬜ |
| TC-005 | Неполные данные | Medium | ⬜ |
| TC-006 | Несанкционированный доступ | Critical | ⬜ |

---

## 3. Типы тестирования

### 3.1 Unit Tests
- **Инструмент:** pytest / jest
- **Покрытие:** минимум 80%
- **Ответственный:** Разработчик

### 3.2 Integration Tests
- **Инструмент:** pytest + requests / jest + supertest
- **Сценарии:** API endpoints, Database integration

### 3.3 E2E Tests
- **Инструмент:** Playwright / Selenium
- **Сценарии:** Пользовательские сценарии

### 3.4 Performance Tests
- **Инструмент:** k6 / JMeter
- **Метрики:** Response time < 200ms, Throughput > 1000 RPS

---

## 4. Расписание

| Фаза | Длительность | Начало | Конец |
|------|--------------|--------|-------|
| Подготовка | 1 день | День 1 | День 1 |
| Тестирование | 3 дня | День 2 | День 4 |
| Регресс | 1 день | День 5 | День 5 |
| Отчёт | 1 день | День 6 | День 6 |

---

## 5. Риски

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| Задержка разработки | Средняя | Высокое | Резервное время |
| Нестабильное окружение | Низкая | Среднее | Автоматизация деплоя |

---

**Подписи:**
- QA Lead: _______________
- Product Manager: _______________
"""
        return files
    
    def _generate_test_cases(self, feature: str) -> Dict[str, str]:
        """Генерация тест-кейсов"""
        files = {}
        
        files["TEST_CASES.md"] = f"""# 🧪 Тест-кейсы: {feature}

**Создано:** Test-Agent

---

## TC-001: Базовый сценарий

**Приоритет:** Critical  
**Предусловия:** Пользователь авторизован

### Шаги:
1. Открыть страницу {feature}
2. Ввести валидные данные
3. Нажать кнопку "Отправить"

### Ожидаемый результат:
- ✅ Данные сохранены
- ✅ Показано подтверждение
- ✅ Произошёл редирект

---

## TC-002: Невалидные данные

**Приоритет:** High  
**Предусловия:** Пользователь авторизован

### Шаги:
1. Открыть страницу {feature}
2. Ввести невалидные данные (пустые поля)
3. Нажать кнопку "Отправить"

### Ожидаемый результат:
- ✅ Показана ошибка валидации
- ✅ Данные не сохранены
- ✅ Фокус на первом ошибочном поле

---

## TC-003: Граничные значения

**Приоритет:** Medium

### Шаги:
1. Ввести максимально допустимое количество символов
2. Отправить форму

### Ожидаемый результат:
- ✅ Данные приняты
- ✅ Нет ошибок

---

## TC-004: XSS попытка

**Приоритет:** Critical

### Шаги:
1. Ввести: `<script>alert('xss')</script>`
2. Отправить форму

### Ожидаемый результат:
- ✅ Скрипт не выполнен
- ✅ Текст экранирован
- ✅ Нет alert

---

## TC-005: SQL Injection

**Приоритет:** Critical

### Шаги:
1. Ввести: `' OR '1'='1`
2. Отправить форму

### Ожидаемый результат:
- ✅ Запрос безопасно обработан
- ✅ Нет утечки данных

---

## TC-006: Перегрузка (Stress)

**Приоритет:** Medium

### Шаги:
1. Отправить 1000 запросов одновременно

### Ожидаемый результат:
- ✅ Сервер отвечает
- ✅ Время ответа < 2s
- ✅ Нет ошибок 500
"""
        return files
    
    def _generate_python_tests(self, feature: str) -> Dict[str, str]:
        """Генерация Python тестов"""
        files = {}
        
        files["test_feature.py"] = f'''"""
🧪 Автотесты для: {feature}
Создано: Test-Agent
"""

import pytest
from unittest.mock import Mock, patch


class Test{feature.replace(" ", "")}:
    """Тесты функционала: {feature}"""
    
    def test_create_success(self):
        """TC-001: Успешное создание"""
        # Arrange
        data = {{"name": "Test", "value": 123}}
        
        # Act
        result = create_item(data)
        
        # Assert
        assert result["success"] is True
        assert result["id"] is not None
    
    def test_create_invalid_data(self):
        """TC-002: Невалидные данные"""
        # Arrange
        data = {{"name": "", "value": -1}}
        
        # Act
        result = create_item(data)
        
        # Assert
        assert result["success"] is False
        assert "errors" in result
    
    def test_create_duplicate(self):
        """TC-003: Дубликат"""
        # Arrange
        data = {{"name": "Existing", "value": 123}}
        
        # Act & Assert
        with pytest.raises(DuplicateError):
            create_item(data)
    
    def test_get_by_id_success(self):
        """TC-004: Получение по ID"""
        # Arrange
        item_id = "123"
        
        # Act
        result = get_item(item_id)
        
        # Assert
        assert result["id"] == item_id
    
    def test_get_by_id_not_found(self):
        """TC-005: Не найдено"""
        # Arrange
        item_id = "nonexistent"
        
        # Act & Assert
        with pytest.raises(NotFoundError):
            get_item(item_id)
    
    def test_update_success(self):
        """TC-006: Успешное обновление"""
        # Arrange
        item_id = "123"
        updates = {{"name": "Updated"}}
        
        # Act
        result = update_item(item_id, updates)
        
        # Assert
        assert result["name"] == "Updated"
    
    def test_delete_success(self):
        """TC-007: Успешное удаление"""
        # Arrange
        item_id = "123"
        
        # Act
        result = delete_item(item_id)
        
        # Assert
        assert result["deleted"] is True
    
    def test_list_pagination(self):
        """TC-008: Пагинация"""
        # Act
        result = list_items(page=1, limit=10)
        
        # Assert
        assert len(result["items"]) <= 10
        assert result["page"] == 1
    
    def test_search_functionality(self):
        """TC-009: Поиск"""
        # Arrange
        query = "test"
        
        # Act
        result = search_items(query)
        
        # Assert
        assert all(query in item["name"].lower() for item in result)
    
    def test_unauthorized_access(self):
        """TC-010: Неавторизованный доступ"""
        # Arrange
        with patch('auth.check', return_value=False):
            # Act & Assert
            with pytest.raises(UnauthorizedError):
                create_item({{}})
    
    @pytest.mark.parametrize("input_value,expected", [
        ("valid@email.com", True),
        ("invalid-email", False),
        ("", False),
        ("@nodomain.com", False),
    ])
    def test_email_validation(self, input_value, expected):
        """TC-011: Валидация email"""
        result = validate_email(input_value)
        assert result == expected


class TestPerformance:
    """Нагрузочные тесты"""
    
    @pytest.mark.slow
    def test_response_time(self):
        """TC-012: Время ответа"""
        import time
        
        start = time.time()
        get_item("123")
        elapsed = time.time() - start
        
        assert elapsed < 0.2  # 200ms
'''
        
        files["conftest.py"] = '''"""
🔧 Конфигурация pytest
"""

import pytest


@pytest.fixture
def client():
    """Фикстура тестового клиента"""
    from app import create_app
    app = create_app(testing=True)
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Фикстура авторизационных заголовков"""
    return {{"Authorization": "Bearer test-token"}}


@pytest.fixture(autouse=True)
def clean_database():
    """Очистка БД перед каждым тестом"""
    # cleanup code
    yield
    # cleanup code
'''
        return files
    
    def _generate_js_tests(self, feature: str) -> Dict[str, str]:
        """Генерация JavaScript тестов"""
        files = {}
        
        files[f"{feature.replace(' ', '_').lower()}.test.js"] = f'''/**
 * 🧪 Автотесты для: {feature}
 * Создано: Test-Agent
 */

import {{ render, screen, fireEvent, waitFor }} from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Mock API
jest.mock('../api', () => ({{
  createItem: jest.fn(),
  getItem: jest.fn(),
  updateItem: jest.fn(),
  deleteItem: jest.fn(),
}}));

describe('{feature}', () => {{
  beforeEach(() => {{
    jest.clearAllMocks();
  }});

  describe('TC-001: Создание', () => {{
    it('успешно создаёт новый элемент', async () => {{
      // Arrange
      const mockData = {{ name: 'Test', value: 123 }};
      createItem.mockResolvedValue({{ id: '123', ...mockData }});
      
      render(<{feature.replace(' ', '')}Form />);
      
      // Act
      await userEvent.type(screen.getByLabelText(/name/i), 'Test');
      await userEvent.click(screen.getByRole('button', {{ name: /создать/i }}));
      
      // Assert
      await waitFor(() => {{
        expect(screen.getByText(/успешно/i)).toBeInTheDocument();
      }});
    }});

    it('показывает ошибку при невалидных данных', async () => {{
      // Arrange
      render(<{feature.replace(' ', '')}Form />);
      
      // Act
      await userEvent.click(screen.getByRole('button', {{ name: /создать/i }}));
      
      // Assert
      expect(screen.getByText(/обязательное поле/i)).toBeInTheDocument();
    }});
  }});

  describe('TC-002: Чтение', () => {{
    it('отображает данные', async () => {{
      // Arrange
      const mockItem = {{ id: '123', name: 'Test' }};
      getItem.mockResolvedValue(mockItem);
      
      render(<{feature.replace(' ', '')}View id="123" />);
      
      // Assert
      await waitFor(() => {{
        expect(screen.getByText('Test')).toBeInTheDocument();
      }});
    }});

    it('показывает "не найдено"', async () => {{
      // Arrange
      getItem.mockRejectedValue(new Error('Not found'));
      
      render(<{feature.replace(' ', '')}View id="999" />);
      
      // Assert
      await waitFor(() => {{
        expect(screen.getByText(/не найдено/i)).toBeInTheDocument();
      }});
    }});
  }});

  describe('TC-003: Обновление', () => {{
    it('успешно обновляет', async () => {{
      // Arrange
      updateItem.mockResolvedValue({{ id: '123', name: 'Updated' }});
      
      render(<{feature.replace(' ', '')}Edit id="123" />);
      
      // Act
      await userEvent.clear(screen.getByLabelText(/name/i));
      await userEvent.type(screen.getByLabelText(/name/i), 'Updated');
      await userEvent.click(screen.getByRole('button', {{ name: /сохранить/i }}));
      
      // Assert
      await waitFor(() => {{
        expect(updateItem).toHaveBeenCalledWith('123', {{ name: 'Updated' }});
      }});
    }});
  }});

  describe('TC-004: Удаление', () => {{
    it('успешно удаляет после подтверждения', async () => {{
      // Arrange
      window.confirm = jest.fn(() => true);
      deleteItem.mockResolvedValue({{ deleted: true }});
      
      render(<{feature.replace(' ', '')}Item id="123" />);
      
      // Act
      await userEvent.click(screen.getByRole('button', {{ name: /удалить/i }}));
      
      // Assert
      expect(deleteItem).toHaveBeenCalledWith('123');
    }});

    it('отменяет при отрицательном ответе', async () => {{
      // Arrange
      window.confirm = jest.fn(() => false);
      
      render(<{feature.replace(' ', '')}Item id="123" />);
      
      // Act
      await userEvent.click(screen.getByRole('button', {{ name: /удалить/i }}));
      
      // Assert
      expect(deleteItem).not.toHaveBeenCalled();
    }});
  }});

  describe('Accessibility', () => {{
    it('поддерживает навигацию с клавиатуры', async () => {{
      render(<{feature.replace(' ', '')}Form />);
      
      // Act
      await userEvent.tab();
      await userEvent.tab();
      
      // Assert
      expect(screen.getByRole('button', {{ name: /создать/i }})).toHaveFocus();
    }});

    it('имеет корректные ARIA-метки', () => {{
      render(<{feature.replace(' ', '')}Form />);
      
      expect(screen.getByRole('form')).toBeInTheDocument();
      expect(screen.getByRole('button')).toBeInTheDocument();
    }});
  }});
}});
'''
        return files
    
    def _generate_api_tests(self, feature: str) -> Dict[str, str]:
        """Генерация API тестов"""
        return self._generate_python_tests(feature)
    
    def _generate_ui_tests(self, feature: str) -> Dict[str, str]:
        """Генерация UI/E2E тестов"""
        files = {}
        
        files["e2e.spec.js"] = f'''/**
 * 🎭 E2E тесты: {feature}
 * Создано: Test-Agent
 */

import {{ test, expect }} from '@playwright/test';

test.describe('{feature}', () => {{
  test.beforeEach(async ({{ page }}) => {{
    await page.goto('/{feature.lower().replace(" ", "-")}');
  }});

  test('TC-001: полный пользовательский сценарий', async ({{ page }}) => {{
    // Создание
    await page.fill('[name="title"]', 'Test Item');
    await page.fill('[name="description"]', 'Test Description');
    await page.click('button:has-text("Создать")');
    
    await expect(page.locator('.success-message')).toBeVisible();
    
    // Проверка в списке
    await expect(page.locator('text=Test Item')).toBeVisible();
    
    // Редактирование
    await page.click('text=Test Item');
    await page.fill('[name="title"]', 'Updated Item');
    await page.click('button:has-text("Сохранить")');
    
    await expect(page.locator('text=Updated Item')).toBeVisible();
    
    // Удаление
    await page.click('button:has-text("Удалить")');
    await page.click('button:has-text("Подтвердить")');
    
    await expect(page.locator('text=Updated Item')).not.toBeVisible();
  }});

  test('TC-002: мобильная адаптивность', async ({{ page }}) => {{
    await page.setViewportSize({{ width: 375, height: 667 }});
    
    await expect(page.locator('.mobile-menu')).toBeVisible();
  }});

  test('TC-003: тёмная тема', async ({{ page }}) => {{
    await page.click('[data-testid="theme-toggle"]');
    
    await expect(page.locator('html')).toHaveClass(/dark/);
  }});
}});
'''
        return files


def main():
    parser = argparse.ArgumentParser(description="🧪 Test-Agent — QA и тестирование")
    parser.add_argument("request", nargs="?", help="Что тестируем")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    parser.add_argument("--type", "-t", default="unit",
                       choices=["unit", "integration", "e2e", "api", "ui"],
                       help="Тип тестов")
    
    args = parser.parse_args()
    
    agent = TestAgent()
    
    if args.request:
        print(f"🧪 {agent.NAME} создаёт тесты для: {args.request}")
        print(f"Тип: {args.type}")
        print("-" * 50)
        
        files = agent.process_request(args.request, args.type)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
            
            print(f"\n📁 Сохранено в: {output_dir}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:800] + "..." if len(content) > 800 else content)
    else:
        print(f"🧪 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"Экспертиза: {', '.join(agent.EXPERTISE)}")
        print("\nПримеры:")
        print('  python test_agent.py "API авторизации" --type api')
        print('  python test_agent.py "Форма входа" --type e2e')
        print('  python test_agent.py "Тест-план для чата"')


if __name__ == "__main__":
    main()
