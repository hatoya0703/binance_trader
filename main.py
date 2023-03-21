# 標準ライブラリからのインポート
import logging
import sys
import datetime
from functools import  partial

# ローカルファイルからのインポート　
import settings
from binance.binance import APIClient
from binance.binance import Order
from app.models.candle import BtcBusdBaseCandle1M

logging.basicConfig(level=logging.INFO, stream=sys.stdout )

if __name__ == "__main__":
    import app.models

    now2 = datetime.datetime(2022,1,2,3,4,5)
    # BtcBusdBaseCandle1M.create(now2, 1.1,2.2,3.3,4.4,5)
    candle = BtcBusdBaseCandle1M.get(now2)
    print(candle.time)
    print(candle.open)
    candle.open = 1000.01
    candle.save()
 
    update_candle = BtcBusdBaseCandle1M.get(now2)
    print(update_candle.time)
    print(update_candle.open)