from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import yfinance as yf

from prostocks.utils.email_utils import send_email
from .models import Stock, PriceEntry

RANGE_TO_NOTIFY_IN_MINUTES = 120

@shared_task
def send_email_task(subject, body, to_email):
    send_email(subject, body, to_email)

@shared_task
def update_prices_periodically():
    stocks = Stock.objects.all()
    current_minute = timezone.now().minute

    for stock in stocks:
        if current_minute % stock.check_frequency == 0:
            update_stock_price(stock)

def update_stock_price(stock):
    ticker = yf.Ticker(stock.symbol)
    price_data = ticker.history(interval='1m', period='1d')

    if not price_data.empty:
        latest_data = price_data.iloc[-1]
        open_price = latest_data['Open']
        close_price = latest_data['Close']
        high_price = latest_data['High']
        low_price = latest_data['Low']
        current_time = timezone.localtime(timezone.now())

        new_entry = PriceEntry(
            stock=stock,
            date=timezone.localdate(),
            time=current_time.time(),
            open_price=open_price,
            close_price=close_price,
            high_price=high_price,
            low_price=low_price
        )
        new_entry.save()

        check_and_send_notification(stock, close_price, high_price)

def check_and_send_notification(stock, close_price, high_price):
    if should_notify(stock, close_price, stock.lower_tunnel_limit):
        send_notification(
            stock, close_price, high_price, "compra",
            "cruzou o limite inferior do túnel. Sugerimos avaliar uma compra."
        )
        stock.last_notification_sent = timezone.now()
        stock.save()

    elif should_notify(stock, close_price, stock.upper_tunnel_limit):
        send_notification(
            stock, close_price, high_price, "venda",
            "cruzou o limite superior do túnel. Sugerimos avaliar uma venda."
        )
        stock.last_notification_sent = timezone.now()
        stock.save()

def should_notify(stock, close_price, tunnel_limit):
    return close_price < tunnel_limit and (
        not stock.last_notification_sent
        or stock.last_notification_sent < timezone.now() - timedelta(minutes=RANGE_TO_NOTIFY_IN_MINUTES)
    )

def send_notification(stock, close_price, high_price, action, message):
    subject = f"ProStocks - Sugestão de {action} para {stock.symbol}"
    html_content = (
        f"<strong>O preço de {stock.symbol} é R${high_price}, e {message} <br>"
        f"Caso o valor se mantenha, você receberá uma nova notificação em {RANGE_TO_NOTIFY_IN_MINUTES} minutos</strong>"
    )
    send_email(
        subject,
        html_content=html_content,
        text_content='Teste',
        to_email=stock.user.username
    )
