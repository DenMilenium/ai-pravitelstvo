#!/usr/bin/env python3
"""
AI-Помощник - Локальный AI-ассистент для ПК
Министерство Десктопных Приложений, AI Правительство
"""

import sys
import argparse
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.assistant import AIAssistant
from ui.main_window import MainWindow

__version__ = "0.1.0"
__author__ = "AI Правительство"


def main():
    parser = argparse.ArgumentParser(
        description="AI-Помощник - Ваш локальный AI-ассистент"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/local.yaml",
        help="Путь к файлу конфигурации"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Запуск без GUI (CLI режим)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Режим отладки"
    )
    
    args = parser.parse_args()
    
    print(f"🤖 AI-Помощник v{__version__}")
    print(f"🏛️  Министерство Десктопных Приложений")
    print("-" * 40)
    
    if args.headless:
        run_cli(args)
    else:
        run_gui(args)


def run_cli(args):
    """CLI режим"""
    print("💬 CLI режим (введите 'exit' для выхода)")
    
    assistant = AIAssistant(config_path=args.config)
    assistant.load_model()
    
    while True:
        try:
            user_input = input("\n👤 Вы: ").strip()
            
            if user_input.lower() in ["exit", "quit", "выход"]:
                print("👋 До свидания!")
                break
            
            if not user_input:
                continue
            
            # Обработка запроса
            response = assistant.process(user_input)
            print(f"🤖 AI: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            if args.debug:
                raise
            print(f"❌ Ошибка: {e}")


def run_gui(args):
    """GUI режим"""
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("❌ PyQt6 не установлен. Установите: pip install PyQt6")
        print("🔄 Переключение в CLI режим...")
        run_cli(args)
        return
    
    app = QApplication(sys.argv)
    app.setApplicationName("AI-Помощник")
    app.setApplicationVersion(__version__)
    
    # Загружаем стиль
    app.setStyle("Fusion")
    
    # Создаём главное окно
    window = MainWindow(config_path=args.config)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
