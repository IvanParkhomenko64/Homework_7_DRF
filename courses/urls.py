from rest_framework import routers

from courses.apps import CoursesConfig
from django.urls import path

from courses.views.course import CourseViewSet
from courses.views.lesson import *

app_name = CoursesConfig.name

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lessons'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='view'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='create'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete'),
]


router = routers.SimpleRouter()
router.register('', CourseViewSet)

urlpatterns += router.urls