from django.db import models
from app.utils.bitboolean import BitBooleanField

class Question(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    group_id = models.IntegerField(db_column='GroupId', blank=False, null=False)
    question = models.CharField(max_length=100, db_column='Question', blank=False, null=False)
    q_type = models.CharField(max_length=45, db_column='QType', blank=False, null=False)
    uid = models.IntegerField(db_column='UID', blank=False, null=False)
    view_order = models.IntegerField(db_column='ViewOrder', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_question'


class QuestionGroup(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    group = models.CharField(max_length=100, db_column='Group', blank=False, null=False)
    about = models.TextField(db_column='About', blank=False, null=False)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_question_group'