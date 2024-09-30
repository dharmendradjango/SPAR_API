from django.db import models
from app.utils.bitboolean import BitBooleanField 

class Store(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=False, null=False)
    owner_name = models.CharField(max_length=100, db_column='OwnerName', blank=False, null=False)
    email = models.EmailField(max_length=100, db_column='Email', blank=False, null=False)
    mobile = models.CharField(max_length=10, db_column='Mobile', blank=False, null=False)
    #chain_id = models.IntegerField(db_column='ChainId', blank=False, null=False)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_store'


class StoreMedia(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    store_id = models.IntegerField(db_column='StoreId', blank=True, null=True)
    name = models.CharField(max_length=100, db_column='Name', blank=True, null=True)
    file = models.FileField(upload_to='media/', db_column='MediaPath', blank=True, null=True)
    media_type = models.CharField(max_length=45, db_column='MediaType', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'tbl_store_media'


class StoreProduct(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    store_id = models.IntegerField(db_column='StoreId', blank=True, null=True)
    product_id = models.IntegerField(db_column='ProductId', blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'tbl_store_product'
