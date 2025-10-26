"""
赛季 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class SeasonBase(BaseModel):
    """赛季基础字段"""
    name: str = Field(..., description="赛季名称")
    description: Optional[str] = Field(None, description="赛季描述")
    initial_capital: float = Field(..., description="初始资金")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")


class SeasonCreate(SeasonBase):
    """创建赛季"""
    model_ids: List[str] = Field(..., description="参与模型 ID 列表")
    
    model_config = ConfigDict(protected_namespaces=())


class SeasonUpdate(BaseModel):
    """更新赛季"""
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None


class SeasonResponse(SeasonBase):
    """赛季响应"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SeasonModelSummary(BaseModel):
    """赛季模型摘要"""
    id: str
    model_id: str
    display_name: str
    color: str
    icon: Optional[str] = None
    current_value: float
    performance: float
    rank: Optional[int] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class SeasonWithModels(SeasonResponse):
    """赛季及其模型"""
    models: List[SeasonModelSummary] = []

