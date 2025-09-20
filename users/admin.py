from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import (
    User,
    UserProfile,
    UserAddress,
    UserPreference,
    UserBusinessData,
    UserActivityLog,
    UserBehaviorAnalytics,
    LoginHistory,
    KeycloakUserSync,
)

@admin.register(User)
class CustomUserAdmin(DjangoUserAdmin):
    fieldsets = (*DjangoUserAdmin.fieldsets, ('Custom Fields', {'fields': ('is_seller', 'is_admin', 'phone')}))
    add_fieldsets = (*DjangoUserAdmin.add_fieldsets, ('Custom Fields', {'fields': ('is_seller', 'is_admin', 'phone')}))
    list_display = ('id', 'username', 'email', 'is_staff', 'is_seller', 'is_admin')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_seller', 'is_admin')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'keycloak_user_id', 'status')
    search_fields = ('keycloak_user_id', 'user__email', 'user__username')
    list_filter = ('status',)

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address_type', 'city', 'country')
    search_fields = ('user__email', 'user__username', 'city', 'country')
    list_filter = ('address_type', 'country')

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'currency', 'timezone')
    search_fields = ('user__email', 'user__username')

@admin.register(UserBusinessData)
class UserBusinessDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'kyc_status', 'business_type')
    search_fields = ('user__email', 'user__username', 'tax_id')
    list_filter = ('kyc_status', 'business_type')

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_type', 'created_at')
    search_fields = ('user__email', 'user__username', 'activity_type')
    list_filter = ('activity_type',)
    date_hierarchy = 'created_at'

@admin.register(UserBehaviorAnalytics)
class UserBehaviorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'pages_viewed', 'time_spent_minutes')
    search_fields = ('user__email', 'user__username')
    date_hierarchy = 'date'

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ip_address', 'success', 'attempted_at')
    search_fields = ('user__email', 'user__username', 'ip_address')
    list_filter = ('success',)
    date_hierarchy = 'attempted_at'

@admin.register(KeycloakUserSync)
class KeycloakUserSyncAdmin(admin.ModelAdmin):
    list_display = ('user', 'keycloak_user_id', 'last_sync_at', 'sync_status')
    search_fields = ('user__email', 'user__username', 'keycloak_user_id')
    list_filter = ('sync_status',)
    date_hierarchy = 'last_sync_at'
