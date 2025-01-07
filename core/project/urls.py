from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include('main.presentation.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
    ] + debug_toolbar_urls()

