"""
持仓服务
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models import Position, SeasonModel
from app.exchange.factory import ExchangeFactory
import logging

logger = logging.getLogger(__name__)


class PositionService:
    """持仓服务"""
    
    @staticmethod
    def get_positions(
        db: Session,
        season_id: Optional[str] = None,
        model_id: Optional[str] = None
    ) -> List[Position]:
        """获取持仓列表"""
        query = db.query(Position).options(
            joinedload(Position.season_model).joinedload(SeasonModel.model)
        )
        
        if season_id:
            query = query.join(SeasonModel).filter(SeasonModel.season_id == season_id)
        
        if model_id:
            query = query.join(SeasonModel).filter(SeasonModel.model_id == model_id)
        
        return query.all()
    
    @staticmethod
    def get_position_by_id(db: Session, position_id: str) -> Optional[Position]:
        """根据 ID 获取持仓"""
        return db.query(Position).filter(Position.id == position_id).first()
    
    @staticmethod
    async def update_positions_prices(db: Session):
        """更新所有持仓的当前价格"""
        try:
            positions = db.query(Position).all()
            if not positions:
                return
            
            # 获取所有需要更新的交易对
            symbols = list(set([pos.symbol for pos in positions]))
            
            # 使用模拟交易获取价格（无需 API 密钥）
            exchange = ExchangeFactory.create_exchange("binance", "paper")
            tickers = await exchange.get_multiple_tickers(symbols)
            await exchange.close()
            
            # 更新每个持仓的价格
            for pos in positions:
                ticker_symbol = f"{pos.symbol}/USDT"
                if ticker_symbol in tickers:
                    current_price = tickers[ticker_symbol]["last"]
                    pos.current_price = current_price
                    
                    # 重新计算盈亏
                    if pos.side == "LONG":
                        pnl = (current_price - pos.entry_price) * pos.amount
                    else:  # SHORT
                        pnl = (pos.entry_price - current_price) * pos.amount
                    
                    pos.unrealized_pnl = pnl
                    pos.profit_percent = (pnl / pos.notional) * 100 if pos.notional > 0 else 0
            
            db.commit()
            logger.info(f"更新了 {len(positions)} 个持仓的价格")
            
        except Exception as e:
            logger.error(f"更新持仓价格失败: {e}")
            db.rollback()

