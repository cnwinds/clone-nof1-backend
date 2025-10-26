"""
AI 模型 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.model_service import ModelService
from app.schemas.model import AIModelResponse, AIModelCreate, AIModelUpdate
from app.schemas.common import APIResponse
from datetime import datetime

router = APIRouter()


@router.get("/models")
async def get_models(db: Session = Depends(get_db)):
    """获取激活的模型（参与交易的模型）"""
    try:
        models = ModelService.get_active_models(db)
        return APIResponse(
            success=True,
            data=[AIModelResponse.model_validate(m).model_dump(by_alias=False) for m in models],
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.get("/models/all")
async def get_all_models(db: Session = Depends(get_db)):
    """获取所有模型（包括未激活的）- 管理员接口"""
    try:
        models = ModelService.get_all_models(db)
        return APIResponse(
            success=True,
            data=[AIModelResponse.model_validate(m).model_dump(by_alias=False) for m in models],
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.get("/models/{model_id}")
async def get_model(model_id: str, db: Session = Depends(get_db)):
    """获取单个模型"""
    try:
        model = ModelService.get_model_by_id(db, model_id)
        if not model:
            return APIResponse(
                success=False,
                error={"code": "MODEL_NOT_FOUND", "message": "模型不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=AIModelResponse.model_validate(model).model_dump(by_alias=False),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.post("/models")
async def create_model(model_data: AIModelCreate, db: Session = Depends(get_db)):
    """创建模型"""
    try:
        # 检查名称是否已存在
        existing = ModelService.get_model_by_name(db, model_data.name)
        if existing:
            return APIResponse(
                success=False,
                error={"code": "MODEL_EXISTS", "message": "模型名称已存在"},
                timestamp=datetime.utcnow()
            )
        
        model = ModelService.create_model(db, model_data)
        return APIResponse(
            success=True,
            data=AIModelResponse.model_validate(model).model_dump(by_alias=False),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.put("/models/{model_id}")
async def update_model(
    model_id: str,
    model_data: AIModelUpdate,
    db: Session = Depends(get_db)
):
    """更新模型"""
    try:
        model = ModelService.update_model(db, model_id, model_data)
        if not model:
            return APIResponse(
                success=False,
                error={"code": "MODEL_NOT_FOUND", "message": "模型不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=AIModelResponse.model_validate(model).model_dump(by_alias=False),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.delete("/models/{model_id}")
async def delete_model(model_id: str, db: Session = Depends(get_db)):
    """删除模型"""
    try:
        success = ModelService.delete_model(db, model_id)
        if not success:
            return APIResponse(
                success=False,
                error={"code": "MODEL_NOT_FOUND", "message": "模型不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data={"message": "模型已删除"},
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )

