from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from courses.models import Lesson
from courses.pagination import LessonPagination
from courses.serializers.lesson import LessonSerializer, LessonListSerializer
from users.permissions import *
from courses.tasks import *


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsOwnerOrModerator]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsOwnerOrModerator]


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator]

    def perform_create(self, serializer):
        """Переопределение метода perform_create для добавления пользователя созданному уроку"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        # Отправка на выполнение задачи при создании нового урока в курсе
        if new_lesson:
            send_course_create.delay(new_lesson.course_id)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    # permission_classes = [IsOwnerOrModerator]
    def perform_update(self, serializer):
        """Переопределение метода perform_update"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        # Отправка на выполнение задачи при изменении нового урока в курсе
        if new_lesson.course:
            new_lesson.course.last_updated = timezone.now()
            new_lesson.course.save()

            # Отправляем уведомление только если курс не обновлялся более 4 часов
        if new_lesson.course:
            send_course_update.delay(new_lesson.course_id)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsOwner]
