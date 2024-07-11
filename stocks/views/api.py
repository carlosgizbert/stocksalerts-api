from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from stocks.models import Stock, PriceEntry
from stocks.serializers import StockSerializer, PriceEntrySerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Stock.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["put", "patch"])
    def update_stock(self, request, pk=None):
        stock = self.get_object()
        if stock.user == request.user:
            serializer = self.get_serializer(stock, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["delete"])
    def delete_stock(self, request, pk=None):
        stock = self.get_object()
        if stock.user == request.user:
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class PriceEntryViewSet(viewsets.ModelViewSet):
    queryset = PriceEntry.objects.all()
    serializer_class = PriceEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PriceEntry.objects.filter(stock__user=self.request.user)

# class PriceEntryViewSet(viewsets.ModelViewSet):
#     queryset = PriceEntry.objects.all()
#     serializer_class = PriceEntrySerializer