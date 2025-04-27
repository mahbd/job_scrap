from django.urls import path, include
from rest_framework import routers

from . import views
from .views import JobViewSet

router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

app_name = 'bd'
urlpatterns = [
    path('api/', include(router.urls)),
    path('jobs/', views.get_job_list_html, name='job_list'),
    path('jobs/<int:pk>/', views.get_job_detail_html, name='job_detail'),
    path('scrap-cefalo/', views.scrap_cefalo_req, name='scrap_cefalo'),
    path('scrap-therap/', views.scrap_therap_req, name='scrap_therap'),
    path('scrap-welldev/', views.scrap_welldev_req, name='scrap_welldev'),
]