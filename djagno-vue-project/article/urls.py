# article/urls.py

from django.urls import path
from django.views.generic import TemplateView

app_name = "article"

urlpatterns = [
    path('', TemplateView.as_view(template_name='article/index.html')),
]
