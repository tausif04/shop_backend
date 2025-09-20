from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'users_user'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    keycloak_user_id = models.CharField(unique=True, max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=17, blank=True, null=True)
    avatar_url = models.CharField(max_length=2048, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sync_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_profiles'

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=8)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_addresses'

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)
    notification_push = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    currency = models.CharField(max_length=10, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    theme = models.CharField(max_length=5, default='light')
    marketing_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_preferences'

class UserBusinessData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kyc_status = models.CharField(max_length=17)
    kyc_documents_json = models.JSONField(blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    business_license = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    verification_notes = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user_business_data'

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    activity_type = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=100, blank=True, null=True)
    resource_id = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activity_log'

class UserBehaviorAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    pages_viewed = models.PositiveIntegerField()
    time_spent_minutes = models.PositiveIntegerField()
    products_viewed = models.PositiveIntegerField()
    searches_made = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_behavior_analytics'
        unique_together = (('user', 'date'),)

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    location_json = models.JSONField(blank=True, null=True)
    login_method = models.CharField(max_length=50, blank=True, null=True)
    success = models.BooleanField()
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'login_history'

class KeycloakUserSync(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    keycloak_user_id = models.CharField(max_length=255, unique=True)
    last_sync_at = models.DateTimeField()
    sync_status = models.CharField(max_length=7)
    error_message = models.TextField(blank=True, null=True)
    attributes_synced_json = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'keycloak_user_sync'
