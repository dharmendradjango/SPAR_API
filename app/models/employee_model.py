from django.db import models

class UserEmployee(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    uid = models.IntegerField(db_column='UID', blank=True, null=True)
    designation = models.CharField(max_length=100, db_column='Designation', blank=True, null=True)
    address = models.CharField(max_length=100, db_column='Address', blank=True, null=True)
    gender = models.CharField(max_length=10, db_column='Gender', blank=True, null=True)
    dob = models.DateField(db_column='DOB', blank=True, null=True)
    doj = models.DateField(db_column='DOJ', blank=True, null=True)
    adhaar_number = models.CharField(max_length=45, db_column='AdhaarNumber', blank=True, null=True)
    pin_code = models.CharField(max_length=6, db_column='PinCode', blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'tbl_user_employee'