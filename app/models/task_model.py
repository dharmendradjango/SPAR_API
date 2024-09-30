from django.db import models
from app.utils.bitboolean import BitBooleanField

class Task(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(max_length=100, db_column='Name', blank=True, null=True)
    uid = models.IntegerField(db_column='UID', blank=True, null=True)
    store_id = models.IntegerField(db_column='StoreId', blank=True, null=True)
    job_id = models.IntegerField(db_column='JobId', blank=True, null=True)
    about = models.TextField(db_column='About', blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, null=True)
    priority = models.CharField(max_length=50, db_column='Priority', blank=True, null=True)
    is_done = models.CharField(max_length=50, db_column='IsDone', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'tbl_task'


class TaskInfo(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    tid = models.IntegerField(db_column='TID', blank=True, null=True)
    qid = models.IntegerField(db_column='QID', blank=True, null=True)
    answer = models.CharField(max_length=100, db_column='Answer', blank=True, null=True)
    status = BitBooleanField(db_column='Status', blank=True, null=True)
    reg_date = models.DateTimeField(db_column='RegDate', blank=True, null=True)

    class Meta:
        managed = False 
        db_table = 'tbl_task_info'
