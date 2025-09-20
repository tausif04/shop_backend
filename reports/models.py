from django.db import models
from users.models import User
from shop.models import Shop

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    details = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reports_report'

class CustomReport(models.Model):
    report_name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=100)
    filters_json = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_run_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'custom_reports'

class ComplianceReport(models.Model):
    report_type = models.CharField(max_length=100)
    period_start = models.DateField()
    period_end = models.DateField()
    report_data_json = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'compliance_reports'

class DailySalesReport(models.Model):
    report_date = models.DateField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    total_orders = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_commission = models.DecimalField(max_digits=15, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=15, decimal_places=2)
    new_customers = models.PositiveIntegerField()
    returning_customers = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_sales_reports'
        unique_together = (('report_date', 'shop'),)

class FinancialReport(models.Model):
    report_type = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    report_data_json = models.JSONField()
    period_start = models.DateField()
    period_end = models.DateField()
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'financial_reports'

class PlatformMetric(models.Model):
    metric_date = models.DateField(unique=True)
    total_users = models.PositiveIntegerField()
    active_users = models.PositiveIntegerField()
    total_shops = models.PositiveIntegerField()
    active_shops = models.PositiveIntegerField()
    total_orders = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=18, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=18, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'platform_metrics'

class ReportSchedule(models.Model):
    report = models.ForeignKey(CustomReport, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=7)
    recipients_json = models.JSONField()
    next_run_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_schedules'
