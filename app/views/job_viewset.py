from django.db import connection
from rest_framework import viewsets
from app.serilaizers.job_serializer import *

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(uid=user_id)
        return queryset


class JobFrequencyViewSet(viewsets.ModelViewSet):
    queryset = JobFrequency.objects.all()
    serializer_class = JobFrequencySerializer