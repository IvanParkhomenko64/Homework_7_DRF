from rest_framework.pagination import PageNumberPagination


class LessonPagination(PageNumberPagination):
    page_size = 10


class CoursePagination(PageNumberPagination):
    page_size = 5
