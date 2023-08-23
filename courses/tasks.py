from datetime import timedelta
from time import timezone

from celery import shared_task
from django.core.mail import send_mail

import subscriptions
from config import settings
from courses.models import Course
from subscriptions.models import Subscription
from users.models import User


@shared_task
def send_course_create(course_id):
    """Задача рассылки писем при создании уроков  курса"""
    try:
        course = Course.objects.get(pk=course_id)  # Получаем курс
        sub_course = Subscription.objects.filter(
            course=course_id
        )  # получаем подписки на курс course_id
        # Перебор подпищиков
        for sub in sub_course:
            send_mail(
                subject=f"Обновление {course.name}",
                message=f" Курс {course.name} обновился",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[f"{sub.subscriber}"],  # список рассылки
                fail_silently=True,  # Исключение исключения о неправильной отправке или не удачной
            )
    except:
        print("Ошибка отправки")


@shared_task
def send_course_update(course_id):
    """Задача рассылки писем при обновлении уроков  курса"""
    try:
        course = Course.objects.get(pk=course_id)  # Получаем курс
        sub_couse = Subscription.objects.filter(
            course=course_id
        )  # получаем подписки на курс course_id
        last_updated = course.last_updated
        current_time = timezone.now()
        if (current_time - last_updated) > timedelta(hours=4):
            # Перебор подпищиков
            for sub in sub_couse:
                send_mail(
                    subject=f"Обновление {course.course_name}",
                    message=f" Курс {course.course_name} обновился",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[f"{sub.subscriber}"],  # список рассылки
                    fail_silently=True,  # Исключение исключения о неправильной отправке, или не удачной
                )
    except:
        print("Ошибка отправки")


@shared_task
def block_in_active_users():
    """Задача для блокирования пользователей при не активности в течении 30 дней."""
    User.objects.filter(
        last_login__lt=timezone.now() - timezone.timedelta(days=30)
    ).update(is_active=False)