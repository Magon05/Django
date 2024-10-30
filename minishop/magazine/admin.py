from django.contrib import admin
from .models import *


class goodsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'regular_price', 'discounted_price', 'stock_quantity', 'product_details', 'category', 'sub_category', 'created']
    list_display_links = ['product_name']
    search_fields = ['product_name', 'product_details']


class categoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    list_display_links = ['category_name']
    search_fields = ['category_name']


class subcategoryAdmin(admin.ModelAdmin):
    list_display = ['subcategory_name', 'category_name']
    list_display_links = ['subcategory_name']
    search_fields = ['subcategory_name']


admin.site.register(goods, goodsAdmin)
admin.site.register(product_category, categoryAdmin)
admin.site.register(product_subcategory, subcategoryAdmin)