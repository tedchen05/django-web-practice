from django.contrib import admin

from webapp.models import Product, Navigation, OrderProduct

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description','price')
    list_filter = ('name','description')
    search_fields = ('name','description')
    ordering = ('id',)

class NavigationAdmin(admin.ModelAdmin):
    list_display = ('id', 'order','title', 'url', 'parent_id')
    list_filter = ('order','title')
    search_fields = ('title','url')
    ordering = ('id',)

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'product_name','quantity','price', 'total_price', 'ordered_at')
    list_filter = ('customer', 'product_name')
    search_fields = ('customer', 'product_name')
    ordering = ('id',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Navigation,NavigationAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)