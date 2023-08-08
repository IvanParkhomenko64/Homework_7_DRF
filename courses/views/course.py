from django.db.models import Count
from rest_framework import viewsets

from courses.models import Course
from courses.serializers.course import *


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(lesson_count=Count("lesson"))
    dafault_serializer = CourseListSerializer
    serializers = {
        "list": CourseDetailSerializer,
        "retrieve": CourseDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.dafault_serializer)
