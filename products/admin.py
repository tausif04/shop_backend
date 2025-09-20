from django.contrib import admin
from .models import (
    Product,
    Category,
    ProductVariant,
    ProductImage,
    ProductAttribute,
    ProductAttributeValue,
    ProductInventory,
    ProductAnalytics,
    ProductReviewsSummary,
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shop', 'category', 'status', 'created_at')
    list_filter = ('status', 'shop', 'category')
    search_fields = ('name', 'shop__name', 'sku')
    raw_id_fields = ('shop', 'category')
    date_hierarchy = 'created_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    raw_id_fields = ('parent',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'sku', 'price', 'is_default')
    search_fields = ('sku', 'name', 'product__name')
    raw_id_fields = ('product',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'variant', 'is_primary', 'sort_order')
    list_filter = ('is_primary',)
    search_fields = ('alt_text', 'product__name')
    raw_id_fields = ('product', 'variant')

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'is_required')
    search_fields = ('name',)

@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'attribute', 'value')
    raw_id_fields = ('product', 'attribute')

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'variant', 'quantity_available', 'quantity_reserved')
    raw_id_fields = ('variant',)

@admin.register(ProductAnalytics)
class ProductAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'date', 'views', 'clicks', 'purchases')
    raw_id_fields = ('product',)

@admin.register(ProductReviewsSummary)
class ProductReviewsSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'average_rating', 'total_reviews')
    raw_id_fields = ('product',)
