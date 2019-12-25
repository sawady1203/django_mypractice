# animal_cf/urls.py

from django.urls import path
from . import views

app_name = 'animal_cf'

urlpatterns = [
    path('', views.index, name='index'),
    # path('animal_cf/', views.animal_classify, name='animal_classify')
]