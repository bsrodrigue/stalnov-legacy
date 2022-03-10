import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls

urlpatterns = [
    path("", include("apps.main.urls")),
    path(
        "inbox/notifications/", include(notifications.urls, namespace="notifications")
    ),
    path("admin/", admin.site.urls),
]


DEV_ENV = os.getenv("ENV", "dev") == "dev"

if DEV_ENV:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
