from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
    path("user/", include('users.urls', namespace="user")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)