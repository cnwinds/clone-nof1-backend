"""
交易记录 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TradeBase(BaseModel):
    """交易基础字段"""
    seasonModelId: str = Field(..., alias="season_model_id")
    symbol: str = Field(..., description="交易对符号")
    type: str = Field(..., description="交易类型: long/short")
    entryPrice: float = Field(..., alias="entry_price", description="入场价格")
    quantity: float = Field(..., description="数量")
    entryNotional: float = Field(..., alias="entry_notional", description="入场名义价值")

    model_config = ConfigDict(populate_by_name=True)


class TradeCreate(TradeBase):
    """创建交易"""
    entryTimestamp: datetime = Field(default_factory=datetime.utcnow, alias="entry_timestamp")

    model_config = ConfigDict(populate_by_name=True)


class TradeUpdate(BaseModel):
    """更新交易（平仓）"""
    exitPrice: float = Field(..., alias="exit_price")
    exitNotional: float = Field(..., alias="exit_notional")
    holdingTime: str = Field(..., alias="holding_time")
    pnl: float
    pnlPercent: float = Field(..., alias="pnl_percent")
    status: str = "closed"
    exitTimestamp: datetime = Field(default_factory=datetime.utcnow, alias="exit_timestamp")

    model_config = ConfigDict(populate_by_name=True)


class TradeResponse(TradeBase):
    """交易响应"""
    id: str
    exitPrice: Optional[float] = Field(None, alias="exit_price")
    exitNotional: Optional[float] = Field(None, alias="exit_notional")
    holdingTime: Optional[str] = Field(None, alias="holding_time")
    pnl: Optional[float] = None
    pnlPercent: Optional[float] = Field(None, alias="pnl_percent")
    status: str
    entryTimestamp: datetime = Field(alias="entry_timestamp")
    exitTimestamp: Optional[datetime] = Field(None, alias="exit_timestamp")
    createdAt: datetime = Field(alias="created_at")
    
    # 前端需要的额外字段
    modelName: Optional[str] = Field(None, alias="model_name")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, protected_namespaces=())

