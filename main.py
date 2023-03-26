# 標準ライブラリからのインポート
import logging
import sys
import datetime
from functools import partial
import time
from threading import Thread
import ipdb as pdb

# ローカルファイルからのインポート
import settings
from binance.binance import APIClient
# from binance.binance import Order
from app.models.candle import factory_candle_class
from app.conrollers.streamdata import stream

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    import app.models

    # for i in range(200):
    #     now2 = datetime.datetime(2000 + i,1,2,3,4,5)
    #     BtcBusdBaseCandle1M.create(now2, 1.1,2.2,3.3,4.4,5)

    # cls = factory_candole_class(settings.symbol, '1m')
    # candles = cls.get_all_candles(3)
    # for candle in candles:
    #     print(candle.value)
    
    # pdb.set_trace()
    streamThread = Thread(target=stream.stream_ingestion_data)
    streamThread.start()
    streamThread.join()