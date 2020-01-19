# animal_cf/urls.py

from django.urls import path
from . import views

app_name = 'animal_cf'

urlpatterns = [
    path('', views.index, name='index'),
]
