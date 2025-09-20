from django.contrib import admin
from .models import Products, Categories, ProductVariants, ProductImages

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'shop', 'category', 'status', 'created_at')
    list_filter = ('status', 'shop', 'category')
    search_fields = ('product_name', 'shop__shop_name', 'sku')
    raw_id_fields = ('shop', 'category')
    date_hierarchy = 'created_at'

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'parent_category', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('category_name',)
    raw_id_fields = ('parent_category',)

@admin.register(ProductVariants)
class ProductVariantsAdmin(admin.ModelAdmin):
    list_display = ('variant_id', 'product', 'variant_name', 'sku', 'price', 'is_default')
    search_fields = ('sku', 'variant_name', 'product__product_name')
    raw_id_fields = ('product',)

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'product', 'variant', 'is_primary', 'sort_order')
    list_filter = ('is_primary',)
    search_fields = ('alt_text', 'product__product_name')
    raw_id_fields = ('product', 'variant')

# Register other product-related models if needed
# from .models import ProductAnalytics, ProductInventory, Reviews, etc.
# admin.site.register(ProductAnalytics)
# admin.site.register(ProductInventory)
# admin.site.register(Reviews)