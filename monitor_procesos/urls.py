# monitor_procesos/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('monitor_windows/', include('monitor_windows.urls')),
    path('monitor_linux/', include('monitor_linux.urls')),
]
