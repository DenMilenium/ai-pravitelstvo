#!/usr/bin/env python3
"""
🖥️ PyQt-Agent
Агент-разработчик GUI-приложений на PyQt6

Умеет:
- Создавать окна и виджеты
- Работать с потоками
- Стилизовать интерфейс
- Сохранять настройки

Запуск:
    python pyqt_agent.py "Создай окно чата с темной темой"
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Component:
    """UI компонент"""
    name: str
    code: str
    imports: List[str]


class PyQtAgent:
    """
    🤖 PyQt-Agent
    
    Специализация: Десктопные GUI-приложения
    Стек: Python, PyQt6/PySide6
    """
    
    NAME = "PyQt-Agent"
    ROLE = "Разработчик GUI-приложений"
    EXPERTISE = ["PyQt6", "PySide6", "QThread", "Styling", "Layouts"]
    
    def __init__(self):
        self.templates = {
            "main_window": self._template_main_window,
            "chat_widget": self._template_chat_widget,
            "settings_dialog": self._template_settings,
            "file_browser": self._template_file_browser,
        }
        self.styles = {
            "dark": self._style_dark,
            "light": self._style_light,
            "modern": self._style_modern,
        }
    
    def process_request(self, request: str) -> str:
        """
        Обработка запроса и генерация кода
        
        Args:
            request: Описание задачи на естественном языке
            
        Returns:
            Сгенерированный Python код
        """
        request_lower = request.lower()
        
        # Определяем тип компонента
        if "чат" in request_lower or "chat" in request_lower:
            component = self.generate_chat_widget()
        elif "настройк" in request_lower or "settings" in request_lower:
            component = self.generate_settings_dialog()
        elif "файл" in request_lower or "file" in request_lower:
            component = self.generate_file_browser()
        elif "главное окно" in request_lower or "main window" in request_lower:
            component = self.generate_main_window()
        else:
            component = self.generate_main_window()
        
        # Определяем тему
        theme = "dark"
        if "светл" in request_lower or "light" in request_lower:
            theme = "light"
        elif "модерн" in request_lower or "modern" in request_lower:
            theme = "modern"
        
        # Собираем полный код
        full_code = self._assemble_code(component, theme)
        return full_code
    
    def generate_chat_widget(self) -> Component:
        """Генерация виджета чата"""
        name = "ChatWidget"
        imports = [
            "from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, ",
            "    QTextEdit, QLineEdit, QPushButton, QListWidget, QLabel)",
            "from PyQt6.QtCore import Qt, pyqtSignal, QThread",
            "from PyQt6.QtGui import QFont",
        ]
        
        code = '''
class ChatWidget(QWidget):
    """Виджет чата с поддержкой отправки сообщений"""
    
    message_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Заголовок
        self.header = QLabel("💬 Чат")
        self.header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(self.header)
        
        # Область сообщений
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.chat_display)
        
        # Область ввода
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите сообщение...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("➤ Отправить")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
    
    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.add_message("Вы", text, is_user=True)
            self.message_sent.emit(text)
            self.input_field.clear()
    
    def add_message(self, sender: str, text: str, is_user: bool = False):
        """Добавить сообщение в чат"""
        if is_user:
            html = f\'\'\'<div style="margin: 10px 0; text-align: right;">
                <div style="background: #007ACC; color: white; padding: 10px; 
                           border-radius: 15px 15px 0 15px; display: inline-block; 
                           max-width: 80%; text-align: left;">
                    <b>👤 {sender}:</b><br>{text}
                </div>
            </div>\'\'\'
        else:
            html = f\'\'\'<div style="margin: 10px 0;">
                <div style="background: #2D2D2D; color: #E0E0E0; padding: 10px; 
                           border-radius: 15px 15px 15px 0; display: inline-block; 
                           max-width: 80%;">
                    <b>🤖 {sender}:</b><br>{text}
                </div>
            </div>\'\'\'
        
        self.chat_display.insertHtml(html)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
            }
            QTextEdit {
                background-color: #252526;
                border: 1px solid #3E3E42;
                border-radius: 8px;
                padding: 10px;
            }
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #3E3E42;
                border-radius: 20px;
                padding: 10px 15px;
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0098FF;
            }
        """)
'''
        return Component(name=name, code=code, imports=imports)
    
    def generate_settings_dialog(self) -> Component:
        """Генерация диалога настроек"""
        name = "SettingsDialog"
        imports = [
            "from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, ",
            "    QTabWidget, QWidget, QLabel, QLineEdit, QComboBox, ",
            "    QCheckBox, QPushButton, QSpinBox)",
            "from PyQt6.QtCore import Qt",
        ]
        
        code = '''
class SettingsDialog(QDialog):
    """Диалог настроек с вкладками"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Настройки")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Табы
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_general_tab(), "📋 Общие")
        self.tabs.addTab(self._create_appearance_tab(), "🎨 Внешний вид")
        self.tabs.addTab(self._create_advanced_tab(), "🔧 Дополнительно")
        layout.addWidget(self.tabs)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.save_btn = QPushButton("💾 Сохранить")
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("❌ Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def _create_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        layout.addWidget(QLabel("📝 Имя пользователя:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        
        layout.addWidget(QLabel("🌐 Язык:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "English", "Deutsch"])
        layout.addWidget(self.language_combo)
        
        self.autostart_check = QCheckBox("🚀 Автозапуск")
        layout.addWidget(self.autostart_check)
        
        layout.addStretch()
        return tab
    
    def _create_appearance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        layout.addWidget(QLabel("🎨 Тема:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Тёмная", "Светлая", "Системная"])
        layout.addWidget(self.theme_combo)
        
        layout.addWidget(QLabel("🔤 Размер шрифта:"))
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(11)
        layout.addWidget(self.font_size)
        
        layout.addStretch()
        return tab
    
    def _create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.debug_check = QCheckBox("🐻 Режим отладки")
        layout.addWidget(self.debug_check)
        
        self.telemetry_check = QCheckBox("📊 Отправлять статистику")
        self.telemetry_check.setChecked(True)
        layout.addWidget(self.telemetry_check)
        
        layout.addStretch()
        return tab
    
    def save_settings(self):
        """Сохранение настроек"""
        settings = {
            "username": self.username_input.text(),
            "language": self.language_combo.currentText(),
            "autostart": self.autostart_check.isChecked(),
            "theme": self.theme_combo.currentText(),
            "font_size": self.font_size.value(),
            "debug": self.debug_check.isChecked(),
            "telemetry": self.telemetry_check.isChecked(),
        }
        print(f"Сохранённые настройки: {settings}")
        self.accept()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
                color: #E0E0E0;
            }
            QTabWidget::pane {
                background-color: #252526;
                border: 1px solid #3E3E42;
            }
            QTabBar::tab {
                background-color: #2D2D30;
                color: #E0E0E0;
                padding: 10px 20px;
                border: none;
            }
            QTabBar::tab:selected {
                background-color: #007ACC;
            }
        """)
'''
        return Component(name=name, code=code, imports=imports)
    
    def generate_main_window(self) -> Component:
        """Генерация главного окна"""
        name = "MainWindow"
        imports = [
            "import sys",
            "from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, ",
            "    QVBoxLayout, QMenuBar, QStatusBar, QMessageBox)",
            "from PyQt6.QtCore import Qt",
            "from PyQt6.QtGui import QAction, QKeySequence",
        ]
        
        code = '''
class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 AI Приложение")
        self.setMinimumSize(900, 700)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Здесь добавляй свои виджеты
        # layout.addWidget(MyWidget())
        
        # Меню
        self._setup_menu()
        
        # Статус бар
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("🟢 Готов к работе")
    
    def _setup_menu(self):
        menubar = self.menuBar()
        
        # Файл
        file_menu = menubar.addMenu("📁 Файл")
        
        exit_action = QAction("❌ Выход", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Помощь
        help_menu = menubar.addMenu("❓ Помощь")
        
        about_action = QAction("ℹ️ О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_about(self):
        QMessageBox.about(self, "О программе", """
            <h1>🤖 AI Приложение</h1>
            <p>Версия: 1.0.0</p>
            <p>Создано с помощью PyQt-Agent</p>
        """)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QMenuBar {
                background-color: #2D2D30;
                color: #E0E0E0;
                padding: 5px;
            }
            QMenuBar::item:selected {
                background-color: #007ACC;
            }
            QStatusBar {
                background-color: #007ACC;
                color: white;
                padding: 5px;
            }
        """)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
'''
        return Component(name=name, code=code, imports=imports)
    
    def _style_dark(self) -> str:
        return """
            QWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                font-family: 'Segoe UI', sans-serif;
            }
        """
    
    def _style_light(self) -> str:
        return """
            QWidget {
                background-color: #FFFFFF;
                color: #333333;
                font-family: 'Segoe UI', sans-serif;
            }
        """
    
    def _style_modern(self) -> str:
        return """
            QWidget {
                background-color: #0F0F0F;
                color: #00FF88;
                font-family: 'Consolas', monospace;
            }
        """
    
    def _assemble_code(self, component: Component, theme: str) -> str:
        """Сборка полного кода"""
        imports = "\n".join(component.imports)
        
        code = f"""#!/usr/bin/env python3
\"\"\"
🖥️ Сгенерировано PyQt-Agent
Компонент: {component.name}
Тема: {theme}
\"\"\"

{imports}


{component.code}


# Дополнительные стили
GLOBAL_STYLE = \"\"\"
{self.styles.get(theme, self._style_dark)()}
\"\"\"

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_STYLE)
    
    # Тестовый запуск
    window = {component.name}()
    window.show()
    
    sys.exit(app.exec())
"""
        return code


def main():
    parser = argparse.ArgumentParser(description="🖥️ PyQt-Agent — Генератор GUI")
    parser.add_argument("request", nargs="?", help="Описание компонента")
    parser.add_argument("--output", "-o", help="Файл для сохранения")
    parser.add_argument("--theme", "-t", default="dark", 
                       choices=["dark", "light", "modern"],
                       help="Тема оформления")
    
    args = parser.parse_args()
    
    agent = PyQtAgent()
    
    if args.request:
        print(f"🤖 {agent.NAME} обрабатывает запрос: {args.request}")
        code = agent.process_request(args.request)
        
        if args.output:
            Path(args.output).write_text(code, encoding="utf-8")
            print(f"✅ Код сохранён в: {args.output}")
        else:
            print("\n" + "="*50)
            print("СГЕНЕРИРОВАННЫЙ КОД:")
            print("="*50)
            print(code)
    else:
        print(f"🤖 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"Экспертиза: {', '.join(agent.EXPERTISE)}")
        print("\nПримеры использования:")
        print('  python pyqt_agent.py "Создай чат"')
        print('  python pyqt_agent.py "Настройки с вкладками" -o settings.py')


if __name__ == "__main__":
    main()
