from datetime import datetime
import dateutil.parser
import math
import time

import sys
import logging
import ccxt
import settings


sys.path.append('../')

logger = logging.getLogger(__name__)

class Blance(object):
    def __init__(self, currency, available):
        self.currency = currency
        self.available = available

class Ticker(object):
    def __init__(self, timestamp, bid, ask, volume, symbol=settings.symbol):
        self.symbol = symbol
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.volume = volume

    @property
    def time(self):
        return datetime.utcfromtimestamp(self.timestamp)
    
    @property
    def mid_price(self):
        return (self.ask + self.bid) /2
    
    def truncate_date_time(self, duration):
        ticker_time = self.time

        if duration == '5s':
            new_sec = math.floor(self.time.second / 5) * 5
            ticker_time = datetime(self.time.year, self.time.month, self.time.day,self.time.hour, self.time.minute, new_sec)
            time_format = '%Y-%m-%d %H:%M:%S'
        elif duration == '1m':
            time_format = '%Y-%m-%d %H:%M'
        elif duration == '1h':
            time_format = '%Y-%m-%d %H'
        else:
            logger.warning('action=truncate_date_time error=datetime_format')
            return None
        
        str_date = datetime.strftime(ticker_time, time_format)
        return datetime.strptime(str_date, time_format)

class Order(object):
    def __init__(self, price, side, amount, client=settings.client, symbol=settings.symbol, type='limit'):
        self.price = price
        self.side = side
        self.amount = amount
        self.client = client
        self.symbol = symbol
        self.type = type

    def send_order(self, order: Order):
        try:
            self.client.create_order(
                order.type, )
        except Exception as e:
            logger.error(f'action=send_order error={e}')
            raise

class APIClient(object):
    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret
        self.client = settings.client
        self.symbol = settings.symbol

    def get_balance(self):
        try:
            resp = self.client.fetch_balance()
        except Exception as e:
            logger.error(f'action=get_balance error={e}')
            raise
        
        currency = settings.currency.strip('\'')
        available = float(resp['free'][settings.currency])

        return Blance(currency, available)

    def get_ticker(self, callback, symbol=settings.symbol) -> Ticker:
        while True:
            time.sleep(10)
            try:
                resp = self.client.fetch_ticker(symbol=symbol)
            except Exception as e:
                logger.error(f'action=get_ticker error={e}')
                raise

            timestamp = datetime.timestamp(
                dateutil.parser.parse(resp['datetime'])
            )
            print(resp['bid'])
            bid = float(resp['bid'])
            ask = float(resp['ask'])
            volume = self.get_candle_volume()
            ticker =  Ticker(timestamp, bid, ask, volume)
            callback(ticker)
        
    def get_candle_volume(self, limit=1, trade_duration=settings.trade_duration):
        try:
            resp =  self.client.fetch_ohlcv(symbol=settings.symbol, timeframe='5m', limit=2)
            return resp[0][5]
        except Exception as e:
            logger.error(f'action=get_candle_volume error={e}')
            raise