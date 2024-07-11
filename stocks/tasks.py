from celery import shared_task
from django.utils import timezone

from prostocks.utils.email_utils import send_email
from .models import Stock, PriceEntry
import yfinance as yf
from datetime import datetime, timedelta

@shared_task
def send_email_task(subject, body, to_email):
    send_email(subject, body, to_email)

@shared_task
def update_prices_periodically():
    stocks = Stock.objects.all()
    current_minute = timezone.now().minute

    for stock in stocks:
        if current_minute % stock.check_frequency == 0:
            ticker = yf.Ticker(stock.symbol)
            today = timezone.localdate()
            current_time = timezone.localtime(timezone.now())
            price_data = ticker.history(interval='1m', period='1d')

            if not price_data.empty:
                latest_data = price_data.iloc[-1]
                open_price = latest_data['Open']
                close_price = latest_data['Close']
                high_price = latest_data['High']
                low_price = latest_data['Low']

                new_entry = PriceEntry()
                new_entry.stock = stock
                new_entry.date = today
                new_entry.time = current_time.time()
                new_entry.open_price = open_price
                new_entry.close_price = close_price
                new_entry.high_price = high_price
                new_entry.low_price = low_price
                new_entry.save()

                RANGE_TO_NOTIFY_IN_MINUTES = 1440

                if close_price < stock.lower_tunnel_limit and (
                        not stock.last_notification_sent
                        or stock.last_notification_sent < timezone.now() - timedelta(minutes=RANGE_TO_NOTIFY_IN_MINUTES)
                ):
                    subject = f"ProStocks - Sugestão de compra para {stock.symbol}"
                    body = f"O preço de {stock.symbol} cruzou o limite inferior do túnel. Sugerimos avaliar uma compra."
                    send_email_task.delay(subject, body, stock.user.email)
                    stock.last_notification_sent = timezone.now()
                    stock.save()

                elif close_price > stock.upper_tunnel_limit and (
                        not stock.last_notification_sent
                        or stock.last_notification_sent < timezone.now() - timedelta(minutes=RANGE_TO_NOTIFY_IN_MINUTES)
                ):
                    subject = f"ProStocks - Sugestão de venda para {stock.symbol}"
                    body = f"O preço de {stock.symbol} cruzou o limite superior do túnel. Sugerimos avaliar uma venda."
                    send_email_task.delay(subject, body, stock.user.email)
                    stock.last_notification_sent = timezone.now()
                    stock.save()
