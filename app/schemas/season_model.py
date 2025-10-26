"""
赛季模型实例 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.schemas.common import ValuePoint


class SeasonModelBase(BaseModel):
    """赛季模型基础字段"""
    season_id: str
    model_id: str
    initial_value: float
    current_value: float
    available_cash: float
    performance: float = 0
    rank: Optional[int] = None
    win_rate: float = 0
    total_trades: int = 0
    status: str = "active"
    
    model_config = ConfigDict(protected_namespaces=())


class SeasonModelResponse(SeasonModelBase):
    """赛季模型响应"""
    id: str
    eliminated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class SeasonModelWithDetails(SeasonModelResponse):
    """赛季模型详细信息（含模型基础信息）"""
    model_name: str
    display_name: str
    color: str
    icon: Optional[str] = None
    value_history: List[ValuePoint] = []
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

