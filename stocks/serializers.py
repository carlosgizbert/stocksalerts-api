from rest_framework import serializers
from stocks.models import Stock, PriceEntry

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'user', 'symbol', 'description', 'lower_tunnel_limit', 'upper_tunnel_limit',
                  'check_frequency', 'created_at', 'updated_at', 'last_notification_sent']

class PriceEntrySerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    class Meta:
        model = PriceEntry
        fields = ['id', 'stock', 'date', 'time', 'open_price', 'close_price', 'high_price',
                  'low_price', 'created_at']
