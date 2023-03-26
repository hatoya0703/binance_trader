from functools import partial
import logging

from app.models.candle import create_candle_widh_duration
from binance.binance import CandleStick, APIClient


import settings

logger = logging.getLogger(__name__)

# TODO
from binance.binance import APIClient

client = APIClient()

class StreamData(object):

    def stream_ingestion_data(self):
        client.get_candle_info(callback=self.trade)

    def trade(self, candle: CandleStick):
        logger.info(f'action=trade ticker={candle.__dict__}')
        is_created = create_candle_widh_duration(candle)
        print(is_created)

stream = StreamData()
