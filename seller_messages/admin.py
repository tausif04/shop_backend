from django.contrib import admin
from .models import SellerMessagesSellermessage

@admin.register(SellerMessagesSellermessage)
class SellerMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'created_at')
    raw_id_fields = ('sender', 'receiver')
    search_fields = ('sender__username', 'receiver__username', 'message')
    date_hierarchy = 'created_at'
