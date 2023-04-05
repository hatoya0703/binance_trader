from app.models.candle import factory_candle_class
import settings

class DataFrameCandle(object):
    def __init__(self, symbol=settings.symbol, duration=settings.trade_duration):
        self.symbol = symbol
        self.duration = duration
        self.candle_cls = factory_candle_class(self.symbol, self.duration)
        self.candles = []

    def set_all_candles(self, limit=1000):
        self.candles = self.candle_cls.get_all_candles(limit)
        return self.candles

    @property
    def value(self):
        return {
            'symbol': self.symbol,
            'duration': self.duration,
            'candles': [c.value for c in self.candles]
        }