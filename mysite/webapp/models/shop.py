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

class OrderProduct(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="訂購人")
    product_name = models.CharField(max_length=100, verbose_name="產品名稱")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")
    price = models.IntegerField(default=0, verbose_name="單一價格(元)")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="單品總價")
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="訂購時間")

    def __str__(self):
        return f"{self.customer.username} ordered {self.product_name} x{self.quantity}"