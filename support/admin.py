from django.contrib import admin
from .models import SupportSupportticket

@admin.register(SupportSupportticket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'status', 'created_at')
    search_fields = ('subject', 'user__username')
    list_filter = ('status',)
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
