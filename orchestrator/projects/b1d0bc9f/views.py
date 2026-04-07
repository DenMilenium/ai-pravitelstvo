from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    """Главная страница"""
    return render(request, 'home.html', {
        'title': 'AI Правительство',
        'message': 'Добро пожаловать!'
    })

def api_status(request):
    """API статус"""
    return JsonResponse({
        'status': 'ok',
        'service': 'ai-pravitelstvo',
        'version': '1.0.0'
    })
