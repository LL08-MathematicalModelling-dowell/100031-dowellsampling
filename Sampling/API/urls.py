from django.urls import path
from . import views

urlpatterns = [
    path('stratified/', views.stratified_sampling, name='stratified_sampling'),
    path('get_data/', views.get_data,name='get_data'),
    path('systematic/', views.systematic_sampling,name='systematic_sampling'),
    path('simple_random/', views.simple_random_sampling,name='simple_random_sampling'),
    path('sampling_input/', views.sampling_input,name='sampling_input'),
    path('cluster_sampling/', views.cluster_sampling,name='cluster_sampling'),
]
