from django.db import models
from app.utils.bitboolean import BitBooleanField

class Department(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=False, null=False)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_department'


class Organization(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=False, null=False)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_organization'