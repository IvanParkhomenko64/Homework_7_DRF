from rest_framework import serializers

from courses.models import Lesson
from courses.validators import LessonValidator


class LessonSerializer(serializers.ModelSerializer):
    amount_of_lessons = serializers.SerializerMethodField()
    validators = [LessonValidator(field="ref")]

    def get_amount_of_lessons(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = "__all__"
        # fields = (
        #     'name', 'description', 'image', 'ref', 'amount_of_lessons',
        # )



class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
