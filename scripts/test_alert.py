#!/usr/bin/env python3
"""
🚨 Test Alert - Триггер тестового алерта
"""
import requests
import sys


def send_test_alert(level='warning', title='🧪 Test Alert', message='Test message'):
    """Отправка тестового алерта через API"""
    
    url = 'http://localhost:5000/api/alerts/test'
    
    data = {
        'level': level,
        'title': title,
        'message': message,
        'metric_name': 'success_rate',
        'threshold_value': 80,
        'current_value': 65
    }
    
    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            print(f"✅ Alert sent: [{level}] {title}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Dashboard not running on localhost:5000")
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        level = sys.argv[1]
        send_test_alert(level=level)
    else:
        # Отправляем все типы
        print("🚨 Sending test alerts...\n")
        send_test_alert('info', 'ℹ️ Info Alert', 'This is an informational alert')
        send_test_alert('warning', '⚠️ Warning Alert', 'Success rate is below threshold')
        send_test_alert('critical', '🚨 Critical Alert', 'Success rate critically low!')
