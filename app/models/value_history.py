"""
价值历史表
"""
from sqlalchemy import Column, String, ForeignKey, DECIMAL, BigInteger, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class ValueHistory(Base):
    """账户价值历史"""
    __tablename__ = "value_history"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    season_model_id = Column(String(50), ForeignKey("season_models.id", ondelete="CASCADE"), nullable=False, index=True)
    
    timestamp = Column(BigInteger, nullable=False)  # Unix 毫秒时间戳
    value = Column(DECIMAL(20, 8), nullable=False)
    
    # 关系
    season_model = relationship("SeasonModel", back_populates="value_history")
    
    # 索引
    __table_args__ = (
        Index('idx_season_model_timestamp', 'season_model_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<ValueHistory(season_model={self.season_model_id}, timestamp={self.timestamp}, value={self.value})>"

