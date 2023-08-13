from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from courses.models import Lesson
from courses.serializers.lesson import LessonSerializer, LessonListSerializer
from users.permissions import *


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator]

    def perform_create(self, serializer):
        """Переопределение метода perform_create для добавления пользователя созданному уроку"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]