"""
AI 模型基础配置表
"""
from sqlalchemy import Column, String, Text, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class TradingMode(str, enum.Enum):
    """交易模式"""
    PAPER = "paper"  # 模拟交易
    REAL = "real"    # 真实交易


class ModelStatus(str, enum.Enum):
    """模型状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class AIModel(Base):
    """AI 模型基础配置"""
    __tablename__ = "models"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False)
    color = Column(String(20), nullable=False)
    icon = Column(String(10))
    description = Column(Text)
    
    # LLM 配置
    llm_provider = Column(String(50), nullable=False)  # openai/anthropic/qwen
    llm_model = Column(String(100), nullable=False)    # gpt-4/claude-3-opus/qwen-max
    strategy_prompt = Column(Text, nullable=False)     # 交易策略提示词
    
    # 交易配置
    trading_mode = Column(Enum(TradingMode), nullable=False, default=TradingMode.PAPER)
    exchange_name = Column(String(50), nullable=False, default="binance")
    execution_interval = Column(Integer, nullable=False, default=15)  # 执行间隔（分钟）
    
    status = Column(Enum(ModelStatus), nullable=False, default=ModelStatus.ACTIVE)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    season_models = relationship("SeasonModel", back_populates="model", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AIModel(id={self.id}, name={self.name}, status={self.status})>"

