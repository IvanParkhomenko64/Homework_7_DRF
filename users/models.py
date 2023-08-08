from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Lesson, Course

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=100, verbose_name='номер телефона', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-date_of_payment',)

    CASH = 'cash'
    TRANSFER = 'transfer'

    METHOD_CHOICES = (
        (CASH, 'cash'),
        (TRANSFER, 'translation'),
    )

    date_of_payment = models.DateTimeField(
        auto_now_add=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Сумма платежа',
    )
    method = models.CharField(
        max_length=50, choices=METHOD_CHOICES,
    )
    paid_lesson = models.ForeignKey(
        Lesson, verbose_name='Оплаченный урок', on_delete=models.CASCADE,
        **NULLABLE, related_name='paid_lessons',
    )
    paid_course = models.ForeignKey(
        Course, verbose_name='Оплаченный курс', on_delete=models.CASCADE,
        **NULLABLE, related_name='paid_courses',
    )
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE,
        related_name='payments',
    )