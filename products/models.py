from django.db import models



class RatingSummaries(models.Model):
    summary_id = models.BigAutoField(primary_key=True)
    product_id = models.PositiveBigIntegerField(unique=True, blank=True, null=True)
    shop_id = models.PositiveBigIntegerField(unique=True, blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_reviews = models.PositiveIntegerField()
    rating_1_count = models.PositiveIntegerField()
    rating_2_count = models.PositiveIntegerField()
    rating_3_count = models.PositiveIntegerField()
    rating_4_count = models.PositiveIntegerField()
    rating_5_count = models.PositiveIntegerField()
    last_updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rating_summaries'

class CustomReports(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    report_name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=100)
    filters_json = models.JSONField()
    created_by = models.ForeignKey('UserProfiles', models.DO_NOTHING, db_column='created_by', to_field='keycloak_user_id')
    created_at = models.DateTimeField()
    last_run_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'custom_reports'

class ReportSchedules(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    report = models.ForeignKey(CustomReports, models.DO_NOTHING)
    frequency = models.CharField(max_length=7)
    recipients_json = models.JSONField()
    next_run_at = models.DateTimeField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'report_schedules'


class ReportsReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=100)
    details = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reports_report'


class ReviewImages(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    review = models.ForeignKey('Reviews', models.DO_NOTHING)
    image_url = models.CharField(max_length=2048)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review_images'


class ReviewModeration(models.Model):
    moderation_id = models.BigAutoField(primary_key=True)
    review = models.ForeignKey('Reviews', models.DO_NOTHING)
    moderator = models.ForeignKey('UserProfiles', models.DO_NOTHING, to_field='keycloak_user_id')
    action = models.CharField(max_length=7)
    reason = models.TextField(blank=True, null=True)
    moderated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review_moderation'


class ReviewResponses(models.Model):
    response_id = models.BigAutoField(primary_key=True)
    review = models.OneToOneField('Reviews', models.DO_NOTHING)
    responder = models.ForeignKey('UserProfiles', models.DO_NOTHING, to_field='keycloak_user_id')
    response_text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review_responses'


class ReviewVotes(models.Model):
    vote_id = models.BigAutoField(primary_key=True)
    review = models.ForeignKey('Reviews', models.DO_NOTHING)
    user = models.ForeignKey('UserProfiles', models.DO_NOTHING, to_field='keycloak_user_id')
    vote_type = models.CharField(max_length=11)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review_votes'
        unique_together = (('review', 'user'),)


class Reviews(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("Products", models.DO_NOTHING)
    order_item = models.OneToOneField("OrderItems", models.DO_NOTHING)
    customer = models.ForeignKey('UserProfiles', models.DO_NOTHING, to_field='keycloak_user_id')
    shop = models.ForeignKey('Shops', models.DO_NOTHING)
    rating = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    is_verified_purchase = models.IntegerField()
    status = models.CharField(max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'


class ProductAnalytics(models.Model):
    analytics_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    date = models.DateField()
    views = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    add_to_cart = models.PositiveIntegerField()
    purchases = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_analytics'
        unique_together = (('product', 'date'),)


class ProductAttributeValues(models.Model):
    value_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    attribute = models.ForeignKey('ProductAttributes', models.DO_NOTHING)
    attribute_value = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_attribute_values'
        unique_together = (('product', 'attribute'),)


class ProductAttributes(models.Model):
    attribute_id = models.BigAutoField(primary_key=True)
    attribute_name = models.CharField(unique=True, max_length=100)
    attribute_type = models.CharField(max_length=7)
    is_required = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_attributes'


class ProductImages(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    variant = models.ForeignKey('ProductVariants', models.DO_NOTHING, blank=True, null=True)
    image_url = models.CharField(max_length=2048)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()
    is_primary = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_images'


class ProductInventory(models.Model):
    inventory_id = models.BigAutoField(primary_key=True)
    variant = models.OneToOneField('ProductVariants', models.DO_NOTHING)
    quantity_available = models.IntegerField()
    quantity_reserved = models.IntegerField()
    reorder_level = models.IntegerField(blank=True, null=True)
    supplier_info_json = models.JSONField(blank=True, null=True)
    last_updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_inventory'


class ProductReviewsSummary(models.Model):
    summary_id = models.BigAutoField(primary_key=True)
    product = models.OneToOneField('Products', models.DO_NOTHING)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_reviews = models.PositiveIntegerField()
    rating_distribution_json = models.JSONField(blank=True, null=True)
    last_updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_reviews_summary'


class ProductVariants(models.Model):
    variant_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    variant_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dimensions_json = models.JSONField(blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_variants'
        unique_together = (('product', 'sku'),)


class Categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    parent_category = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    category_name = models.CharField(max_length=255)
    category_slug = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=2048, blank=True, null=True)
    commission_rate_override = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sort_order = models.IntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'categories'

class Products(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey('Shops', models.DO_NOTHING)
    category = models.ForeignKey(Categories, models.DO_NOTHING)
    product_name = models.CharField(max_length=255)
    product_slug = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=512, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=8)
    featured = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'products'
        unique_together = (('shop', 'sku'), ('shop', 'product_slug'),)


class ProductsProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    shop = models.ForeignKey('ShopShop', models.DO_NOTHING)
    category = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'products_product'


class Categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    parent_category = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    category_name = models.CharField(max_length=255)
    category_slug = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=2048, blank=True, null=True)
    commission_rate_override = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sort_order = models.IntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'categories'