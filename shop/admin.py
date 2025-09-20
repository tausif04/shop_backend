# admin.py

from django.contrib import admin
from .models import (
    Shops,
    ShopCategories,
    ShopCategoryAssignments,
    ShopPolicies,
    ShopPerformance,
    ShopReviews,
    ShopSettings,
    ShopStaff,
    ShopStatistics,
    ShopUserRoles,
    ShopShop,
    ShopShopattachment,
    ShopShopdocument,
)

@admin.register(Shops)
class ShopsAdmin(admin.ModelAdmin):
    """Admin configuration for the main Shops model."""
    list_display = ('shop_id', 'shop_name', 'owner', 'status', 'city', 'country', 'created_at')
    list_filter = ('status', 'country', 'state', 'shop_type')
    search_fields = ('shop_name', 'owner__keycloak_user_id', 'email', 'phone')
    raw_id_fields = ('owner',) # Better for performance with many users
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'approval_date')

@admin.register(ShopCategories)
class ShopCategoriesAdmin(admin.ModelAdmin):
    """Admin configuration for Shop Categories."""
    list_display = ('category_id', 'category_name', 'commission_rate_override', 'created_at')
    search_fields = ('category_name',)

@admin.register(ShopCategoryAssignments)
class ShopCategoryAssignmentsAdmin(admin.ModelAdmin):
    """Admin for the link between Shops and Categories."""
    list_display = ('assignment_id', 'shop', 'category', 'assigned_at')
    raw_id_fields = ('shop', 'category')
    date_hierarchy = 'assigned_at'

@admin.register(ShopPolicies)
class ShopPoliciesAdmin(admin.ModelAdmin):
    """Admin for Shop Policies (One-to-One with Shop)."""
    list_display = ('policy_id', 'shop', 'updated_at')
    raw_id_fields = ('shop',)
    search_fields = ('shop__shop_name',)

@admin.register(ShopPerformance)
class ShopPerformanceAdmin(admin.ModelAdmin):
    """Admin for tracking daily shop performance."""
    list_display = ('performance_id', 'shop', 'date', 'revenue', 'orders_count', 'average_rating')
    raw_id_fields = ('shop',)
    list_filter = ('date',)
    date_hierarchy = 'date'
    search_fields = ('shop__shop_name',)

@admin.register(ShopReviews)
class ShopReviewsAdmin(admin.ModelAdmin):
    """Admin for customer reviews of shops."""
    list_display = ('shop_review_id', 'shop', 'customer', 'order', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating')
    raw_id_fields = ('shop', 'customer', 'order')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'review_text', 'shop__shop_name', 'customer__keycloak_user_id')

@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    """Admin for key-value shop settings."""
    list_display = ('setting_id', 'shop', 'setting_key', 'setting_value', 'setting_type')
    list_filter = ('setting_type',)
    raw_id_fields = ('shop',)
    search_fields = ('setting_key', 'setting_value', 'shop__shop_name')

@admin.register(ShopStaff)
class ShopStaffAdmin(admin.ModelAdmin):
    """Admin for managing staff members of a shop."""
    list_display = ('staff_id', 'shop', 'user', 'role', 'status', 'hired_at')
    list_filter = ('role', 'status')
    raw_id_fields = ('shop', 'user')
    search_fields = ('shop__shop_name', 'user__keycloak_user_id')
    date_hierarchy = 'hired_at'

@admin.register(ShopStatistics)
class ShopStatisticsAdmin(admin.ModelAdmin):
    """Admin for viewing shop statistics (One-to-One with Shop)."""
    list_display = ('stat_id', 'shop', 'total_revenue', 'total_orders', 'average_rating', 'last_calculated_at')
    raw_id_fields = ('shop',)
    search_fields = ('shop__shop_name',)

@admin.register(ShopUserRoles)
class ShopUserRolesAdmin(admin.ModelAdmin):
    """Admin for viewing keycloak user roles related to shops."""
    list_display = ('role_assignment_id', 'shop_id', 'keycloak_user_id', 'keycloak_role_name', 'is_active')
    list_filter = ('is_active', 'keycloak_role_name')
    search_fields = ('shop_id', 'keycloak_user_id', 'keycloak_role_name')

# --- Legacy/Alternate Shop Tables ---

@admin.register(ShopShop)
class ShopShopAdmin(admin.ModelAdmin):
    """Admin for the legacy 'shop_shop' table."""
    list_display = ('id', 'name', 'owner', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'owner__username') # Assuming UsersUser has a username
    raw_id_fields = ('owner',)
    date_hierarchy = 'created_at'

@admin.register(ShopShopattachment)
class ShopShopattachmentAdmin(admin.ModelAdmin):
    """Admin for the legacy 'shop_shopattachment' table."""
    list_display = ('id', 'shop', 'name', 'uploaded_at')
    search_fields = ('name', 'shop__name')
    raw_id_fields = ('shop',)
    date_hierarchy = 'uploaded_at'

@admin.register(ShopShopdocument)
class ShopShopdocumentAdmin(admin.ModelAdmin):
    """Admin for the legacy 'shop_shopdocument' table."""
    list_display = ('id', 'shop', 'doc_type', 'number', 'uploaded_at')
    list_filter = ('doc_type',)
    search_fields = ('number', 'shop__name')
    raw_id_fields = ('shop',)
    date_hierarchy = 'uploaded_at'