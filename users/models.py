from django.db import models
from django.contrib.auth.models import AbstractUser



from django.db import models


class UsersUser( AbstractUser):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    is_seller = models.IntegerField()
    is_admin = models.IntegerField()
    phone = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users_user'


class UsersUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    group = models.ForeignKey('auth.Group', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_groups'
        unique_together = (('user', 'group'),)


class UsersUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    permission = models.ForeignKey('auth.Permission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_user_permissions'
        unique_together = (('user', 'permission'),)


class UserProfiles(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    keycloak_user_id = models.CharField(unique=True, max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=17, blank=True, null=True)
    avatar_url = models.CharField(max_length=2048, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    last_sync_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profiles'


class UserAddresses(models.Model):
    address_id = models.BigAutoField(primary_key=True)
    keycloak_user = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    address_type = models.CharField(max_length=8)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_addresses'


class UserPreferences(models.Model):
    preference_id = models.BigAutoField(primary_key=True)
    keycloak_user = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    notification_email = models.IntegerField()
    notification_sms = models.IntegerField()
    notification_push = models.IntegerField()
    language = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    timezone = models.CharField(max_length=50)
    theme = models.CharField(max_length=5)
    marketing_consent = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_preferences'


class UserBusinessData(models.Model):
    business_id = models.BigAutoField(primary_key=True)
    keycloak_user = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    kyc_status = models.CharField(max_length=17)
    kyc_documents_json = models.JSONField(blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    business_license = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    verification_notes = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_business_data'


class UserActivityLog(models.Model):
    activity_id = models.BigAutoField(primary_key=True)
    keycloak_user_id = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=100, blank=True, null=True)
    resource_id = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_activity_log'


class UserBehaviorAnalytics(models.Model):
    behavior_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    date = models.DateField()
    pages_viewed = models.PositiveIntegerField()
    time_spent_minutes = models.PositiveIntegerField()
    products_viewed = models.PositiveIntegerField()
    searches_made = models.PositiveIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_behavior_analytics'
        unique_together = (('user', 'date'),)


class LoginHistory(models.Model):
    login_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserProfiles, models.DO_NOTHING, to_field='keycloak_user_id')
    ip_address = models.CharField(max_length=45)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    location_json = models.JSONField(blank=True, null=True)
    login_method = models.CharField(max_length=50, blank=True, null=True)
    success = models.IntegerField()
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    attempted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'login_history'


class KeycloakUserSync(models.Model):
    sync_id = models.BigAutoField(primary_key=True)
    keycloak_user_id = models.CharField(max_length=255)
    last_sync_at = models.DateTimeField()
    sync_status = models.CharField(max_length=7)
    error_message = models.TextField(blank=True, null=True)
    attributes_synced_json = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keycloak_user_sync'
