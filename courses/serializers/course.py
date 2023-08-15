from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from courses.models import Course, Lesson
from courses.serializers.lesson import LessonSerializer, LessonListSerializer


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = IntegerField()
    lessons = LessonSerializer(many=True, required=False)
    lesson_this_course = SerializerMethodField()
    subscription = SerializerMethodField(read_only=True)

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

    class Meta:
        model = Course
        fields = "__all__"
