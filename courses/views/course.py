from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from courses.models import Course
from courses.serializers.course import *
from users.permissions import *


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(lesson_count=Count("lesson"))
    dafault_serializer = CourseListSerializer
    serializers = {
        "list": CourseDetailSerializer,
        "retrieve": CourseDetailSerializer
    }
    #permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.dafault_serializer)

    def perform_create(self, serializer):
        """Переопределение метода perform_create для добавления пользователя"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        """Переопределение метода get_permissions для назначение разных прав доступа на разные дейтсвия"""
        # создавать курсы может только пользователь, не входящий в группу модераторы
        if self.action == "create":
            permission_classes = [IsNotModerator]
        # редактировать курсы может только создатель курса или модератор
        elif self.action == "update" or self.action == "partial_update":
            permission_classes = [IsOwnerOrModerator]
        elif self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]

        # удалять курсы может только их создатель
        elif self.action == "destroy":
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]