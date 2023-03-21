import logging

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
from app.models.base import session_scope

logger = logging.getLogger(__name__)

class BaseCandleMixin(object):
    time = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)

    @classmethod
    def create(cls, time, open, close, high, low, volume):
        candle = cls(time=time,
                     open=open,
                     close=close,
                     high=high,
                     low=low,
                     volume=volume
        )

        try:
            with session_scope() as session:
                session.add(candle)
        except IntegrityError:
            return False

    @classmethod
    def get(cls, time):
        with session_scope() as session:
            candle = session.query(cls).filter(cls.time == time).first()

            if candle is None:
                return None
            return candle

    def save(self):
        with session_scope() as session:
            session.add(self)

class BtcBusdBaseCandle5S(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_1S'


class BtcBusdBaseCandle1M(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_1M'


class BtcBusdBaseCandle5M(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_5M'


class BtcBusdBaseCandle15M(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_15M'


class BtcBusdBaseCandle1H(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_1H'