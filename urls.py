# main/urls.py
from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_get/', views.ajax_get, name="ajax_get"),
    path('ajax_post/', views.ajax_post, name="ajax_post"),
]
