"""
持仓 API 端点
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.position_service import PositionService
from app.schemas.position import PositionResponse
from app.schemas.common import APIResponse
from datetime import datetime

router = APIRouter()


@router.get("/positions", response_model=APIResponse[List[PositionResponse]])
async def get_positions(
    season_id: Optional[str] = Query(None, description="赛季 ID"),
    model_id: Optional[str] = Query(None, description="模型 ID"),
    db: Session = Depends(get_db)
):
    """获取持仓列表"""
    try:
        positions = PositionService.get_positions(db, season_id, model_id)
        
        # 构建响应数据（添加额外字段）
        positions_data = []
        for pos in positions:
            pos_dict = PositionResponse.model_validate(pos).model_dump()
            pos_dict["model_name"] = pos.season_model.model.display_name
            pos_dict["model_icon"] = pos.season_model.model.icon
            pos_dict["coin_logo"] = pos.symbol[0]  # 简化：使用首字母
            pos_dict["available_cash"] = float(pos.season_model.available_cash)
            positions_data.append(PositionResponse(**pos_dict))
        
        return APIResponse(
            success=True,
            data=positions_data,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.get("/positions/{position_id}", response_model=APIResponse[PositionResponse])
async def get_position(position_id: str, db: Session = Depends(get_db)):
    """获取单个持仓"""
    try:
        position = PositionService.get_position_by_id(db, position_id)
        if not position:
            return APIResponse(
                success=False,
                error={"code": "POSITION_NOT_FOUND", "message": "持仓不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=PositionResponse.model_validate(position),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )

