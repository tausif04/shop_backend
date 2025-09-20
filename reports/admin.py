from django.contrib import admin
from .models import (
    Report,
    CustomReport,
    ComplianceReport,
    DailySalesReport,
    FinancialReport,
    PlatformMetric,
    ReportSchedule,
)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'status', 'created_at')
    list_filter = ('status', 'type')
    search_fields = ('details', 'user__username')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'

@admin.register(CustomReport)
class CustomReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_name', 'report_type', 'created_by', 'created_at')
    list_filter = ('report_type',)
    search_fields = ('report_name', 'created_by__username')
    raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'

@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_type', 'period_start', 'period_end', 'generated_at')
    list_filter = ('report_type',)
    date_hierarchy = 'generated_at'

@admin.register(DailySalesReport)
class DailySalesReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_date', 'shop', 'total_revenue', 'total_orders')
    list_filter = ('report_date',)
    raw_id_fields = ('shop',)
    date_hierarchy = 'report_date'

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_type', 'shop', 'period_start', 'period_end', 'generated_at')
    list_filter = ('report_type',)
    raw_id_fields = ('shop',)
    date_hierarchy = 'generated_at'

@admin.register(PlatformMetric)
class PlatformMetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'metric_date', 'total_users', 'total_shops', 'total_orders', 'total_revenue')
    date_hierarchy = 'metric_date'

@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'frequency', 'next_run_at', 'is_active')
    list_filter = ('frequency', 'is_active')
    raw_id_fields = ('report',)
