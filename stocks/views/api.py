from rest_framework import viewsets

from stocks.models import Stock, PriceEntry
from stocks.serializers import StockSerializer, PriceEntrySerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class PriceEntryViewSet(viewsets.ModelViewSet):
    queryset = PriceEntry.objects.all()
    serializer_class = PriceEntrySerializer