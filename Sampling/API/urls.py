from django.urls import path
from . import views

urlpatterns = [
    path('',views.samplingInternalAPI, name = "Internal Sampling API"),
    path('<str:api_key>/',views.samplingAPI, name = "Public Sampling API")
]