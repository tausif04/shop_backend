from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=2048, blank=True, null=True)
    commission_rate_override = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sort_order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'categories'

class Product(models.Model):
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default='')
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=512, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=8)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        unique_together = (('shop', 'sku'), ('shop', 'slug'),)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dimensions_json = models.JSONField(blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_variants'
        unique_together = (('product', 'sku'),)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, blank=True, null=True)
    image_url = models.CharField(max_length=2048)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'

class ProductAttribute(models.Model):
    name = models.CharField(unique=True, max_length=100)
    type = models.CharField(max_length=7)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_attributes'

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_attribute_values'
        unique_together = (('product', 'attribute'),)

class ProductInventory(models.Model):
    variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE)
    quantity_available = models.IntegerField()
    quantity_reserved = models.IntegerField()
    reorder_level = models.IntegerField(blank=True, null=True)
    supplier_info_json = models.JSONField(blank=True, null=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_inventory'

class ProductAnalytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    add_to_cart = models.PositiveIntegerField()
    purchases = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_analytics'
        unique_together = (('product', 'date'),)

class ProductReviewsSummary(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_reviews = models.PositiveIntegerField()
    rating_distribution_json = models.JSONField(blank=True, null=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_reviews_summary'
