"""
持仓表
"""
from sqlalchemy import Column, String, ForeignKey, DECIMAL, Integer, Enum, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class PositionSide(str, enum.Enum):
    """持仓方向"""
    LONG = "LONG"    # 多头
    SHORT = "SHORT"  # 空头


class Position(Base):
    """当前持仓"""
    __tablename__ = "positions"
    
    id = Column(String(50), primary_key=True, index=True)
    season_model_id = Column(String(50), ForeignKey("season_models.id", ondelete="CASCADE"), nullable=False, index=True)
    
    symbol = Column(String(20), nullable=False)
    side = Column(Enum(PositionSide), nullable=False)
    leverage = Column(Integer, nullable=False, default=1)
    
    # 数量和价格
    amount = Column(DECIMAL(20, 8), nullable=False)
    entry_price = Column(DECIMAL(20, 8), nullable=False)
    current_price = Column(DECIMAL(20, 8), nullable=False)
    
    # 名义价值和盈亏
    notional = Column(DECIMAL(20, 8), nullable=False)
    unrealized_pnl = Column(DECIMAL(20, 8), nullable=False, default=0)
    profit_percent = Column(DECIMAL(10, 2), nullable=False, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    season_model = relationship("SeasonModel", back_populates="positions")
    
    # 索引
    __table_args__ = (
        Index('idx_season_model_symbol', 'season_model_id', 'symbol'),
    )
    
    def __repr__(self):
        return f"<Position(id={self.id}, symbol={self.symbol}, side={self.side}, amount={self.amount})>"

