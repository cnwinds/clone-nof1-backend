"""
赛季 API 端点
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.season_service import SeasonService
from app.schemas.season import SeasonResponse, SeasonCreate, SeasonUpdate, SeasonWithModels, SeasonModelSummary
from app.schemas.common import APIResponse
from datetime import datetime

router = APIRouter()


@router.get("/seasons", response_model=APIResponse[List[SeasonResponse]])
async def get_seasons(
    status: Optional[str] = Query(None, description="过滤状态: pending/active/completed"),
    db: Session = Depends(get_db)
):
    """获取所有赛季"""
    try:
        seasons = SeasonService.get_all_seasons(db, status)
        return APIResponse(
            success=True,
            data=[SeasonResponse.model_validate(s) for s in seasons],
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.get("/seasons/active", response_model=APIResponse[SeasonResponse])
async def get_active_season(db: Session = Depends(get_db)):
    """获取当前活跃赛季"""
    try:
        season = SeasonService.get_active_season(db)
        if not season:
            return APIResponse(
                success=False,
                error={"code": "NO_ACTIVE_SEASON", "message": "当前没有活跃的赛季"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=SeasonResponse.model_validate(season),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.get("/seasons/{season_id}", response_model=APIResponse[SeasonWithModels])
async def get_season(season_id: str, db: Session = Depends(get_db)):
    """获取赛季详情（含模型排名）"""
    try:
        season = SeasonService.get_season_by_id(db, season_id)
        if not season:
            return APIResponse(
                success=False,
                error={"code": "SEASON_NOT_FOUND", "message": "赛季不存在"},
                timestamp=datetime.utcnow()
            )
        
        # 构建响应数据
        season_data = SeasonResponse.model_validate(season)
        models_data = []
        
        for sm in season.season_models:
            # 只显示激活的模型
            if sm.model.status == "active":
                models_data.append(SeasonModelSummary(
                    id=sm.id,
                    model_id=sm.model_id,
                    display_name=sm.model.display_name,
                    color=sm.model.color,
                    icon=sm.model.icon,
                    current_value=float(sm.current_value),
                    performance=float(sm.performance),
                    rank=sm.rank,
                    status=sm.status
                ))
        
        # 按排名排序
        models_data.sort(key=lambda x: x.rank if x.rank else 999)
        
        return APIResponse(
            success=True,
            data=SeasonWithModels(
                **season_data.model_dump(),
                models=models_data
            ),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.post("/seasons", response_model=APIResponse[SeasonResponse])
async def create_season(season_data: SeasonCreate, db: Session = Depends(get_db)):
    """创建赛季"""
    try:
        season = SeasonService.create_season(db, season_data)
        return APIResponse(
            success=True,
            data=SeasonResponse.model_validate(season),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.post("/seasons/{season_id}/start", response_model=APIResponse[SeasonResponse])
async def start_season(season_id: str, db: Session = Depends(get_db)):
    """启动赛季"""
    try:
        season = SeasonService.start_season(db, season_id)
        if not season:
            return APIResponse(
                success=False,
                error={"code": "CANNOT_START", "message": "无法启动赛季"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=SeasonResponse.model_validate(season),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.post("/seasons/{season_id}/end", response_model=APIResponse[SeasonResponse])
async def end_season(season_id: str, db: Session = Depends(get_db)):
    """结束赛季"""
    try:
        season = SeasonService.end_season(db, season_id)
        if not season:
            return APIResponse(
                success=False,
                error={"code": "SEASON_NOT_FOUND", "message": "赛季不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=SeasonResponse.model_validate(season),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.put("/seasons/{season_id}", response_model=APIResponse[SeasonResponse])
async def update_season(
    season_id: str,
    season_data: SeasonUpdate,
    db: Session = Depends(get_db)
):
    """更新赛季"""
    try:
        season = SeasonService.update_season(db, season_id, season_data)
        if not season:
            return APIResponse(
                success=False,
                error={"code": "SEASON_NOT_FOUND", "message": "赛季不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=SeasonResponse.model_validate(season),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )

