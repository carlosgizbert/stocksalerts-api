from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

def validate_unique_symbol(value):
    if isinstance(value, str):
        if Stock.objects.filter(symbol=value).exists():
            raise ValidationError('Symbol must be unique for each user.')
    else:
        user = value.user
        symbol = value.symbol
        if Stock.objects.filter(user=user, symbol=symbol).exists():
            raise ValidationError('Symbol must be unique for each user.')

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, validators=[validate_unique_symbol])
    description = models.CharField(max_length=255, null=True, blank=True)
    lower_tunnel_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_tunnel_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    check_frequency = models.PositiveIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_notification_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.symbol} - {self.description}"


class PriceEntry(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_time = self.time.strftime('%H:%M:%S')
        return f"{self.stock.symbol} - {self.date} / {formatted_time} - R${self.close_price}"