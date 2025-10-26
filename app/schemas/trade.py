"""
交易记录 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TradeBase(BaseModel):
    """交易基础字段"""
    season_model_id: str
    symbol: str = Field(..., description="交易对符号")
    type: str = Field(..., description="交易类型: long/short")
    entry_price: float = Field(..., description="入场价格")
    quantity: float = Field(..., description="数量")
    entry_notional: float = Field(..., description="入场名义价值")


class TradeCreate(TradeBase):
    """创建交易"""
    entry_timestamp: datetime = Field(default_factory=datetime.utcnow)


class TradeUpdate(BaseModel):
    """更新交易（平仓）"""
    exit_price: float
    exit_notional: float
    holding_time: str
    pnl: float
    pnl_percent: float
    status: str = "closed"
    exit_timestamp: datetime = Field(default_factory=datetime.utcnow)


class TradeResponse(TradeBase):
    """交易响应"""
    id: str
    exit_price: Optional[float] = None
    exit_notional: Optional[float] = None
    holding_time: Optional[str] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None
    status: str
    entry_timestamp: datetime
    exit_timestamp: Optional[datetime] = None
    created_at: datetime
    
    # 前端需要的额外字段
    model_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

