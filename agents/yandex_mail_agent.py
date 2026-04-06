#!/usr/bin/env python3
"""📧 YandexMail-Agent - Yandex Mail Integration Specialist"""

import argparse
from pathlib import Path
from typing import Dict


class YandexMailAgent:
    """📧 YandexMail-Agent - Yandex Mail Integration"""
    
    NAME = "📧 YandexMail-Agent"
    ROLE = "Yandex Mail Specialist"
    EXPERTISE = ["Yandex SMTP", "Yandex IMAP", "Email Automation", "Webhooks"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "yandex-mail-setup.md": self._generate_setup_guide(),
            "smtp-config.py": self._generate_smtp_config(),
            "contact-form.html": self._generate_contact_form(),
            "auto-reply-templates.md": self._generate_templates()
        }
    
    def _generate_setup_guide(self) -> str:
        return '''# Yandex Mail Integration Guide

## Setup Instructions

### 1. Create App Password
1. Go to https://mail.yandex.ru
2. Settings -> Security -> App passwords
3. Generate password for your application

### 2. SMTP Configuration
- Host: smtp.yandex.ru
- Port: 465 (SSL) or 587 (TLS)
- Login: your-email@yandex.ru
- Password: App password (not your main password!)

### 3. IMAP Configuration
- Host: imap.yandex.ru
- Port: 993 (SSL)
- Login: your-email@yandex.ru
- Password: App password

## Usage Examples

### Send Email
```python
from yandex_mail import YandexMailClient, MailConfig

config = MailConfig(
    login="your@yandex.ru",
    password="app-password"
)
client = YandexMailClient(config)

client.send_email(
    to="recipient@example.com",
    subject="Hello",
    body="Test message"
)
```

### Fetch Unread Emails
```python
emails = client.fetch_unread(folder="INBOX", limit=10)
for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
```
'''
    
    def _generate_smtp_config(self) -> str:
        return """import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class MailConfig:
    login: str
    password: str
    smtp_host: str = "smtp.yandex.ru"
    smtp_port: int = 465
    imap_host: str = "imap.yandex.ru"
    imap_port: int = 993


class YandexMailClient:
    def __init__(self, config: MailConfig):
        self.config = config
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config.login
            msg['To'] = to
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            if html_body:
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            with smtplib.SMTP_SSL(
                self.config.smtp_host,
                self.config.smtp_port
            ) as server:
                server.login(self.config.login, self.config.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def fetch_unread(self, folder: str = "INBOX", limit: int = 10) -> List[Dict]:
        emails = []
        try:
            mail = imaplib.IMAP4_SSL(
                self.config.imap_host,
                self.config.imap_port
            )
            mail.login(self.config.login, self.config.password)
            mail.select(folder)
            
            _, search_data = mail.search(None, 'UNSEEN')
            email_ids = search_data[0].split()[-limit:]
            
            for e_id in email_ids:
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
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
                    'body': body[:500]
                })
            
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Error: {e}")
        
        return emails


if __name__ == "__main__":
    config = MailConfig(
        login="your@yandex.ru",
        password="app-password"
    )
    client = YandexMailClient(config)
"""
    
    def _generate_contact_form(self) -> str:
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Contact Form</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>Contact Us</h1>
    <form action="/api/contact" method="POST">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="subject">Subject</label>
            <input type="text" id="subject" name="subject" required>
        </div>
        <div class="form-group">
            <label for="message">Message</label>
            <textarea id="message" name="message" rows="5" required></textarea>
        </div>
        <button type="submit">Send Message</button>
    </form>
</body>
</html>'''
    
    def _generate_templates(self) -> str:
        return '''# Email Templates

## Support Auto-Reply

**Subject**: Thank you for your inquiry!

**Body**:
```
Hello!

Thank you for contacting us. We have received your message and will respond within 24 hours.

Your inquiry: {message_preview}

--
Best regards,
Support Team
```

## Order Confirmation

**Subject**: Order #{order_id} confirmed!

**Body**:
```
Thank you for your order!

Order Number: {order_id}
Amount: {amount}

We will contact you to confirm.

--
Store Team
```

## Vacation Auto-Reply

**Subject**: Auto-reply: On vacation

**Body**:
```
Hello!

I am on vacation from {start_date} to {end_date}.

For urgent matters, please contact: {backup_contact}

--
{signature}
```
'''


def main():
    parser = argparse.ArgumentParser(description="📧 YandexMail-Agent")
    parser.add_argument("--output", "-o", help="Output directory")
    args = parser.parse_args()
    
    agent = YandexMailAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"Generated: {filename}")
    else:
        print(f"{agent.NAME}")
        for filename in files.keys():
            print(f"  - {filename}")


if __name__ == "__main__":
    main()
