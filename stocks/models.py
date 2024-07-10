from django.contrib.auth.models import User
from django.db import models


class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)
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