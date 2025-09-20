from django.contrib import admin
from .models import (
    Shop,
    ShopCategory,
    ShopCategoryAssignment,
    ShopPolicy,
    ShopPerformance,
    ShopReview,
    ShopSetting,
    ShopStaff,
    ShopStatistics,
    ShopUserRole,
)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'status', 'city', 'country', 'created_at')
    list_filter = ('status', 'country', 'state', 'shop_type')
    search_fields = ('name', 'owner__username', 'email', 'phone')
    raw_id_fields = ('owner',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'approval_date')

@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'commission_rate_override', 'created_at')
    search_fields = ('name',)

@admin.register(ShopCategoryAssignment)
class ShopCategoryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'category', 'assigned_at')
    raw_id_fields = ('shop', 'category')
    date_hierarchy = 'assigned_at'

@admin.register(ShopPolicy)
class ShopPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'updated_at')
    raw_id_fields = ('shop',)
    search_fields = ('shop__name',)

@admin.register(ShopPerformance)
class ShopPerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'date', 'revenue', 'orders_count', 'average_rating')
    raw_id_fields = ('shop',)
    list_filter = ('date',)
    date_hierarchy = 'date'
    search_fields = ('shop__name',)

@admin.register(ShopReview)
class ShopReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'customer', 'order', 'rating', 'status', 'created_at')
    list_filter = ('status', 'rating')
    raw_id_fields = ('shop', 'customer', 'order')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'review_text', 'shop__name', 'customer__username')

@admin.register(ShopSetting)
class ShopSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'key', 'value', 'type')
    list_filter = ('type',)
    raw_id_fields = ('shop',)
    search_fields = ('key', 'value', 'shop__name')

@admin.register(ShopStaff)
class ShopStaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'user', 'role', 'status', 'hired_at')
    list_filter = ('role', 'status')
    raw_id_fields = ('shop', 'user')
    search_fields = ('shop__name', 'user__username')
    date_hierarchy = 'hired_at'

@admin.register(ShopStatistics)
class ShopStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'total_revenue', 'total_orders', 'average_rating', 'last_calculated_at')
    raw_id_fields = ('shop',)
    search_fields = ('shop__name',)

@admin.register(ShopUserRole)
class ShopUserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'user', 'role_name', 'is_active')
    list_filter = ('is_active', 'role_name')
    search_fields = ('shop__name', 'user__username', 'role_name')
