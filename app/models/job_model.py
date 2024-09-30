from django.db import models
from app.utils.bitboolean import BitBooleanField

class Job(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=True, null=True)
    about = models.TextField(db_column='About', blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, null=True)
    business_type = models.CharField(max_length=200, db_column='BussinessType', blank=True, null=True)
    work_type = models.CharField(max_length=200, db_column='WorkType', blank=True, null=True)
    job_type = models.CharField(max_length=200, db_column='JobType', blank=True, null=True)
    job_category = models.CharField(max_length=200, db_column='JobCategory', blank=True, null=True)
    job_managed_by = models.CharField(max_length=200, db_column='JobManagedBy', blank=True, null=True)
    revenue_managed_by = models.CharField(max_length=200, db_column='RevenueManagedBY', blank=True, null=True)
    ms_type = models.CharField(max_length=200, db_column='MSType', blank=True, null=True)
    department_id = models.IntegerField(db_column='DepartmentId', blank=True, null=True)
    organization_id = models.IntegerField(db_column='OrganizationId', blank=True, null=True)
    manager_id = models.IntegerField(db_column='ManaerId', blank=True, null=True)
    uid = models.IntegerField(db_column='UID', blank=True, null=True)
    job_date = models.DateField(db_column='JobDate', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'tbl_job'


class JobFrequency(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    job_id = models.IntegerField(db_column='JobId', blank=False, null=False)
    f_date = models.DateField(db_column='FDate', blank=False, null=False)
    f_time = models.TimeField(db_column='Ftime', blank=False, null=False)
    note = models.TextField(db_column='Note',blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='Regdate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_job_frequency'
