"""
加密货币价格缓存表
"""
from sqlalchemy import Column, String, DECIMAL, DateTime, Index
from sqlalchemy.sql import func
from app.core.database import Base


class CryptoPrice(Base):
    """加密货币价格缓存"""
    __tablename__ = "crypto_prices"
    
    id = Column(String(50), primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    
    # 价格信息
    current_price = Column(DECIMAL(20, 8), nullable=False)
    price_change_24h = Column(DECIMAL(10, 2))
    market_cap = Column(DECIMAL(30, 2))
    high_24h = Column(DECIMAL(20, 8))
    low_24h = Column(DECIMAL(20, 8))
    
    last_updated = Column(DateTime(timezone=True), nullable=False)
    
    # 索引
    __table_args__ = (
        Index('idx_symbol_updated', 'symbol', 'last_updated'),
    )
    
    def __repr__(self):
        return f"<CryptoPrice(symbol={self.symbol}, price={self.current_price})>"

