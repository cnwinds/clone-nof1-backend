"""
赛季模型实例表（核心表）
"""
from sqlalchemy import Column, String, ForeignKey, DECIMAL, Integer, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class SeasonModelStatus(str, enum.Enum):
    """赛季模型状态"""
    ACTIVE = "active"          # 活跃交易中
    ELIMINATED = "eliminated"  # 资金亏完，淘汰
    COMPLETED = "completed"    # 赛季结束


class SeasonModel(Base):
    """赛季中的模型实例"""
    __tablename__ = "season_models"
    
    id = Column(String(50), primary_key=True, index=True)
    season_id = Column(String(50), ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False, index=True)
    model_id = Column(String(50), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 资金状态
    initial_value = Column(DECIMAL(20, 8), nullable=False)
    current_value = Column(DECIMAL(20, 8), nullable=False)
    available_cash = Column(DECIMAL(20, 8), nullable=False)
    
    # 统计数据
    performance = Column(DECIMAL(10, 2), nullable=False, default=0)  # 收益率百分比
    rank = Column(Integer)
    win_rate = Column(DECIMAL(5, 2), default=0)
    total_trades = Column(Integer, default=0)
    
    status = Column(Enum(SeasonModelStatus), nullable=False, default=SeasonModelStatus.ACTIVE)
    eliminated_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 唯一约束：一个模型在一个赛季中只能有一个实例
    __table_args__ = (
        UniqueConstraint('season_id', 'model_id', name='uix_season_model'),
    )
    
    # 关系
    season = relationship("Season", back_populates="season_models")
    model = relationship("AIModel", back_populates="season_models")
    trades = relationship("Trade", back_populates="season_model", cascade="all, delete-orphan")
    positions = relationship("Position", back_populates="season_model", cascade="all, delete-orphan")
    value_history = relationship("ValueHistory", back_populates="season_model", cascade="all, delete-orphan")
    chats = relationship("AutomatedChat", back_populates="season_model", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SeasonModel(id={self.id}, season={self.season_id}, model={self.model_id}, value={self.current_value})>"

