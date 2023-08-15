import re

from rest_framework.exceptions import ValidationError


class LessonValidator:
    """Валидация данных для уроков"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        field_new = dict(value).get(self.field)
        if field_new:
            if not bool(re.search(r"youtube.com", field_new)):
                raise ValidationError("Размещать видео можно только на платформе youtube.com")