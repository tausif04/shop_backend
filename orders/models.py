from django.db import models
from django.utils import timezone
from users.models import User
from products.models import Product, ProductVariant
from shop.models import Shop

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_number = models.CharField(unique=True, max_length=50, default='')
    status = models.CharField(max_length=10)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    order_date = models.DateTimeField(default=timezone.now)
    shipped_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'

class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=8)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'order_addresses'
        unique_together = (('order', 'address_type'),)

class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=9)
    gateway_response_json = models.JSONField(blank=True, null=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_payments'

class OrderRefund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_refunds')
    processed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'order_refunds'

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    notification_sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_status_history'

class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.CharField(max_length=2048, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    estimated_delivery = models.DateField(blank=True, null=True)
    last_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'order_tracking'
        unique_together = (('order', 'tracking_number'),)
