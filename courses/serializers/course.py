import stripe
from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from config import settings
from courses.models import Course, Lesson
from courses.serializers.lesson import LessonSerializer, LessonListSerializer


stripe.api_key = settings.STRIPE_API_KEY

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = IntegerField()
    lessons = LessonSerializer(many=True, required=False)
    lesson_this_course = SerializerMethodField()
    subscription = SerializerMethodField(read_only=True)
    payments = serializers.SerializerMethodField()

    def get_lesson_this_course(self, course):
        return LessonListSerializer(Lesson.objects.filter(course=course), many=True).data
        # return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    def get_subscription(self, instance):
        request = self.context.get("request")
        user = request.user
        sub_all = instance.subscription.all()
        for sub in sub_all:
            if sub.subscriber == user:
                return True
        return False

    def get_payments(self, course):
        """Добавление оплаты для курса"""
        # создание продукта с именем, которое берется из имени курса
        payment = stripe.Product.create(
            name=course.name,
        )
        # Создание цены на продукт:
        price = stripe.Price.create(
            # сумма
            unit_amount=int(course.price*90),
            # валюта
            currency="usd",
            # привязка к продукту
            product=payment["id"],
        )
        # Создание платежной сессии
        session = stripe.checkout.Session.create(
            # адрес после успешного платежа
            success_url="https://example.com/success",
            # при неудаче
            cancel_url="https://example.com/cancel",
            # Тип платежного метода
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price["id"],
                    # количество
                    "quantity": 1,
                },
            ],
            # Режим платежа
            mode="payment",
        )
        # Возврат URL-адреса для оплаты
        return session["url"]

    class Meta:
        model = Course
        fields = "__all__"
