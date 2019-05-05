from django.db import models


class TblConsultancyData(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    procurement_title = models.TextField(blank=True, null=True)
    procurement_name = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    publish_date = models.TextField(blank=True, null=True)
    close_date = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    tender_notice = models.TextField(blank=True, null=True)
    bidding_document = models.TextField(blank=True, null=True)
    page_no = models.IntegerField()
    row_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False


class TblMonthlyProgressObjectBased(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    gs_no = models.TextField(blank=True, null=True)
    financial_month = models.TextField(blank=True, null=True)
    financial_year = models.TextField(blank=True, null=True)
    sno = models.IntegerField(blank=True, null=True)
    object_code = models.TextField(blank=True, null=True)
    object_code_title = models.TextField(blank=True, null=True)
    provision_total = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    provision_capital = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    provision_revenue = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    revised_allocation_total = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    revised_allocation_capital = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    revised_allocation_revenue = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    pnd_released_total = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    pnd_released_capital = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    pnd_released_revenue = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    fd_released_total = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    fd_released_capital = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    fd_released_revenue = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    received_released_total = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    received_released_capital = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    received_released_revenue = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    utilized = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    percentage_util_revised_allocation = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    user = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = True
