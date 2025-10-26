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
    initialCapital: float = Field(..., alias="initial_capital", description="初始资金")
    startTime: datetime = Field(..., alias="start_time", description="开始时间")
    endTime: datetime = Field(..., alias="end_time", description="结束时间")

    model_config = ConfigDict(populate_by_name=True)


class SeasonCreate(SeasonBase):
    """创建赛季"""
    modelIds: List[str] = Field(..., alias="model_ids", description="参与模型 ID 列表")
    
    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())


class SeasonUpdate(BaseModel):
    """更新赛季"""
    name: Optional[str] = None
    description: Optional[str] = None
    startTime: Optional[datetime] = Field(None, alias="start_time")
    endTime: Optional[datetime] = Field(None, alias="end_time")
    status: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class SeasonResponse(SeasonBase):
    """赛季响应"""
    id: str
    status: str
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SeasonModelSummary(BaseModel):
    """赛季模型摘要"""
    id: str
    modelId: str = Field(alias="model_id")
    displayName: str = Field(alias="display_name")
    color: str
    icon: Optional[str] = None
    currentValue: float = Field(alias="current_value")
    performance: float
    rank: Optional[int] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, protected_namespaces=())


class SeasonWithModels(SeasonResponse):
    """赛季及其模型"""
    models: List[SeasonModelSummary] = []

