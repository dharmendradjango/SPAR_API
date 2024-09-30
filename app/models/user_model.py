from django.contrib.auth.models import AbstractUser
from django.db import models
from app.utils.bitboolean import BitBooleanField

class Role(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    role = models.CharField(max_length=45, db_column='Role', blank=False, null=False)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=False, null=False)

    class Meta:
        managed = False 
        db_table = 'tbl_role'


class User(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    first_name = models.CharField(max_length=100, db_column='FirstName', blank=True, null=True)
    last_name = models.CharField(max_length=100, db_column='LastName', blank=True, null=True)
    email = models.EmailField(max_length=100, db_column='Email', blank=True, null=True)
    mobile = models.CharField(max_length=10, db_column='Mobile', blank=True, null=True)
    username = models.CharField(max_length=100, db_column='UserName', blank=True, null=True, unique=True)
    password = models.CharField(max_length=200, db_column='Password', blank=True, null=True)
    file = models.ImageField(max_length=200, db_column='Photo', blank=True, null=True)
    role_id = models.IntegerField(db_column='RoleId', blank=True, null=True)
    # uid = models.IntegerField(db_column='UID', blank=True, null=True)
    status = BitBooleanField(db_column='Status')
    reg_date = models.DateTimeField(db_column='RegDate', blank=True, null=True)

    @property
    def is_authenticated(self):
        """
        Returns True if the user is authenticated.
        """
        return self.status

    class Meta:
        managed = False 
        db_table = 'tbl_user'


# class CustomUser(AbstractUser):
#     role = models.IntegerField(db_column='role', blank=False, null=False)

#     def __str__(self):
#         return self.username


# app/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from datetime import timedelta

class CustomToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=60)  # Set token expiry (e.g., 10 minutes)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Token for {self.user.username} (Expires: {self.expires_at})"
