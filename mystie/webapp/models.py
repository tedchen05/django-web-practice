from django.contrib.auth.models import User
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

class OrderProduct(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="訂購人")
    product_name = models.CharField(max_length=100, verbose_name="產品名稱")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金額")
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="訂購時間")

    def __str__(self):
        return f"{self.customer.username} ordered {self.product_name} x{self.quantity}"