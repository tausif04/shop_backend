from django.db import models



class OrderAddresses(models.Model):
    address_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
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
        managed = False
        db_table = 'order_addresses'
        unique_together = (('order', 'address_type'),)


class OrderItems(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    variant = models.ForeignKey('ProductVariants', models.DO_NOTHING)
    shop = models.ForeignKey('Shops', models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=9)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_items'


class OrderPayments(models.Model):
    payment_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=9)
    gateway_response_json = models.JSONField(blank=True, null=True)
    processed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_payments'


class OrderRefunds(models.Model):
    refund_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    item = models.ForeignKey(OrderItems, models.DO_NOTHING, blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9)
    processed_by = models.CharField(max_length=255, blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_refunds'


class OrderStatusHistory(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    status = models.CharField(max_length=50)
    changed_by = models.CharField(max_length=255, blank=True, null=True)
    changed_at = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    notification_sent = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_status_history'


class OrderTracking(models.Model):
    tracking_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.CharField(max_length=2048, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    estimated_delivery = models.DateField(blank=True, null=True)
    last_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_tracking'
        unique_together = (('order', 'tracking_number'),)


class Orders(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('UserProfiles', models.DO_NOTHING, to_field='keycloak_user_id')
    order_number = models.CharField(unique=True, max_length=50)
    status = models.CharField(max_length=10)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    order_date = models.DateTimeField()
    shipped_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class OrdersOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    product = models.ForeignKey('ProductsProduct', models.DO_NOTHING)
    user = models.ForeignKey('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'orders_order'

