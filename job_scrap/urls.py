# Python
from django.contrib import admin
from django.urls import path, include

from bd.urls import urlpatterns as bd_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bd/', include(bd_urls)),
]