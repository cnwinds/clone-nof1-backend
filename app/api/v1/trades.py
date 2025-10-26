"""
交易记录 API 端点
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.trade_service import TradeService
from app.schemas.trade import TradeResponse
from app.schemas.common import APIResponse
from datetime import datetime

router = APIRouter()


@router.get("/trades")
async def get_trades(
    season_id: Optional[str] = Query(None, description="赛季 ID"),
    model_id: Optional[str] = Query(None, description="模型 ID"),
    limit: int = Query(100, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """获取交易记录"""
    try:
        trades = TradeService.get_trades(db, season_id, model_id, limit)
        
        # 构建响应数据（添加模型名称）
        trades_data = []
        for trade in trades:
            trade_dict = TradeResponse.model_validate(trade).model_dump(by_alias=False)
            trade_dict["modelName"] = trade.season_model.model.display_name
            trades_data.append(trade_dict)
        
        return APIResponse(
            success=True,
            data=trades_data,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.get("/trades/{trade_id}")
async def get_trade(trade_id: str, db: Session = Depends(get_db)):
    """获取单个交易"""
    try:
        trade = TradeService.get_trade_by_id(db, trade_id)
        if not trade:
            return APIResponse(
                success=False,
                error={"code": "TRADE_NOT_FOUND", "message": "交易不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=TradeResponse.model_validate(trade).model_dump(by_alias=False),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )

