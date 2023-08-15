from django.urls import path

from subscriptions.apps import SubscriptionsConfig
from subscriptions.views import *

app_name = SubscriptionsConfig.name

urlpatterns = [
    path("create/", SubscriptionCreateAPIView.as_view(), name="subscription_create"),
    path("list/", SubscriptionListAPIView.as_view(), name="subscription_list"),
    path("deteil/<int:pk>/", SubscriptionRetrieveAPIView.as_view(), name="subscription_deteil",),
    path("update/<int:pk>/", SubscriptionUpdateAPIView.as_view(), name="subscription_update",),
    path("delete/<int:pk>/", SubscriptionDestroyAPIView.as_view(), name="subscription_delete",),
]