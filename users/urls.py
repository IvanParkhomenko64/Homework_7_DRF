from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (PaymentsListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update-user"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("payments/", PaymentsListAPIView.as_view(), name="user-payments"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]