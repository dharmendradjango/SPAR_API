from django.db import models
from app.utils.bitboolean import BitBooleanField

    
class State(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=False, null=False)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_state'
    

class City(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    state_id = models.IntegerField(db_column='StateId')
    city = models.CharField(max_length=100, db_column='City')
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate')

    class Meta:
        managed = False 
        db_table = 'tbl_city'


class Pincode(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    code = models.IntegerField(db_column='Code')
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate')

    class Meta:
        managed = False 
        db_table = 'tbl_pincode'


class ClientAddress(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    uid = models.IntegerField(db_column='UID', blank=False, null=False)
    address1 = models.CharField(max_length=100, db_column='Address1', blank=False, null=False) 
    address2 = models.CharField(max_length=100, db_column='Address2', blank=False, null=False)
    street = models.CharField(max_length=100, db_column='Street')
    landmark = models.CharField(max_length=100, db_column='Landmark')
    city = models.IntegerField(db_column='City', blank=False, null=False)
    state = models.IntegerField(db_column='State', blank=False, null=False)
    country = models.CharField(max_length=45, db_column='Country', blank=False, null=False)
    pin_code = models.IntegerField(db_column='PinCode', blank=False, null=False)
    latitude = models.CharField(max_length=45, db_column='Latitude', blank=True, null=True)
    longitude = models.CharField(max_length=45, db_column='Longitude', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_client_address'


class StoreAddress(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    store_id = models.IntegerField(db_column='StoreId', blank=True, null=True)
    address1 = models.CharField(max_length=100, db_column='Address1', blank=True, null=True)
    address2 = models.CharField(max_length=100, db_column='Address2', blank=True, null=True)
    street = models.CharField(max_length=100, db_column='Street', blank=True, null=True)
    landmark = models.CharField(max_length=100, db_column='Landmark', blank=True, null=True)
    city = models.IntegerField(db_column='City', blank=True, null=True)
    state = models.IntegerField(db_column='State', blank=True, null=True)
    country = models.CharField(max_length=45, db_column='Country', blank=True, null=True)
    pincode = models.IntegerField(db_column='Pincode', blank=True, null=True)
    latitude = models.CharField(max_length=45, db_column='Latitude', blank=True, null=True)
    longitude = models.CharField(max_length=45, db_column='Longitude', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'tbl_store_address'


class UserClientAddress(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    user_id = models.IntegerField(db_column='User_id', blank=False, null=False)
    user_client_id = models.IntegerField(db_column='user_client_id', blank=False, null=False)
    user_address_id = models.IntegerField(db_column='user_address_id', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_client_user_address'
