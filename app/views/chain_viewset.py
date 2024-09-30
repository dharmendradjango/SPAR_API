from rest_framework import viewsets
from app.serilaizers.chain_serializer import *

class ChainViewSet(viewsets.ModelViewSet):
    queryset = Chain.objects.all()
    serializer_class = ChainSerializer


class ChainStoreViewSet(viewsets.ModelViewSet):
    queryset = ChainStore.objects.all()
    serializer_class = ChainStoreSerializer