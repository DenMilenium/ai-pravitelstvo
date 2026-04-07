#!/usr/bin/env python3
"""
🔐 Проверка и исправление входа в Dashboard
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'dashboard.db'

def check_and_fix_login():
    """Проверяет и исправляет возможные проблемы с логином"""
    
    print("🔍 Проверка базы данных...")
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # 1. Проверяем существование таблицы users
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not c.fetchone():
        print("❌ Таблица users не существует! Создаём...")
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        conn.commit()
        print("✅ Таблица users создана")
    
    # 2. Проверяем структуру таблицы (убираем role если есть)
    c.execute("PRAGMA table_info(users)")
    columns = c.fetchall()
    print(f"📋 Колонки в таблице users: {[col[1] for col in columns]}")
    
    # 3. Проверяем наличие пользователя admin
    c.execute("SELECT id, username, password_hash FROM users WHERE username = 'admin'")
    user = c.fetchone()
    
    if user:
        print(f"👤 Пользователь admin найден (ID: {user[0]})")
        
        # Проверяем пароль
        test_password = 'admin123'
        if check_password_hash(user[2], test_password):
            print("✅ Пароль admin123 работает!")
        else:
            print("⚠️ Пароль не совпадает! Сбрасываю на admin123...")
            new_hash = generate_password_hash(test_password)
            c.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (new_hash,))
            conn.commit()
            print("✅ Пароль сброшен на admin123")
    else:
        print("⚠️ Пользователь admin не найден! Создаём...")
        password_hash = generate_password_hash('admin123')
        c.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            ('admin', password_hash, 'admin@example.com')
        )
        conn.commit()
        print("✅ Пользователь admin создан с паролем admin123")
    
    # 4. Проверяем что пользователь точно есть
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    final_check = c.fetchone()
    
    if final_check:
        print(f"\n✅ ГОТОВО! Можно входить:")
        print(f"   Логин: admin")
        print(f"   Пароль: admin123")
    else:
        print("\n❌ ОШИБКА: Пользователь не создан!")
    
    conn.close()

if __name__ == "__main__":
    os.chdir('/var/www/ai-pravitelstvo/dashboard')
    check_and_fix_login()
