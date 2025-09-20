from django.contrib import admin
from .models import ReportsReport

@admin.register(ReportsReport)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'status', 'created_at')
    list_filter = ('status', 'type')
    search_fields = ('details', 'user__username')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
