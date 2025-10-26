"""
通用 Schema 定义
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from datetime import datetime

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    success: bool
    data: Optional[T] = None
    error: Optional[dict] = None
    timestamp: datetime = datetime.utcnow()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }


class ValuePoint(BaseModel):
    """价值历史点"""
    timestamp: int  # Unix 毫秒时间戳
    value: float
    
    class Config:
        from_attributes = True

