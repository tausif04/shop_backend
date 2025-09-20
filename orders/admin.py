from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    OrderAddress,
    OrderPayment,
    OrderRefund,
    OrderStatusHistory,
    OrderTracking,
)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'customer', 'status', 'total_amount', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer__username')
    raw_id_fields = ('customer',)
    date_hierarchy = 'order_date'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'variant', 'shop', 'quantity', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('order__order_number', 'product__name', 'shop__name')
    raw_id_fields = ('order', 'product', 'variant', 'shop')

@admin.register(OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'address_type', 'city', 'country', 'postal_code')
    list_filter = ('address_type', 'country')
    search_fields = ('order__order_number', 'city', 'postal_code')
    raw_id_fields = ('order',)

@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'transaction_id', 'amount', 'status', 'processed_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'order__order_number')
    raw_id_fields = ('order',)
    date_hierarchy = 'processed_at'

@admin.register(OrderRefund)
class OrderRefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item', 'refund_amount', 'status', 'processed_at')
    list_filter = ('status',)
    search_fields = ('order__order_number', 'item__id')
    raw_id_fields = ('order', 'item')

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status', 'changed_by', 'changed_at')
    list_filter = ('status',)
    search_fields = ('order__order_number',)
    raw_id_fields = ('order',)
    date_hierarchy = 'changed_at'

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'carrier', 'tracking_number', 'status')
    list_filter = ('carrier', 'status')
    search_fields = ('tracking_number', 'order__order_number')
    raw_id_fields = ('order',)
