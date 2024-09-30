from django.db import models
from app.utils.bitboolean import BitBooleanField

class Product(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=False, null=False)
    description = models.TextField(db_column='Description', blank=False, null=False)
    price = models.CharField(max_length=10, db_column='Price', blank=False, null=False)
    uid = models.IntegerField(db_column='UID', blank=False, null=False)
    view_order = models.IntegerField(db_column='ViewOrder', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_product'


class ProductMedia(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    product_id = models.IntegerField(db_column='ProductId', blank=False, null=False)
    name = models.CharField(max_length=100, db_column='Name', blank=False, null=False)
    media_path = models.CharField(max_length=200, db_column='MediaPath', blank=False, null=False)
    media_type = models.CharField(max_length=100, db_column='MediaType', blank=False, null=False)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_product_media'