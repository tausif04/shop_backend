from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import UsersUser, UserProfiles # Import the correct model
# Register the main custom user model

@admin.register(UsersUser)
class CustomUserAdmin(DjangoUserAdmin):
    """
    Admin configuration for the primary User model (UsersUser).
    It inherits from Django's UserAdmin to get all the default user management features.
    """
    # Add your custom fields to the display and editing forms
    fieldsets = (*DjangoUserAdmin.fieldsets, ('Custom Fields', {'fields': ('is_seller', 'is_admin', 'phone')}))
    add_fieldsets = (*DjangoUserAdmin.add_fieldsets, ('Custom Fields', {'fields': ('is_seller', 'is_admin', 'phone')}))
    list_display = ('id', 'username', 'email', 'is_staff', 'is_seller', 'is_admin')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_seller', 'is_admin')

# Optionally, register the UserProfiles model to make it visible in the admin
@admin.register(UserProfiles)
class UserProfilesAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserProfiles model.
    """
    list_display = ('profile_id', 'keycloak_user_id', 'email', 'first_name', 'last_name', 'status')
    search_fields = ('keycloak_user_id', 'email', 'first_name', 'last_name')
    list_filter = ('status',)

# You can continue to register your other models here if you wish
# from .models import UserAddresses, UserPreferences, etc.
# admin.site.register(UserAddresses)
# admin.site.register(UserPreferences)
