from django.db import models
from app.utils.bitboolean import BitBooleanField

class Chain(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name',)
    description = models.TextField(db_column='Description',)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate',)

    class Meta:
        managed = False 
        db_table = 'tbl_chain'


class ChainStore(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    store_id = models.IntegerField(db_column='StoreId')
    chain_id = models.IntegerField(db_column='ChainId')

    class Meta:
        managed = False 
        db_table = 'tbl_chain_store'