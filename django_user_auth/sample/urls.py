# sample/urls.py

from django.urls import path, include
from . import views

app_name = 'sample'  # 追加

urlpatterns = [
    path('', views.index, name='index'),
]
