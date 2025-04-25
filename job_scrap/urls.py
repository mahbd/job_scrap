# Python
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bd.therap import scrap_therap
from bd.views import JobViewSet

router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

@api_view(['GET'])
def scrap_therap_req(request):
    scrap_therap()
    return Response({"status": "scraping started"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('scrap_therap/', scrap_therap_req, name='scrap_therap'),
]