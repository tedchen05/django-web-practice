from django.contrib import admin

from webapp.models import Product, Navigation


# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description','price')
    list_filter = ('name','description')
    search_fields = ('name','description')
    ordering = ('id',)

class NavigationAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'url')
    list_filter = ('title','url')
    search_fields = ('title','url')
    ordering = ('id',)

admin.site.register(Product, productAdmin)
admin.site.register(Navigation,NavigationAdmin)