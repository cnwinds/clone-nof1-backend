"""
持仓 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class PositionBase(BaseModel):
    """持仓基础字段"""
    season_model_id: str
    symbol: str = Field(..., description="交易对符号")
    side: str = Field(..., description="方向: LONG/SHORT")
    leverage: int = Field(1, description="杠杆倍数")
    amount: float = Field(..., description="数量")
    entry_price: float = Field(..., description="入场价格")
    current_price: float = Field(..., description="当前价格")
    notional: float = Field(..., description="名义价值")


class PositionCreate(PositionBase):
    """创建持仓"""
    unrealized_pnl: float = 0
    profit_percent: float = 0


class PositionUpdate(BaseModel):
    """更新持仓"""
    current_price: float
    notional: float
    unrealized_pnl: float
    profit_percent: float


class PositionResponse(PositionBase):
    """持仓响应"""
    id: str
    unrealized_pnl: float
    profit_percent: float
    created_at: datetime
    updated_at: datetime
    
    # 前端需要的额外字段
    model_name: Optional[str] = None
    model_icon: Optional[str] = None
    coin_logo: Optional[str] = None
    available_cash: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

