from celery import shared_task
from django.utils import timezone

from prostocks.utils.email_utils import send_email
from .models import Stock, PriceEntry
import yfinance as yf
from datetime import timedelta

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

                new_entry = PriceEntry(
                    stock=stock,
                    date=today,
                    time=current_time.time(),
                    open_price=open_price,
                    close_price=close_price,
                    high_price=high_price,
                    low_price=low_price
                )
                new_entry.save()

                RANGE_TO_NOTIFY_IN_MINUTES = 3

                if close_price < stock.lower_tunnel_limit and (
                        not stock.last_notification_sent
                        or stock.last_notification_sent < timezone.now() - timedelta(minutes=RANGE_TO_NOTIFY_IN_MINUTES)
                ):
                    subject = f"ProStocks - Sugestão de compra para {stock.symbol}"
                    html = f"<strong>O preço de {stock.symbol} é R${high_price}, e cruzou o limite inferior do túnel. Sugerimos avaliar uma compra. <br> Caso o valor se mantenha, você receberá uma nova notificação em {RANGE_TO_NOTIFY_IN_MINUTES} minutos</strong>"
                    send_email(subject, html_content=html, text_content='Teste', to_email=stock.user.username)
                    stock.last_notification_sent = timezone.now()
                    stock.save()

                elif close_price > stock.upper_tunnel_limit and (
                        not stock.last_notification_sent
                        or stock.last_notification_sent < timezone.now() - timedelta(minutes=RANGE_TO_NOTIFY_IN_MINUTES)
                ):
                    subject = f"ProStocks - Sugestão de venda para {stock.symbol}"
                    html = f"<strong>O preço de {stock.symbol} é é R${high_price}, e cruzou o limite superior do túnel. Sugerimos avaliar uma venda. <br> Caso o valor se mantenha, você receberá uma nova notificação em {RANGE_TO_NOTIFY_IN_MINUTES} minutos</strong>"
                    send_email(subject, html_content=html, text_content='Teste', to_email=stock.user.username)
                    stock.last_notification_sent = timezone.now()
                    stock.save()
