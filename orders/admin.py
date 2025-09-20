from django.contrib import admin
from .models import (
    Orders,
    OrderItems,
    OrderAddresses,
    OrderPayments,
    OrderRefunds,
    OrderStatusHistory,
    OrderTracking,
    OrdersOrder # Legacy order table
)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_number', 'customer', 'status', 'total_amount', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer__keycloak_user_id')
    raw_id_fields = ('customer',)
    date_hierarchy = 'order_date'

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'order', 'product', 'variant', 'shop', 'quantity', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('order__order_number', 'product__product_name', 'shop__shop_name')
    raw_id_fields = ('order', 'product', 'variant', 'shop')

@admin.register(OrderAddresses)
class OrderAddressesAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'order', 'address_type', 'city', 'country', 'postal_code')
    list_filter = ('address_type', 'country')
    search_fields = ('order__order_number', 'city', 'postal_code')
    raw_id_fields = ('order',)

@admin.register(OrderPayments)
class OrderPaymentsAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'transaction_id', 'amount', 'status', 'processed_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'order__order_number')
    raw_id_fields = ('order',)
    date_hierarchy = 'processed_at'

@admin.register(OrderRefunds)
class OrderRefundsAdmin(admin.ModelAdmin):
    list_display = ('refund_id', 'order', 'item', 'refund_amount', 'status', 'processed_at')
    list_filter = ('status',)
    search_fields = ('order__order_number', 'item__item_id')
    raw_id_fields = ('order', 'item')

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'order', 'status', 'changed_by', 'changed_at')
    list_filter = ('status',)
    search_fields = ('order__order_number',)
    raw_id_fields = ('order',)
    date_hierarchy = 'changed_at'

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'order', 'carrier', 'tracking_number', 'status')
    list_filter = ('carrier', 'status')
    search_fields = ('tracking_number', 'order__order_number')
    raw_id_fields = ('order',)

@admin.register(OrdersOrder)
class OrdersOrderAdmin(admin.ModelAdmin):
    # Admin for the legacy 'orders_order' table
    list_display = ('id', 'user', 'product', 'status', 'quantity', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'product__name')
    raw_id_fields = ('user', 'product')
    date_hierarchy = 'created_at'