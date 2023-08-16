from rest_framework import generics

from subscriptions.models import Subscription
from subscriptions.pagination import SubscriptionPagination
from subscriptions.serializers import SubscriptionSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Создание подписки"""
    serializer_class = SubscriptionSerializer


class SubscriptionListAPIView(generics.ListAPIView):
    """Просмотр списка подписок"""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    pagination_class = SubscriptionPagination


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    """Отображение элемента подписки """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """Изменение элемента подписки"""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Удаление элемента подписки"""
    queryset = Subscription.objects.all()