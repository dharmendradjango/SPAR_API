from django.db import models
from app.utils.bitboolean import BitBooleanField


class UserClient(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=False, null=False)
    full_name = models.CharField(max_length=100, db_column='FullName', blank=False, null=False)
    trade_name = models.CharField(max_length=100, db_column='TradeName', blank=False, null=False)
    gst = models.CharField(max_length=20, db_column='GST', blank=False, null=False)
    code = models.CharField(max_length=20, db_column='Code', blank=True, null=True)
    role = models.CharField(max_length=45, db_column='Role', blank=True, null=True) 
    type = models.CharField(max_length=45, db_column='Type', blank=True, null=True)
    email = models.EmailField(max_length=50, db_column='Email', blank=False, null=False)
    mobile = models.CharField(max_length=10, db_column='Mobile', blank=False, null=False)
    pan = models.CharField(max_length=45, db_column='PAN', blank=True, null=True)
    cin = models.CharField(max_length=45, db_column='CIN', blank=True, null=True)
    inc_date = models.DateField(db_column='INCDate', blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, null=False)
    file = models.ImageField(max_length=200, db_column='Logo', blank=True, null=True)
    uid = models.IntegerField(db_column='UID', blank=False, null=False) 
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_user_client'




