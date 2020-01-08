# config/routers.py

from rest_framework import routers
from article.views import ArticleViewSet

router = routers.DefaultRouter()

router.register(r'article', ArticleViewSet)
