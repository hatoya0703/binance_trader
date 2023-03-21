# 標準ライブラリからのインポート
import logging
import sys
import datetime
from functools import  partial

# ローカルファイルからのインポート　
import settings
from binance.binance import APIClient
from binance.binance import Order
from app.models.base import BtcBusdBaseCandle1M

logging.basicConfig(level=logging.INFO, stream=sys.stdout )

if __name__ == "__main__":
    import app.models

    now1 = datetime.datetime(2021,1,2,3,4,5)
    # BtcBusdBaseCandle1M.create(now1, 1.1,2.2,3.3,4.4,5)
    candle = BtcBusdBaseCandle1M.get(now1)
    print(candle.time)
    print(candle.open)
    candle.open = 10000.1
    candle.save()
 
    updated_candle = BtcBusdBaseCandle1M.get(now1)
    print(updated_candle.open)