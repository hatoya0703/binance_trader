import datetime
import omitempty

from sqlalchemy import Column, Integer, String, DateTime, desc, Float
from app.models.base import session_scope
from app.models.base import Base
import constants
import settings

class SignalEvent(Base):
    __tablename__ = 'signal_event'
    
    # カラムを定義
    time = Column(DateTime, primary_key=True, nullable=False)
    symbol = Column(String(50)) # 文字数も指定しないと、VARCHAR requires a length on dialect mysqlエラーになる
    side = Column(String(50)) # 売り or 買い
    price = Column(Float)
    unit = Column(Integer)
    
    def save(self):
        with session_scope() as session: # DBのセッションを作成
            session.add(self) # DBに保存
            
    @property
    def value(self):
        dict_values = omitempty({
            'time': self.time,
            'symbol': self.symbol,
            'side': self.side,
            'price': self.price,
            'unit': self.unit
        })
        if not dict_values:
            return None
        return dict_values
    
    @classmethod
    # classmethodなので、引数clsにはクラス自身が入る
    def get_signal_events_by_count(cls, count, symbol=settings.symbol):
        with session_scope() as session:
            rows = session.query(cls).filter(cls.symbol == symbol).order_by(desc(cls.time)).limit(count).all()
            if rows is None:
                return []
            rows.reverse()
            return rows

    @classmethod
    def get_signal_events_after_time(cls, time):
        with session_scope() as session:
            rows = session.query(cls).filter(cls.time >= time).all()
            if rows is None:
                return []
            return rows
        