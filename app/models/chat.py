"""
自动化聊天记录表
"""
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class AutomatedChat(Base):
    """自动化聊天记录"""
    __tablename__ = "automated_chats"
    
    id = Column(String(50), primary_key=True, index=True)
    season_model_id = Column(String(50), ForeignKey("season_models.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 内容
    content = Column(Text, nullable=False)  # 摘要内容
    user_prompt = Column(Text)
    chain_of_thought = Column(Text)
    trading_decisions = Column(JSON)  # 交易决策数组
    
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    season_model = relationship("SeasonModel", back_populates="chats")
    
    def __repr__(self):
        return f"<AutomatedChat(id={self.id}, season_model={self.season_model_id}, timestamp={self.timestamp})>"

