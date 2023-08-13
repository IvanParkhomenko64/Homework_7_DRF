from django.conf import settings
from django.db import models
import datetime

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='courses/', verbose_name='Изображение', **NULLABLE)
    owner = models.ForeignKey('users.User', verbose_name='владелец', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='courses/', verbose_name='Изображение', **NULLABLE)
    ref = models.TextField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', **NULLABLE)
    owner = models.ForeignKey('users.User', verbose_name='владелец', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

