from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/status/', views.api_status, name='api_status'),
]
