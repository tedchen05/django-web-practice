from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Navigation(models.Model):
    title = models.CharField(max_length=100, verbose_name="名稱")  # 顯示文字
    url = models.CharField(max_length=200, blank=True, verbose_name="連結")  # 對應連結
    order = models.PositiveIntegerField(default=0, verbose_name="排序")
    parent_id = models.PositiveIntegerField(default=0, verbose_name="父節點ID")

    def __str__(self):
        return self.title