from django.db import models
from users.models import User, UserProfile

class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255, default='')
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_url = models.CharField(max_length=2048, blank=True, null=True)
    banner_url = models.CharField(max_length=2048, blank=True, null=True)
    status = models.CharField(max_length=9)
    approval_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    minimum_payout_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shop_type = models.CharField(max_length=100, blank=True, null=True)
    business_license = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shops'

class ShopCategory(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    commission_rate_override = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shop_categories'

class ShopCategoryAssignment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shop_category_assignments'
        unique_together = (('shop', 'category'),)

class ShopPolicy(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    return_policy = models.TextField(blank=True, null=True)
    shipping_policy = models.TextField(blank=True, null=True)
    privacy_policy = models.TextField(blank=True, null=True)
    terms_of_service = models.TextField(blank=True, null=True)
    refund_policy = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_policies'

class ShopPerformance(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    date = models.DateField()
    orders_count = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    commission_paid = models.DecimalField(max_digits=15, decimal_places=2)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    response_time_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shop_performance'
        unique_together = (('shop', 'date'),)

class ShopReview(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shop_reviews'
        unique_together = (('shop', 'customer', 'order'),)

class ShopSetting(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.TextField()
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop_settings'
        unique_together = (('shop', 'key'),)

class ShopStaff(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=7)
    permissions_json = models.JSONField(blank=True, null=True)
    hired_at = models.DateTimeField()
    status = models.CharField(max_length=8)

    class Meta:
        db_table = 'shop_staff'
        unique_together = (('shop', 'user'),)

class ShopStatistics(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField()
    total_orders = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_reviews = models.PositiveIntegerField()
    last_calculated_at = models.DateTimeField()

    class Meta:
        db_table = 'shop_statistics'

class ShopUserRole(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=100)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_roles')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'shop_user_roles'
        unique_together = (('shop', 'user', 'role_name'),)
