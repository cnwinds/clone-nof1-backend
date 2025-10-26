"""
加密货币价格 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CryptoPriceBase(BaseModel):
    """加密货币价格基础字段"""
    id: str
    symbol: str = Field(..., description="交易对符号")
    name: str = Field(..., description="币种名称")
    current_price: float = Field(..., description="当前价格")
    price_change_percentage_24h: Optional[float] = Field(None, description="24小时涨跌幅")
    market_cap: Optional[float] = Field(None, description="市值")
    high_24h: Optional[float] = Field(None, description="24小时最高价")
    low_24h: Optional[float] = Field(None, description="24小时最低价")


class CryptoPriceResponse(CryptoPriceBase):
    """加密货币价格响应"""
    last_updated: datetime
    
    class Config:
        from_attributes = True

