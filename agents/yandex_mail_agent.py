#!/usr/bin/env python3
"""
📧 YandexMail-Agent
Yandex Mail Integration Specialist

Интеграция с Яндекс Почтой для бизнеса.
SMTP, IMAP, Webhooks, автоответы, обратная связь.
"""

import argparse
from pathlib import Path
from typing import Dict


class YandexMailAgent:
    """
    📧 YandexMail-Agent
    
    Специализация: Yandex Mail Integration
    Задачи: SMTP/IMAP, формы обратной связи, автоответы
    """
    
    NAME = "📧 YandexMail-Agent"
    ROLE = "Yandex Mail Specialist"
    EXPERTISE = ["Yandex Mail", "SMTP", "IMAP", "Webhooks", "Auto-replies", "Contact Forms"]
    
    SMTP_HOST = "smtp.yandex.ru"
    SMTP_PORT = 465
    IMAP_HOST = "imap.yandex.ru"
    IMAP_PORT = 993
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["yandex-mail-config.py"] = self._generate_mail_config()
        files["contact-form-backend.js"] = self._generate_contact_form()
        files["auto-reply-setup.md"] = self._generate_auto_reply_guide()
        files["webhook-handler.py"] = self._generate_webhook_handler()
        files["mail-fetcher.py"] = self._generate_mail_fetcher()
        
        return files
    
    def _generate_mail_config(self) -> str:
        return '''"""
Yandex Mail Configuration
Настройка отправки и получения почты через Яндекс
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import os
from dataclasses import dataclass


@dataclass
class MailConfig:
    """Конфигурация почты Яндекс"""
    login: str  # Полный email вида user@yandex.ru
    password: str  # Пароль приложения (не основной!)
    smtp_host: str = "smtp.yandex.ru"
    smtp_port: int = 465
    imap_host: str = "imap.yandex.ru"
    imap_port: int = 993


class YandexMailClient:
    """Клиент для работы с Яндекс Почтой"""
    
    def __init__(self, config: MailConfig):
        self.config = config
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Отправить email через Яндекс SMTP
        
        Args:
            to: Получатель
            subject: Тема
            body: Текст письма
            html_body: HTML версия (опционально)
            cc: Копия
            bcc: Скрытая копия
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config.login
            msg['To'] = to
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Plain text версия
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # HTML версия (если есть)
            if html_body:
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Отправка через SMTP
            with smtplib.SMTP_SSL(
                self.config.smtp_host,
                self.config.smtp_port
            ) as server:
                server.login(self.config.login, self.config.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def fetch_unread(self, folder: str = "INBOX", limit: int = 10) -> List[Dict]:
        """
        Получить непрочитанные письма через IMAP
        
        Args:
            folder: Папка для проверки
            limit: Максимальное количество писем
            
        Returns:
            Список писем с полями: subject, from, date, body
        """
        emails = []
        
        try:
            mail = imaplib.IMAP4_SSL(
                self.config.imap_host,
                self.config.imap_port
            )
            mail.login(self.config.login, self.config.password)
            mail.select(folder)
            
            # Ищем непрочитанные
            _, search_data = mail.search(None, 'UNSEEN')
            
            email_ids = search_data[0].split()[-limit:]
            
            for e_id in email_ids:
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                # Извлекаем тело письма
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                else:
                    body = email_message.get_payload(decode=True).decode('utf-8')
                
                emails.append({
                    'id': e_id.decode(),
                    'subject': email_message['Subject'],
                    'from': email_message['From'],
                    'date': email_message['Date'],
                    'body': body[:500]  # Первые 500 символов
                })
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"Error fetching emails: {e}")
        
        return emails
    
    def send_auto_reply(self, to: str, template: str, **kwargs) -> bool:
        """
        Отправить автоответ
        
        Args:
            to: Получатель
            template: Название шаблона
            **kwargs: Переменные для шаблона
        """
        templates = {
            'support': {
                'subject': 'Спасибо за обращение!',
                'body': '''Здравствуйте!

Спасибо за ваше обращение. Мы получили ваше сообщение и ответим в течение 24 часов.

Ваше обращение: {message_preview}

--
С уважением,
Команда поддержки
'''
            },
            'order_confirmation': {
                'subject': 'Заказ #{order_id} принят!',
                'body': '''Спасибо за заказ!

Номер заказа: {order_id}
Сумма: {amount} ₽

Мы свяжемся с вами для подтверждения.

--
Магазин
'''
            },
            'vacation': {
                'subject': 'Автоответ: В отпуске',
                'body': '''Здравствуйте!

Я в отпуске с {start_date} по {end_date}.

По срочным вопросам обращайтесь: {backup_contact}

--
С уважением
'''
            }
        }
        
        if template not in templates:
            return False
        
        tmpl = templates[template]
        body = tmpl['body'].format(**kwargs)
        
        return self.send_email(to, tmpl['subject'], body)


# Пример использования
if __name__ == "__main__":
    config = MailConfig(
        login=os.getenv("YANDEX_EMAIL", "your@yandex.ru"),
        password=os.getenv("YANDEX_PASSWORD", "your_app_password")
    )
    
    client = YandexMailClient(config)
    
    # Отправка письма
    client.send_email(
        to="recipient@example.com",
        subject="Тестовое письмо",
        body="Привет! Это тест.",
        html_body="<h1>Привет!</h1><p>Это тест.</p>"
    )
    
    # Проверка непрочитанных
    unread = client.fetch_unread(limit=5)
    for email in unread:
        print(f"From: {email['from']}, Subject: {email['subject']}")
'''
    
    def _generate_contact_form(self) -> str:
        return '''const express = require('express');
const nodemailer = require('nodemailer');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');

/**
 * API для формы обратной связи
 * Отправляет письма через Яндекс SMTP
 */

const app = express();
app.use(express.json());

// Rate limiting - защита от спама
const contactLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 минут
  max: 5, // максимум 5 сообщений
  message: { 
    success: false, 
    error: 'Слишком много запросов. Попробуйте позже.' 
  }
});

// Настройка транспорта Яндекс
const createTransporter = () => {
  return nodemailer.createTransport({
    host: 'smtp.yandex.ru',
    port: 465,
    secure: true,
    auth: {
      user: process.env.YANDEX_EMAIL,
      pass: process.env.YANDEX_APP_PASSWORD
    }
  });
};

// Валидация формы
const validateContact = [
  body('name')
    .trim()
    .isLength({ min: 2, max: 100 })
    .withMessage('Имя должно быть от 2 до 100 символов'),
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Укажите корректный email'),
  body('subject')
    .trim()
    .isLength({ min: 5, max: 200 })
    .withMessage('Тема должна быть от 5 до 200 символов'),
  body('message')
    .trim()
    .isLength({ min: 10, max: 5000 })
    .withMessage('Сообщение должно быть от 10 до 5000 символов'),
  body('phone')
    .optional()
    .matches(/^\\+?[0-9\\s\\-\\(\\)]{10,20}$/)
    .withMessage('Укажите корректный телефон')
];

// API endpoint для формы обратной связи
app.post('/api/contact', contactLimiter, validateContact, async (req, res) => {
  try {
    // Проверка валидации
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const { name, email, subject, message, phone, company } = req.body;
    
    const transporter = createTransporter();
    
    // Письмо вам
    await transporter.sendMail({
      from: `"Форма обратной связи" <${process.env.YANDEX_EMAIL}>`,
      to: process.env.RECIPIENT_EMAIL || process.env.YANDEX_EMAIL,
      replyTo: email,
      subject: `[Сайт] ${subject}`,
      text: `
Новое сообщение с сайта:

Имя: ${name}
Email: ${email}
Телефон: ${phone || 'не указан'}
Компания: ${company || 'не указана'}

Тема: ${subject}

Сообщение:
${message}

---
IP: ${req.ip}
Время: ${new Date().toLocaleString('ru-RU')}
      `,
      html: `
        <h2>Новое сообщение с сайта</h2>
        <table style="border-collapse: collapse;">
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Имя:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${name}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Email:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${email}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Телефон:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${phone || 'не указан'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Компания:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${company || 'не указана'}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Тема:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">${subject}</td></tr>
        </table>
        <h3>Сообщение:</h3>
        <p style="white-space: pre-wrap;">${message}</p>
        <hr>
        <small>IP: ${req.ip} | ${new Date().toLocaleString('ru-RU')}</small>
      `
    });
    
    // Подтверждение отправителю
    await transporter.sendMail({
      from: `"Команда поддержки" <${process.env.YANDEX_EMAIL}>`,
      to: email,
      subject: 'Ваше сообщение получено',
      text: `
Здравствуйте, ${name}!

Мы получили ваше сообщение:
"${subject}"

Ответим вам в течение 24 часов.

--
С уважением,
Команда поддержки
      `,
      html: `
        <h2>Здравствуйте, ${name}!</h2>
        <p>Мы получили ваше сообщение:</p>
        <blockquote style="border-left: 3px solid #ccc; padding-left: 10px; color: #666;">
          ${subject}
        </blockquote>
        <p>Ответим вам в течение <strong>24 часов</strong>.</p>
        <hr>
        <small>С уважением, Команда поддержки</small>
      `
    });
    
    res.json({
      success: true,
      message: 'Сообщение успешно отправлено! Мы ответим вам в течение 24 часов.'
    });
    
  } catch (error) {
    console.error('Contact form error:', error);
    res.status(500).json({
      success: false,
      error: 'Произошла ошибка при отправке. Попробуйте позже.'
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'yandex-mail-api' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`📧 Yandex Mail API running on port ${PORT}`);
});

module.exports = app;
'''
    
    def _generate_auto_reply_guide(self) -> str:
        return '''# Настройка автоответов в Яндекс Почте

## 1. Получение пароля приложения

1. Войдите в Яндекс ID: https://id.yandex.ru
2. Перейдите в "Безопасность" → "Пароли приложений"
3. Создайте пароль для приложения "Почта (IMAP, POP3, SMTP)"
4. **Сохраните пароль** — он показывается только один раз!

## 2. Настройка автоответа (В отпуске)

### Через веб-интерфейс:
1. Откройте Яндекс Почту
2. Настройки (⚙️) → Почта → Автоответ
3. Включите "Присылать автоответы"
4. Укажите период и текст

### Программный автоответ:

```python
from yandex_mail_config import YandexMailClient, MailConfig
import os
import time

config = MailConfig(
    login=os.getenv("YANDEX_EMAIL"),
    password=os.getenv("YANDEX_APP_PASSWORD")
)

client = YandexMailClient(config)

# Проверяем новые письма каждые 5 минут
while True:
    unread = client.fetch_unread(limit=10)
    
    for email in unread:
        # Отправляем автоответ
        client.send_auto_reply(
            to=email['from'],
            template='vacation',
            start_date='01.05.2024',
            end_date='15.05.2024',
            backup_contact='backup@company.ru'
        )
        print(f"Автоответ отправлен: {email['from']}")
    
    time.sleep(300)  # 5 минут
```

## 3. Правила обработки

### Создание правил в Яндекс Почте:

1. Настройки → Правила обработки писем
2. "Создать правило"

**Примеры правил:**

| Условие | Действие |
|---------|----------|
| Тема содержит "заказ" | Переместить в папку "Заказы" + Автоответ |
| Отправитель @partner.com | Переместить в "Партнеры" + Пометить важным |
| Тема содержит "поддержка" | Переслать на support@company.ru |

## 4. Интеграция с сайтом

### HTML форма:

```html
<form id="contactForm">
  <input type="text" name="name" placeholder="Ваше имя" required>
  <input type="email" name="email" placeholder="Email" required>
  <input type="text" name="subject" placeholder="Тема" required>
  <textarea name="message" placeholder="Сообщение" required></textarea>
  <button type="submit">Отправить</button>
</form>

<script>
document.getElementById('contactForm').onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  
  const response = await fetch('/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(Object.fromEntries(formData))
  });
  
  const result = await response.json();
  alert(result.message);
};
</script>
```

## 5. Проверка DNS (для корпоративного домена)

Если используете свой домен:

```bash
# Проверьте MX записи
dig MX yourdomain.com

# Должно быть:
# 10 mx.yandex.net.
```

## 6. Ограничения Яндекс Почты

| Лимит | Значение |
|-------|----------|
| Писем в час | 500 |
| Получателей за раз | 35 |
| Размер вложения | 55 МБ |
| Ящик (бесплатно) | 10 ГБ |

---

**Готово!** Форма обратной связи настроена и работает через Яндекс Почту.
'''
    
    def _generate_webhook_handler(self) -> str:
        return '''"""
Webhook Handler для Яндекс Почты
Обрабатывает входящие письма через webhook
"""

from flask import Flask, request, jsonify
import hmac
import hashlib
from typing import Dict, Callable
import json

app = Flask(__name__)

class YandexMailWebhookHandler:
    """Обработчик вебхуков от Яндекс Почты"""
    
    def __init__(self, secret: str):
        self.secret = secret
        self.handlers: Dict[str, Callable] = {}
    
    def register_handler(self, event_type: str, handler: Callable):
        """Регистрация обработчика события"""
        self.handlers[event_type] = handler
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """Проверка подписи вебхука"""
        expected = hmac.new(
            self.secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected, signature)
    
    def process_webhook(self, data: Dict) -> Dict:
        """Обработка данных вебхука"""
        event_type = data.get('event_type', 'unknown')
        
        if event_type in self.handlers:
            return self.handlers[event_type](data)
        
        return {'status': 'ignored', 'event': event_type}


# Создаём обработчик
webhook_handler = YandexMailWebhookHandler(
    secret="your_webhook_secret"
)

# Обработчик новых писем
def handle_new_email(data: Dict) -> Dict:
    """Обработка нового входящего письма"""
    email_data = data.get('email', {})
    
    sender = email_data.get('from')
    subject = email_data.get('subject', '').lower()
    
    # Автоответ для определённых тем
    if 'заказ' in subject or 'order' in subject:
        # Создать задачу в CRM
        create_crm_task(email_data)
        return {'status': 'processed', 'action': 'crm_task_created'}
    
    if 'поддержка' in subject or 'support' in subject:
        # Отправить в систему поддержки
        create_support_ticket(email_data)
        return {'status': 'processed', 'action': 'support_ticket'}
    
    return {'status': 'processed', 'action': 'none'}

# Обработчик спама
def handle_spam(data: Dict) -> Dict:
    """Обработка письма помеченного как спам"""
    sender = data.get('email', {}).get('from')
    print(f"Spam detected from: {sender}")
    return {'status': 'logged'}

# Регистрируем обработчики
webhook_handler.register_handler('new_email', handle_new_email)
webhook_handler.register_handler('marked_spam', handle_spam)


@app.route('/webhook/yandex-mail', methods=['POST'])
def yandex_webhook():
    """Endpoint для вебхуков Яндекс Почты"""
    signature = request.headers.get('X-Yandex-Signature', '')
    payload = request.get_data()
    
    # Проверка подписи
    if not webhook_handler.verify_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    data = request.get_json()
    result = webhook_handler.process_webhook(data)
    
    return jsonify(result)


def create_crm_task(email_data: Dict):
    """Создать задачу в CRM"""
    # Интеграция с вашей CRM
    print(f"CRM Task: {email_data.get('subject')}")


def create_support_ticket(email_data: Dict):
    """Создать тикет в системе поддержки"""
    # Интеграция с helpdesk
    print(f"Support Ticket: {email_data.get('subject')}")


if __name__ == '__main__':
    app.run(port=5000)
'''
    
    def _generate_mail_fetcher(self) -> str:
        return '''#!/usr/bin/env python3
"""
Yandex Mail Fetcher
Периодическая проверка и обработка писем
"""

import asyncio
import os
from datetime import datetime
from yandex_mail_config import YandexMailClient, MailConfig


class MailFetcher:
    """Периодический сборщик писем"""
    
    def __init__(self, config: MailConfig):
        self.client = YandexMailClient(config)
        self.processed_ids = set()
    
    async def fetch_loop(self, interval: int = 60):
        """
        Цикл проверки почты
        
        Args:
            interval: Интервал проверки в секундах
        """
        while True:
            try:
                print(f"[{datetime.now()}] Проверка почты...")
                
                emails = self.client.fetch_unread(limit=20)
                
                for email in emails:
                    if email['id'] not in self.processed_ids:
                        await self.process_email(email)
                        self.processed_ids.add(email['id'])
                
                print(f"  Обработано: {len(emails)} писем")
                
            except Exception as e:
                print(f"Ошибка: {e}")
            
            await asyncio.sleep(interval)
    
    async def process_email(self, email: dict):
        """Обработка одного письма"""
        subject = email['subject'].lower()
        sender = email['from']
        
        print(f"  Новое письмо: {subject[:50]}... от {sender}")
        
        # Автоответы по ключевым словам
        if any(word in subject for word in ['заказ', 'order', 'покупка']):
            self.client.send_auto_reply(
                to=sender,
                template='order_confirmation',
                order_id=self.extract_order_id(email['body']),
                amount=self.extract_amount(email['body'])
            )
        
        elif any(word in subject for word in ['вакансия', 'резюме', 'job']):
            # Переслать HR
            print(f"    → Переслано в HR")
        
        elif 'партнер' in subject:
            # Переслать отделу партнёрства
            print(f"    → Переслано в Партнёрства")
    
    def extract_order_id(self, body: str) -> str:
        """Извлечь номер заказа из текста"""
        # Простой пример - в реальности используйте регулярные выражения
        return "ORD-2024-001"
    
    def extract_amount(self, body: str) -> str:
        """Извлечь сумму из текста"""
        return "1500"


async def main():
    config = MailConfig(
        login=os.getenv("YANDEX_EMAIL"),
        password=os.getenv("YANDEX_APP_PASSWORD")
    )
    
    fetcher = MailFetcher(config)
    
    print("📧 Yandex Mail Fetcher запущен")
    print("Нажмите Ctrl+C для остановки")
    
    try:
        await fetcher.fetch_loop(interval=60)  # Проверка каждую минуту
    except KeyboardInterrupt:
        print("\\n👋 Остановлено")


if __name__ == "__main__":
    asyncio.run(main())
'''


def main():
    parser = argparse.ArgumentParser(description="📧 YandexMail-Agent")
    parser.add_argument("request", nargs="?", help="Задача")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = YandexMailAgent()
    
    if args.request:
        print(f"📧 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"📧 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"\\nSMTP: {agent.SMTP_HOST}:{agent.SMTP_PORT}")
        print(f"IMAP: {agent.IMAP_HOST}:{agent.IMAP_PORT}")


if __name__ == "__main__":
    main()
