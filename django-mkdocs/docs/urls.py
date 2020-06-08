from django.urls import path, re_path
from . import views

app_name = "docs"

urlpatterns = [
    re_path(r'^(?P<path>.*)$', views.serve_docs, name="serve_docs"),
]
