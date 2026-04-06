#!/usr/bin/env python3
"""
📧 Email-Agent
Email Developer агент

Создаёт:
- Email шаблоны
- HTML письма
- MJML email
- Email рассылки
"""

import argparse
from pathlib import Path
from typing import Dict


class EmailAgent:
    """
    📧 Email-Agent
    
    Специализация: Email Development
    Технологии: HTML Email, MJML, CSS
    """
    
    NAME = "📧 Email-Agent"
    ROLE = "Email Developer"
    EXPERTISE = ["HTML Email", "MJML", "Email Templates", "Newsletters", "Transactional"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["welcome-email.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <title>Welcome!</title>
  <style>
    /* Reset styles for email clients */
    body, table, td, p, a, li, blockquote {
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    img { -ms-interpolation-mode: bicubic; border: 0; }
    
    /* Responsive */
    @media screen and (max-width: 600px) {
      .container { width: 100% !important; }
      .content { padding: 20px !important; }
      .button { width: 100% !important; }
    }
  </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4;">
  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
    <tr>
      <td align="center" style="padding: 40px 0;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" class="container" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
          
          <!-- Header -->
          <tr>
            <td align="center" style="padding: 40px 40px 20px;" class="content">
              <img src="https://example.com/logo.png" alt="Logo" width="120" style="display: block;">
            </td>
          </tr>
          
          <!-- Content -->
          <tr>
            <td style="padding: 20px 40px;" class="content">
              <h1 style="color: #333333; font-family: Arial, sans-serif; font-size: 28px; margin: 0 0 20px; text-align: center;">
                Welcome to Our Platform! 🎉
              </h1>
              <p style="color: #666666; font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6; margin: 0 0 20px;">
                Hi {{name}},
              </p>
              <p style="color: #666666; font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6; margin: 0 0 30px;">
                Thank you for joining us! We're excited to have you on board. Get started by exploring your new dashboard.
              </p>
              
              <!-- CTA Button -->
              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                <tr>
                  <td align="center" style="padding: 20px 0;">
                    <a href="{{dashboard_url}}" class="button" style="display: inline-block; padding: 15px 40px; background-color: #3b82f6; color: #ffffff; text-decoration: none; border-radius: 6px; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold;">
                      Go to Dashboard
                    </a>
                  </td>
                </tr>
              </table>
              
              <p style="color: #999999; font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; margin: 30px 0 0; text-align: center;">
                If you didn't create an account, you can safely ignore this email.
              </p>
            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td style="padding: 30px 40px; background-color: #f9f9f9; border-radius: 0 0 8px 8px;" class="content">
              <p style="color: #999999; font-family: Arial, sans-serif; font-size: 12px; line-height: 1.6; margin: 0; text-align: center;">
                © 2024 Your Company. All rights reserved.<br>
                <a href="{{unsubscribe_url}}" style="color: #999999; text-decoration: underline;">Unsubscribe</a>
              </p>
            </td>
          </tr>
          
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
        
        files["newsletter.mjml"] = """<mjml>
  <mj-head>
    <mj-title>Monthly Newsletter</mj-title>
    <mj-font name="Inter" href="https://fonts.googleapis.com/css?family=Inter" />
    <mj-attributes>
      <mj-all font-family="Inter, Arial, sans-serif" />
      <mj-text font-size="16px" color="#333333" line-height="1.6" />
      <mj-button background-color="#3b82f6" color="white" border-radius="6px" />
    </mj-attributes>
  </mj-head>
  
  <mj-body background-color="#f4f4f4">
    
    <!-- Header -->
    <mj-section background-color="#3b82f6" padding="30px">
      <mj-column>
        <mj-image src="https://example.com/logo-white.png" alt="Logo" width="150px" />
        <mj-text color="white" font-size="24px" font-weight="bold" align="center">
          Monthly Newsletter
        </mj-text>
      </mj-column>
    </mj-section>
    
    <!-- Hero -->
    <mj-section background-color="white" padding="40px 30px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" align="center">
          What's New This Month
        </mj-text>
        <mj-text align="center" color="#666666">
          Catch up on the latest updates, features, and insights from our team.
        </mj-text>
      </mj-column>
    </mj-section>
    
    <!-- Article 1 -->
    <mj-section background-color="white" padding="0 30px 30px">
      <mj-column width="40%">
        <mj-image src="https://example.com/article1.jpg" alt="Article" border-radius="8px" />
      </mj-column>
      <mj-column width="60%">
        <mj-text font-size="20px" font-weight="bold">
          New Feature Launch
        </mj-text>
        <mj-text color="#666666">
          We've added powerful new tools to help you work more efficiently.
        </mj-text>
        <mj-button href="https://example.com/article1">
          Read More
        </mj-button>
      </mj-column>
    </mj-section>
    
    <!-- Article 2 -->
    <mj-section background-color="#f9f9f9" padding="30px">
      <mj-column width="60%">
        <mj-text font-size="20px" font-weight="bold">
          Customer Success Story
        </mj-text>
        <mj-text color="#666666">
          See how Company XYZ increased productivity by 200% using our platform.
        </mj-text>
        <mj-button href="https://example.com/article2">
          Read Story
        </mj-button>
      </mj-column>
      <mj-column width="40%">
        <mj-image src="https://example.com/article2.jpg" alt="Success Story" border-radius="8px" />
      </mj-column>
    </mj-section>
    
    <!-- Footer -->
    <mj-section background-color="#333333" padding="30px">
      <mj-column>
        <mj-text color="#999999" font-size="12px" align="center">
          © 2024 Your Company. All rights reserved.<br>
          <a href="{{unsubscribe_url}}" style="color: #999999;">Unsubscribe</a> | 
          <a href="{{preferences_url}}" style="color: #999999;">Preferences</a>
        </mj-text>
        <mj-social font-size="12px" icon-size="24px" mode="horizontal" align="center">
          <mj-social-element name="facebook" href="https://facebook.com/yourcompany" />
          <mj-social-element name="twitter" href="https://twitter.com/yourcompany" />
          <mj-social-element name="linkedin" href="https://linkedin.com/company/yourcompany" />
        </mj-social>
      </mj-column>
    </mj-section>
    
  </mj-body>
</mjml>
"""
        
        files["email-styles.css"] = """/* Email-safe CSS */
/* Use inline styles for best compatibility */

/* Base */
.email-body {
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.email-container {
  max-width: 600px;
  margin: 0 auto;
  background-color: #ffffff;
}

/* Typography */
.email-h1 {
  color: #333333;
  font-size: 28px;
  font-weight: bold;
  line-height: 1.3;
  margin: 0 0 20px;
}

.email-h2 {
  color: #333333;
  font-size: 22px;
  font-weight: bold;
  line-height: 1.4;
  margin: 0 0 15px;
}

.email-text {
  color: #666666;
  font-size: 16px;
  line-height: 1.6;
  margin: 0 0 15px;
}

.email-small {
  color: #999999;
  font-size: 12px;
  line-height: 1.5;
}

/* Button */
.email-button {
  display: inline-block;
  padding: 15px 40px;
  background-color: #3b82f6;
  color: #ffffff !important;
  text-decoration: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
}

/* Layout */
.email-section {
  padding: 40px;
}

.email-header {
  background-color: #3b82f6;
  padding: 40px;
  text-align: center;
}

.email-footer {
  background-color: #f9f9f9;
  padding: 30px 40px;
  text-align: center;
}

/* Utilities */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.mb-0 { margin-bottom: 0; }
.mt-20 { margin-top: 20px; }
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="📧 Email-Agent — Email Development")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = EmailAgent()
    
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
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"📧 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
