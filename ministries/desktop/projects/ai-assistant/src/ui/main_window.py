"""
Главное окно приложения (PyQt6)
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QSplitter, QListWidget, QStatusBar, QMenuBar,
    QMenu, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QKeySequence

from ..core.assistant import AIAssistant


class AIWorker(QThread):
    """Поток для неблокирующей генерации ответов"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, assistant: AIAssistant, user_input: str):
        super().__init__()
        self.assistant = assistant
        self.user_input = user_input
    
    def run(self):
        try:
            response = self.assistant.process(self.user_input)
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    """Главное окно AI-Помощника"""
    
    def __init__(self, config_path: str, parent=None):
        super().__init__(parent)
        self.config_path = config_path
        self.assistant = AIAssistant(config_path)
        
        self.setWindowTitle("🤖 AI-Помощник")
        self.setMinimumSize(900, 700)
        
        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
        
        # Загружаем модель в фоне
        self._load_model_async()
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Сплиттер для сайдбара и чата
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # === Сайдбар ===
        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок сайдбара
        sidebar_title = QLabel("💬 История")
        sidebar_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        sidebar_layout.addWidget(sidebar_title)
        
        # Список чатов
        self.chat_list = QListWidget()
        self.chat_list.addItem("Текущий чат")
        sidebar_layout.addWidget(self.chat_list)
        
        # Кнопки управления
        new_chat_btn = QPushButton("➕ Новый чат")
        new_chat_btn.clicked.connect(self._new_chat)
        sidebar_layout.addWidget(new_chat_btn)
        
        clear_btn = QPushButton("🗑️ Очистить")
        clear_btn.clicked.connect(self._clear_chat)
        sidebar_layout.addWidget(clear_btn)
        
        sidebar_layout.addStretch()
        
        # === Область чата ===
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок чата
        chat_header = QLabel("🤖 AI-Помощник")
        chat_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        chat_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chat_layout.addWidget(chat_header)
        
        # Область сообщений
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 11))
        chat_layout.addWidget(self.chat_display)
        
        # Область ввода
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите сообщение...")
        self.input_field.setFont(QFont("Segoe UI", 11))
        self.input_field.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.input_field)
        
        send_btn = QPushButton("➤ Отправить")
        send_btn.setShortcut(QKeySequence("Ctrl+Return"))
        send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(send_btn)
        
        chat_layout.addLayout(input_layout)
        
        # Добавляем в сплиттер
        splitter.addWidget(sidebar)
        splitter.addWidget(chat_widget)
        splitter.setSizes([200, 700])
    
    def _setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()
        
        # Файл
        file_menu = menubar.addMenu("Файл")
        
        new_chat_action = QAction("Новый чат", self)
        new_chat_action.setShortcut(QKeySequence("Ctrl+N"))
        new_chat_action.triggered.connect(self._new_chat)
        file_menu.addAction(new_chat_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Инструменты
        tools_menu = menubar.addMenu("Инструменты")
        
        settings_action = QAction("Настройки", self)
        settings_action.triggered.connect(self._show_settings)
        tools_menu.addAction(settings_action)
        
        # Помощь
        help_menu = menubar.addMenu("Помощь")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_statusbar(self):
        """Настройка статус-бара"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("🟡 Загрузка модели...")
    
    def _load_model_async(self):
        """Асинхронная загрузка модели"""
        class LoadWorker(QThread):
            finished = pyqtSignal(bool)
            
            def __init__(self, assistant):
                super().__init__()
                self.assistant = assistant
            
            def run(self):
                success = self.assistant.load_model()
                self.finished.emit(success)
        
        self.load_worker = LoadWorker(self.assistant)
        self.load_worker.finished.connect(self._on_model_loaded)
        self.load_worker.start()
    
    def _on_model_loaded(self, success: bool):
        """Callback после загрузки модели"""
        if success:
            self.statusbar.showMessage("🟢 Модель загружена | Готов к работе")
            self._add_system_message("🤖 Привет! Я ваш AI-Помощник. Чем могу помочь?")
        else:
            self.statusbar.showMessage("🔴 Ошибка загрузки модели")
            self._add_system_message("❌ Не удалось загрузить модель. Проверьте конфигурацию.")
    
    def _send_message(self):
        """Отправка сообщения"""
        text = self.input_field.text().strip()
        if not text:
            return
        
        # Добавляем сообщение пользователя
        self._add_user_message(text)
        self.input_field.clear()
        
        # Показываем индикатор загрузки
        self._add_system_message("⏳ Думаю...")
        self.statusbar.showMessage("🟡 Генерация ответа...")
        
        # Запускаем генерацию в отдельном потоке
        self.ai_worker = AIWorker(self.assistant, text)
        self.ai_worker.response_ready.connect(self._on_response_ready)
        self.ai_worker.error_occurred.connect(self._on_error)
        self.ai_worker.start()
    
    def _on_response_ready(self, response: str):
        """Обработка готового ответа"""
        # Удаляем индикатор загрузки
        self._remove_last_message()
        
        # Добавляем ответ
        self._add_ai_message(response)
        self.statusbar.showMessage("🟢 Готов к работе")
    
    def _on_error(self, error: str):
        """Обработка ошибки"""
        self._remove_last_message()
        self._add_system_message(f"❌ Ошибка: {error}")
        self.statusbar.showMessage("🔴 Произошла ошибка")
    
    def _add_user_message(self, text: str):
        """Добавить сообщение пользователя"""
        html = f'''
        <div style="margin: 10px 0; text-align: right;">
            <div style="background: #007ACC; color: white; padding: 10px; 
                       border-radius: 15px 15px 0 15px; display: inline-block; 
                       max-width: 80%; text-align: left;">
                <b>👤 Вы:</b><br>{text}
            </div>
        </div>
        '''
        self.chat_display.insertHtml(html)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def _add_ai_message(self, text: str):
        """Добавить сообщение AI"""
        html = f'''
        <div style="margin: 10px 0;">
            <div style="background: #2D2D2D; color: #E0E0E0; padding: 10px; 
                       border-radius: 15px 15px 15px 0; display: inline-block; 
                       max-width: 80%;">
                <b>🤖 AI:</b><br>{text}
            </div>
        </div>
        '''
        self.chat_display.insertHtml(html)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def _add_system_message(self, text: str):
        """Добавить системное сообщение"""
        html = f'''
        <div style="margin: 10px 0; text-align: center;">
            <span style="color: #888; font-size: 12px;">{text}</span>
        </div>
        '''
        self.chat_display.insertHtml(html)
    
    def _remove_last_message(self):
        """Удалить последнее сообщение (для убирания индикатора загрузки)"""
        # Упрощённая реализация - в продакшене нужно более точное управление
        pass
    
    def _new_chat(self):
        """Создать новый чат"""
        self.chat_display.clear()
        self.assistant.memory.clear()
        self._add_system_message("🆕 Новый чат создан")
        self._add_system_message("🤖 Привет! Чем могу помочь?")
    
    def _clear_chat(self):
        """Очистить текущий чат"""
        self.chat_display.clear()
        self.assistant.memory.clear()
    
    def _show_settings(self):
        """Показать настройки"""
        QMessageBox.information(
            self, 
            "Настройки",
            "Настройки будут здесь..."
        )
    
    def _show_about(self):
        """Показать информацию о программе"""
        QMessageBox.about(
            self,
            "О программе",
            """<h1>🤖 AI-Помощник</h1>
            <p>Версия: 0.1.0</p>
            <p>Министерство Десктопных Приложений<br>
            AI Правительство © 2024</p>
            <p>Локальный AI-ассистент с приватностью данных.</p>
            """
        )
