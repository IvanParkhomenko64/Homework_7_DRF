from rest_framework.pagination import PageNumberPagination


class PaymentPagination(PageNumberPagination):
    page_size = 5
