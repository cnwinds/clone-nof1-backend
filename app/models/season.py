"""
交易赛季表
"""
from sqlalchemy import Column, String, Text, DECIMAL, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class SeasonStatus(str, enum.Enum):
    """赛季状态"""
    PENDING = "pending"      # 待开始
    ACTIVE = "active"        # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class Season(Base):
    """交易赛季"""
    __tablename__ = "seasons"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # 赛季配置
    initial_capital = Column(DECIMAL(20, 8), nullable=False)  # 每个模型的初始资金
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    
    status = Column(Enum(SeasonStatus), nullable=False, default=SeasonStatus.PENDING)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    season_models = relationship("SeasonModel", back_populates="season", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Season(id={self.id}, name={self.name}, status={self.status})>"

