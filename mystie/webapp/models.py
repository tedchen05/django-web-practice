from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="產品名稱")
    description = models.TextField(blank=True, verbose_name="產品簡介")
    price = models.IntegerField(verbose_name="價格(元)")
    image_url = models.URLField(blank=True,default='',verbose_name="圖片網址")

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Navigation(models.Model):
    title = models.CharField(max_length=100)  # 顯示文字
    url = models.CharField(max_length=200, blank=True)  # 對應連結

    def __str__(self):
        return self.title