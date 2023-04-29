from django.urls import path
from . import views

urlpatterns = [
    path('stratified/', views.stratified_sampling,name='stratified_sampling'),
    path('get_data/', views.get_data,name='get_data'),
]