# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    # 年齢を追加したい場合
    age = models.IntegerField('年齢', blank=True, null=True)
    weight = models.IntegerField('体重', blank=True, null=True)
