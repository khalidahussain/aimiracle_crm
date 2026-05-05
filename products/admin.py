from django.contrib import admin
from django.utils.html import format_html

from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px;" />',
                obj.image.url
            )
        return "No Image"

    image_tag.short_description = 'Image'


admin.site.register(Product, ProductAdmin)