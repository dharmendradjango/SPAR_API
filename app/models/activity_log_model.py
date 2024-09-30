from django.db import models

class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    table_name = models.CharField(max_length=100, db_column='TableName', blank=False, null=False)
    user_name = models.CharField(max_length=100, db_column='UserName', blank=False, null=False)
    action = models.CharField(max_length=100, db_column='Action', blank=False, null=False)
    ip_address = models.CharField(max_length=100, db_column='IPAddress', blank=False, null=False)
    data = models.TextField( db_column='Data', blank=False, null=False)
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_activity_log'
