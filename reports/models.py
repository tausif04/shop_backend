from django.db import models

class CustomReports(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    report_name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=100)
    filters_json = models.JSONField()
    created_by = models.ForeignKey('UserProfiles', models.DO_NOTHING, db_column='created_by', to_field='keycloak_user_id')
    created_at = models.DateTimeField()
    last_run_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'custom_reports'


class ComplianceReports(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    report_type = models.CharField(max_length=100)
    period_start = models.DateField()
    period_end = models.DateField()
    report_data_json = models.JSONField()
    generated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'compliance_reports'


class DailySalesReports(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    report_date = models.DateField()
    shop_id = models.PositiveBigIntegerField(blank=True, null=True)
    total_orders = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_commission = models.DecimalField(max_digits=15, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=15, decimal_places=2)
    new_customers = models.PositiveIntegerField()
    returning_customers = models.PositiveIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'daily_sales_reports'
        unique_together = (('report_date', 'shop_id'),)


class FinancialReports(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    report_type = models.CharField(max_length=100)
    shop = models.ForeignKey('Shops', models.DO_NOTHING, blank=True, null=True)
    report_data_json = models.JSONField()
    period_start = models.DateField()
    period_end = models.DateField()
    generated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'financial_reports'

class PlatformMetrics(models.Model):
    metric_id = models.BigAutoField(primary_key=True)
    metric_date = models.DateField(unique=True)
    total_users = models.PositiveIntegerField()
    active_users = models.PositiveIntegerField()
    total_shops = models.PositiveIntegerField()
    active_shops = models.PositiveIntegerField()
    total_orders = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=18, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=18, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'platform_metrics'


class ReportSchedules(models.Model):
    schedule_id = models.BigAutoField(primary_key=True)
    report = models.ForeignKey(CustomReports, models.DO_NOTHING)
    frequency = models.CharField(max_length=7)
    recipients_json = models.JSONField()
    next_run_at = models.DateTimeField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'report_schedules'


class ReportsReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=100)
    details = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reports_report'
