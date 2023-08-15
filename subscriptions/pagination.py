from rest_framework.pagination import PageNumberPagination


class SubscriptionPagination(PageNumberPagination):
    """Класс описания пагинации подписок"""
    page_size = 10