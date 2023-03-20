# 標準ライブラリからのインポート
import logging
import sys
from functools import  partial

# ローカルファイルからのインポート　
import settings
from binance.binance import APIClient
from binance.binance import Order

logging.basicConfig(level=logging.INFO, stream=sys.stdout )

if __name__ == "__main__" :
    api_client = APIClient(settings.binance_access_key, settings.binance_secret_access_key)
    def trade(ticker):
        print(f'mid_price={ticker.mid_price}')
        print(f'ask={ticker.ask}')
        print(f'bid={ticker.bid}')

    callback = partial(trade)
    api_client.get_ticker(callback)

    order = Order(1000, 'buy', 0.0001)