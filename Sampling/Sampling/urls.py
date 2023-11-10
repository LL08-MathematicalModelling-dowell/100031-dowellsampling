from django.contrib import admin
from django.urls import path, include
from API.views import insert_data
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('API.urls')),
    path('sample-size/', include('SampleSizeApi.urls')),
    path('insert/',insert_data,name='insert_data')
    
]
