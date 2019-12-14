from django.db import models

# Create your models here.


class List(models.Model):

    # item名
    item = models.CharField(
        max_length=200,
        )

    # 完了かどうか
    completed = models.BooleanField(
        default=False
        )

    def __str__(self):
        return self.item + '|' + str(self.completed)
