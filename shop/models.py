from django.db import models
from users.models import UserProfiles, UsersUser


class Shops(models.Model):
    shop_id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    shop_name = models.CharField(max_length=255)
    shop_slug = models.CharField(unique=True, max_length=255)
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
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_payout_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shop_type = models.CharField(max_length=100, blank=True, null=True)
    business_license = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shops'


class ShopCategories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    commission_rate_override = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_categories'


class ShopCategoryAssignments(models.Model):
    assignment_id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shops, models.DO_NOTHING)
    category = models.ForeignKey(ShopCategories, models.DO_NOTHING)
    assigned_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_category_assignments'
        unique_together = (('shop', 'category'),)


class ShopPolicies(models.Model):
    policy_id = models.BigAutoField(primary_key=True)
    shop = models.OneToOneField(Shops, models.DO_NOTHING)
    return_policy = models.TextField(blank=True, null=True)
    shipping_policy = models.TextField(blank=True, null=True)
    privacy_policy = models.TextField(blank=True, null=True)
    terms_of_service = models.TextField(blank=True, null=True)
    refund_policy = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_policies'


class ShopPerformance(models.Model):
    performance_id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shops, models.DO_NOTHING)
    date = models.DateField()
    orders_count = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    commission_paid = models.DecimalField(max_digits=15, decimal_places=2)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    response_time_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_performance'
        unique_together = (('shop', 'date'),)


class ShopReviews(models.Model):
    shop_review_id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shops, models.DO_NOTHING)
    customer = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    order = models.ForeignKey('orders.Orders', models.DO_NOTHING)
    rating = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_reviews'
        unique_together = (('shop', 'customer', 'order'),)


class ShopSettings(models.Model):
    setting_id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shops, models.DO_NOTHING)
    setting_key = models.CharField(max_length=100)
    setting_value = models.TextField()
    setting_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_settings'
        unique_together = (('shop', 'setting_key'),)


class ShopStaff(models.Model):
    staff_id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey(Shops, models.DO_NOTHING)
    user = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    role = models.CharField(max_length=7)
    permissions_json = models.JSONField(blank=True, null=True)
    hired_at = models.DateTimeField()
    status = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'shop_staff'
        unique_together = (('shop', 'user'),)


class ShopStatistics(models.Model):
    stat_id = models.BigAutoField(primary_key=True)
    shop = models.OneToOneField(Shops, models.DO_NOTHING)
    total_products = models.PositiveIntegerField()
    total_orders = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_reviews = models.PositiveIntegerField()
    last_calculated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_statistics'


class ShopUserRoles(models.Model):
    role_assignment_id = models.BigAutoField(primary_key=True)
    shop_id = models.PositiveBigIntegerField()
    keycloak_user_id = models.CharField(max_length=255)
    keycloak_role_name = models.CharField(max_length=100)
    assigned_at = models.DateTimeField()
    assigned_by = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shop_user_roles'
        unique_together = (('shop_id', 'keycloak_user_id', 'keycloak_role_name'),)


# Legacy/alternate shop tables (keep only if still in DB)
class ShopShop(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.ForeignKey(UsersUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_shop'


class ShopShopattachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField()
    shop = models.ForeignKey(ShopShop, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_shopattachment'


class ShopShopdocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    doc_type = models.CharField(max_length=32)
    number = models.CharField(max_length=128)
    file = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()
    shop = models.ForeignKey(ShopShop, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_shopdocument'
