# chat\routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer)
]

# ここでre_pathを使う理由がよくわからない
# (Note we use re_path() due to limitations in URLRouter.)
# https://channels.readthedocs.io/en/latest/topics/routing.html#urlrouter
