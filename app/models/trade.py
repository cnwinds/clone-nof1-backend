"""
交易记录表
"""
from sqlalchemy import Column, String, ForeignKey, DECIMAL, Enum, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class TradeType(str, enum.Enum):
    """交易类型"""
    LONG = "long"    # 做多
    SHORT = "short"  # 做空


class TradeStatus(str, enum.Enum):
    """交易状态"""
    OPEN = "open"      # 开仓
    CLOSED = "closed"  # 平仓


class Trade(Base):
    """交易记录"""
    __tablename__ = "trades"
    
    id = Column(String(50), primary_key=True, index=True)
    season_model_id = Column(String(50), ForeignKey("season_models.id", ondelete="CASCADE"), nullable=False, index=True)
    
    symbol = Column(String(20), nullable=False)  # BTC, ETH, XRP 等
    type = Column(Enum(TradeType), nullable=False)
    
    # 价格和数量
    entry_price = Column(DECIMAL(20, 8), nullable=False)
    exit_price = Column(DECIMAL(20, 8))
    quantity = Column(DECIMAL(20, 8), nullable=False)
    
    # 名义价值
    entry_notional = Column(DECIMAL(20, 8), nullable=False)
    exit_notional = Column(DECIMAL(20, 8))
    
    # 持仓时间
    holding_time = Column(String(20))  # 如 "2H", "30M"
    
    # 盈亏
    pnl = Column(DECIMAL(20, 8))
    pnl_percent = Column(DECIMAL(10, 2))
    
    status = Column(Enum(TradeStatus), nullable=False, default=TradeStatus.OPEN)
    
    entry_timestamp = Column(DateTime(timezone=True), nullable=False)
    exit_timestamp = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    season_model = relationship("SeasonModel", back_populates="trades")
    
    # 索引
    __table_args__ = (
        Index('idx_season_model_status', 'season_model_id', 'status'),
    )
    
    def __repr__(self):
        return f"<Trade(id={self.id}, symbol={self.symbol}, type={self.type}, status={self.status})>"

