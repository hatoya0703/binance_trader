from contextlib import contextmanager
import logging
import threading

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import settings

logger = logging.getLogger(__name__)
Base = declarative_base()
engine = create_engine(f'mysql+mysqlconnector://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}')
Session = scoped_session(sessionmaker(bind=engine))

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
            Session.add(candle)
            Session.commit()
        except IntegrityError:
            return False

    @classmethod
    def get(cls, time):
        candle = Session.query(cls).filter(cls.time == time).first()

        if candle is None:
            return None
        return candle

    def save(self):
        Session.add(self)
        Session.commit()

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


def init_db():
    Base.metadata.create_all(bind=engine)