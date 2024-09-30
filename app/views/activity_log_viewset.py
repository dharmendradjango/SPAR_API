from django.db import connection
from rest_framework import viewsets
from app.serilaizers.activity_log_serializer import *

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer

