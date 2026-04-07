"""
🐍 Django Agent
Создаёт Django проекты с models, views, templates
"""

from orchestrator.core.task_executor import BaseAgentExecutor
from orchestrator.core.database import Task
from typing import Dict


class DjangoAgentExecutor(BaseAgentExecutor):
    """
    🐍 Django Developer Agent
    
    Генерирует:
    - Django models
    - Views (FBV и CBV)
    - Templates
    - Admin configuration
    - API endpoints (DRF)
    """
    
    AGENT_TYPE = 'django'
    NAME = 'Django Agent'
    EMOJI = '🐍'
    
    def can_execute(self, task: Task) -> bool:
        return task.agent_type in ['django', 'python', 'backend']
    
    def execute(self, task: Task) -> Dict:
        """Генерирует Django проект"""
        
        title = task.title.lower()
        
        if 'api' in title or 'rest' in title:
            return self._create_api(task)
        elif 'blog' in title or 'cms' in title:
            return self._create_blog(task)
        elif 'shop' in title or 'магазин' in title or 'e-commerce' in title:
            return self._create_shop(task)
        else:
            return self._create_default_app(task)
    
    def _create_api(self, task: Task) -> Dict:
        """Создаёт Django REST API"""
        
        models_py = '''from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """Модель проекта"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активный'),
        ('completed', 'Завершён'),
    ]
    
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """Модель задачи"""
    PRIORITY_CHOICES = [
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    priority = models.IntegerField('Приоритет', choices=PRIORITY_CHOICES, default=2)
    completed = models.BooleanField('Выполнено', default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField('Срок выполнения', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"
'''

        serializers_py = '''from rest_framework import serializers
from .models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для задач"""
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'completed', 
                  'assigned_to', 'assigned_to_name', 'created_at', 'due_date']


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор для проектов с вложенными задачами"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    tasks_count = serializers.SerializerMethodField()
    completed_tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'owner', 'owner_name',
                  'tasks', 'tasks_count', 'completed_tasks_count', 'created_at']
    
    def get_tasks_count(self, obj):
        return obj.tasks.count()
    
    def get_completed_tasks_count(self, obj):
        return obj.tasks.filter(completed=True).count()
'''

        views_py = '''from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления проектами
    
    list: Получить список проектов
    create: Создать новый проект
    retrieve: Получить детали проекта
    update: Обновить проект
    destroy: Удалить проект
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'owner']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    
    def get_queryset(self):
        """Пользователь видит только свои проекты"""
        return Project.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """Автоматически назначаем текущего пользователя владельцем"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Отметить проект как завершённый"""
        project = self.get_object()
        project.status = 'completed'
        project.save()
        return Response({'status': 'project completed'})


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления задачами
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'completed', 'priority', 'assigned_to']
    
    def get_queryset(self):
        """Фильтр по проектам пользователя"""
        return Task.objects.filter(project__owner=self.request.user)
    
    @action(detail=False)
    def my_tasks(self, request):
        """Получить задачи, назначенные текущему пользователю"""
        tasks = self.get_queryset().filter(assigned_to=request.user, completed=False)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Отметить задачу как выполненную"""
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({'status': 'task completed'})
'''

        urls_py = '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
'''

        settings_rest = '''# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'PAGE_SIZE': 20
}

# JWT settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
'''

        readme = '''# Django REST API

🐍 API создано с помощью AI Правительство

## Установка

```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Method | Endpoint | Описание |
|--------|----------|----------|
| GET | /api/projects/ | Список проектов |
| POST | /api/projects/ | Создать проект |
| GET | /api/projects/{id}/ | Детали проекта |
| GET | /api/tasks/ | Список задач |
| POST | /api/auth/token/ | Получить JWT токен |

## Модели

- **Project** - Проекты с задачами
- **Task** - Задачи с приоритетами
'''

        return {
            'success': True,
            'message': f'✅ Django REST API создано!',
            'artifacts': {
                'models.py': models_py,
                'serializers.py': serializers_py,
                'views.py': views_py,
                'urls.py': urls_py,
                'settings_rest.py': settings_rest,
                'README.md': readme
            }
        }
    
    def _create_blog(self, task: Task) -> Dict:
        """Создаёт Django Blog"""
        
        models_py = '''from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """Модель поста блога"""
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField('Содержание')
    excerpt = models.TextField('Анонс', blank=True)
    image = models.ImageField('Изображение', upload_to='posts/%Y/%m/', blank=True)
    published = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)
    status = models.CharField('Статус', max_length=10, 
                              choices=[('draft', 'Черновик'), ('published', 'Опубликовано')],
                              default='draft')
    tags = models.CharField('Теги', max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """Комментарии к постам"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('Комментарий')
    created = models.DateTimeField('Создан', auto_now_add=True)
    active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']
    
    def __str__(self):
        return f'Комментарий от {self.author}'
'''

        return {
            'success': True,
            'message': f'✅ Django Blog создан!',
            'artifacts': {
                'models.py': models_py,
                'README.md': '# Django Blog\n\nПростой блог на Django'
            }
        }
    
    def _create_shop(self, task: Task) -> Dict:
        """Создаёт Django E-commerce"""
        
        models_py = '''from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('На складе', default=0)
    available = models.BooleanField('Доступен', default=True)
    image = models.ImageField('Изображение', upload_to='products/', blank=True)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']
    
    def __str__(self):
        return self.name


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('processing', 'Обрабатывается'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=250)
    postal_code = models.CharField('Индекс', max_length=20)
    city = models.CharField('Город', max_length=100)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    paid = models.BooleanField('Оплачен', default=False)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
    
    def __str__(self):
        return f'Заказ {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)
    
    def __str__(self):
        return f'{self.id}'
    
    def get_cost(self):
        return self.price * self.quantity
'''

        return {
            'success': True,
            'message': f'✅ Django E-commerce создан!',
            'artifacts': {
                'models.py': models_py,
                'README.md': '# Django Shop\n\nИнтернет-магазин на Django'
            }
        }
    
    def _create_default_app(self, task: Task) -> Dict:
        """Создаёт базовое Django приложение"""
        
        views_py = '''from django.shortcuts import render
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
'''

        urls_py = '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/status/', views.api_status, name='api_status'),
]
'''

        return {
            'success': True,
            'message': f'✅ Базовое Django приложение создано!',
            'artifacts': {
                'views.py': views_py,
                'urls.py': urls_py,
                'README.md': '# Django App\n\nБазовое приложение на Django'
            }
        }
