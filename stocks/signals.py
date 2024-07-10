# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Stock, PriceEntry
# import yfinance as yf
# from datetime import datetime
#
# @receiver(post_save, sender=Stock)
# def create_price_entry(sender, instance, created, **kwargs):
#     if created:
#         ticker = yf.Ticker(instance.symbol)
#         today = datetime.now().date()
#         current_price = ticker.history(period='1d').iloc[-1]['Close']
#
#         PriceEntry.objects.create(symbol=instance.symbol, date=today, price=current_price)
