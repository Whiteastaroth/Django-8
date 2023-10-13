from django.db import models
from django.contrib.auth.models import User

from django.core.cache import cache

class New(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def preview(self):
        preview = f'{self.text[:128]}...'
        return preview


    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )