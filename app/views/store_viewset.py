from rest_framework import viewsets
from app.serilaizers.store_serializer import *

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreProductViewSet(viewsets.ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer


class StoreMediaViewSet(viewsets.ModelViewSet):
    queryset = StoreMedia.objects.all()
    serializer_class = StoreMediaSerializer
