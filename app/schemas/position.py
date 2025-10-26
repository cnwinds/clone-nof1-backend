"""
持仓 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class PositionBase(BaseModel):
    """持仓基础字段"""
    seasonModelId: str = Field(..., alias="season_model_id")
    symbol: str = Field(..., description="交易对符号")
    side: str = Field(..., description="方向: LONG/SHORT")
    leverage: int = Field(1, description="杠杆倍数")
    amount: float = Field(..., description="数量")
    entryPrice: float = Field(..., alias="entry_price", description="入场价格")
    currentPrice: float = Field(..., alias="current_price", description="当前价格")
    notional: float = Field(..., description="名义价值")

    model_config = ConfigDict(populate_by_name=True)


class PositionCreate(PositionBase):
    """创建持仓"""
    unrealizedPnl: float = Field(0, alias="unrealized_pnl")
    profitPercent: float = Field(0, alias="profit_percent")

    model_config = ConfigDict(populate_by_name=True)


class PositionUpdate(BaseModel):
    """更新持仓"""
    currentPrice: float = Field(..., alias="current_price")
    notional: float
    unrealizedPnl: float = Field(..., alias="unrealized_pnl")
    profitPercent: float = Field(..., alias="profit_percent")

    model_config = ConfigDict(populate_by_name=True)


class PositionResponse(PositionBase):
    """持仓响应"""
    id: str
    unrealizedPnl: float = Field(alias="unrealized_pnl")
    profitPercent: float = Field(alias="profit_percent")
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")
    
    # 前端需要的额外字段
    modelName: Optional[str] = Field(None, alias="model_name")
    modelIcon: Optional[str] = Field(None, alias="model_icon")
    coinLogo: Optional[str] = Field(None, alias="coin_logo")
    availableCash: Optional[float] = Field(None, alias="available_cash")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, protected_namespaces=())

