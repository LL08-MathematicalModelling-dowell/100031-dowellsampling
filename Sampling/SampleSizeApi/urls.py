from django.urls import path
from . import views

urlpatterns = [
    path('', views.sample_size),
    path('health_checks/', views.health_check),
    path('<str:api_key>/', views.sample_size_api),
]
