from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)