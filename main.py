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
from app.conrollers.webserver import start

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    from app.models.dfcandle import DataFrameCandle
    import numpy as np
    import talib

    # df = DataFrameCandle(settings.symbol, settings.trade_duration)
    # df.set_all_candles(100)

    # df.add_sma(7)
    # print(df.value)

    streamThread = Thread(target=stream.stream_ingestion_data)
    serverThread = Thread(target=start)
    streamThread.start()
    serverThread.start()

    streamThread.join()
    serverThread.join()