from app.models.candle import factory_candle_class
import numpy as np
import talib

from app.models.candle import factory_candle_class
import settings
from utils.utils import Serializer

def nan_to_zero(values: np.asarray):
    values[np.isnan(values)] = 0
    return values

def empty_to_none(input_list: list):
    if not input_list:
        return None
    return input_list

class Sma(Serializer):
    def __init__(self, period: int, values: list):
        self.period = period
        self.values = values

class DataFrameCandle(object):
    def __init__(self, symbol=settings.symbol, duration=settings.trade_duration):
        self.symbol = symbol
        self.duration = duration
        self.candle_cls = factory_candle_class(self.symbol, self.duration)
        self.candles = []
        self.smas = []

    def set_all_candles(self, limit=1000):
        self.candles = self.candle_cls.get_all_candles(limit)
        return self.candles

    @property
    def value(self):
        return {
            'symbol': self.symbol,
            'duration': self.duration,
            'candles': [c.value for c in self.candles],
            'smas': empty_to_none([s.value for s in self.smas])
        }
    
    @property
    def opens(self):
        values = []
        for candle in self.candles:
            values.append(candle.open)
        return values
        
    @property
    def closes(self):
        values = []
        for candle in self.candles:
            values.append(candle.close)
        return values
        
    @property
    def highs(self):
        values = []
        for candle in self.candles:
            values.append(candle.high)
        return values
        
    @property
    def lows(self):
        values = []
        for candle in self.candles:
            values.append(candle.low)
        return values
        
    @property
    def volumes(self):
        values = []
        for candle in self.candles:
            values.append(candle.volume)
        return values
    
    def add_sma(self, period: int):

        if(len(self.closes) > period):
            values = talib.SMA(np.asarray(self.closes), period)
            sma = Sma(
                period,
                nan_to_zero(values).tolist()
            )
            self.smas.append(sma)
            return True
        return False