"""
交易服务
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models import Trade, SeasonModel


class TradeService:
    """交易服务"""
    
    @staticmethod
    def get_trades(
        db: Session,
        season_id: Optional[str] = None,
        model_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Trade]:
        """获取交易记录"""
        query = db.query(Trade).options(
            joinedload(Trade.season_model).joinedload(SeasonModel.model)
        )
        
        if season_id:
            query = query.join(SeasonModel).filter(SeasonModel.season_id == season_id)
        
        if model_id:
            query = query.join(SeasonModel).filter(SeasonModel.model_id == model_id)
        
        return query.order_by(Trade.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_trade_by_id(db: Session, trade_id: str) -> Optional[Trade]:
        """根据 ID 获取交易"""
        return db.query(Trade).filter(Trade.id == trade_id).first()
    
    @staticmethod
    def get_open_trades(db: Session, season_model_id: str) -> List[Trade]:
        """获取开仓交易"""
        return db.query(Trade).filter(
            Trade.season_model_id == season_model_id,
            Trade.status == "open"
        ).all()
    
    @staticmethod
    def get_closed_trades(db: Session, season_model_id: str) -> List[Trade]:
        """获取平仓交易"""
        return db.query(Trade).filter(
            Trade.season_model_id == season_model_id,
            Trade.status == "closed"
        ).all()

