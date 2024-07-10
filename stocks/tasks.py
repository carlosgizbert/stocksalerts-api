from celery import shared_task
from .models import Stock, PriceEntry
import yfinance as yf
from datetime import datetime

@shared_task
def send_email_task(subject, body, subscriber):
    print('Ola sou um email aaaaaa')
    print(datetime.now())


@shared_task
def update_prices_periodically():
    stocks = Stock.objects.all()
    current_minute = datetime.now().minute

    for stock in stocks:
        # Verifica se o minuto atual é múltiplo do check_frequency da ação
        if current_minute % stock.check_frequency == 0:
            ticker = yf.Ticker(stock.symbol)
            today = datetime.now().date()
            current_time = datetime.now().time()
            # Obtém os dados de preços a cada minuto para o dia atual
            price_data = ticker.history(interval='1m', period='1d')

            if not price_data.empty:
                # Pega a última linha para obter a cotação mais recente
                latest_data = price_data.iloc[-1]
                open_price = latest_data['Open']
                close_price = latest_data['Close']
                high_price = latest_data['High']
                low_price = latest_data['Low']

                new_entry = PriceEntry()
                new_entry.stock = stock
                new_entry.date = today
                new_entry.time = current_time
                new_entry.open_price = open_price
                new_entry.close_price = close_price
                new_entry.high_price = high_price
                new_entry.low_price = low_price
                new_entry.save()