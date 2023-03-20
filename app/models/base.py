from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import settings

Base = declarative_base()
engine = create_engine(f'sqlite:///{settings.db_name}?check_same_thread=False')
Session = scoped_session(sessionmaker(bind=engine))


class BaseCandleMixin(object):
    time = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)


class UsdJpyBaseCandle5S(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_1S'


class UsdJpyBaseCandle1H(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_5M'


class UsdJpyBaseCandle1H(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_15M'


class UsdJpyBaseCandle1H(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_1M'


class UsdJpyBaseCandle1M(BaseCandleMixin, Base):
    __tablename__ = 'BTC_BUSD_1H'


def init_db():
    Base.metadata.create_all(bind=engine)