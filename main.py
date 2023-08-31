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
    from app.models.events import SignalEvent
    import datetime
    import settings
    import constants
    
    now = datetime.datetime.now().utcnow()
    s = SignalEvent(time=now, symbol=settings.symbol, side=constants.BUY, price=100.0, unit=1)
    s.save()
    
    signal_events = SignalEvent.get_signal_events_by_count(10)
    for signal_event in signal_events:
        print(signal_event.value)
        
    now -= datetime.timedelta(minutes=10)
    signal_events = SignalEvent.get_signal_events_after_time(now)
    for signal_event in signal_events:
        print(signal_event.value)

    # df = DataFrameCandle(settings.symbol, settings.trade_duration)
    # df.set_all_candles(100)

    # df.add_sma(7)
    # print(df.value)

    # streamThread = Thread(target=stream.stream_ingestion_data)
    # serverThread = Thread(target=start)
    # streamThread.start()
    # serverThread.start()

    # streamThread.join()
    # serverThread.join()