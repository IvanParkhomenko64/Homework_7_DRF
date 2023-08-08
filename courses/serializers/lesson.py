from rest_framework import serializers

from courses.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    amount_of_lessons = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = (
            'name', 'description', 'image', 'ref', 'amount_of_lessons',
        )


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
