from django.db import models
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
