"""
加密货币价格 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CryptoPriceBase(BaseModel):
    """加密货币价格基础字段"""
    id: str
    symbol: str = Field(..., description="交易对符号")
    name: str = Field(..., description="币种名称")
    currentPrice: float = Field(..., alias="current_price", description="当前价格")
    priceChangePercentage24h: Optional[float] = Field(None, alias="price_change_percentage_24h", description="24小时涨跌幅")
    marketCap: Optional[float] = Field(None, alias="market_cap", description="市值")
    high24h: Optional[float] = Field(None, alias="high_24h", description="24小时最高价")
    low24h: Optional[float] = Field(None, alias="low_24h", description="24小时最低价")

    model_config = ConfigDict(populate_by_name=True)


class CryptoPriceResponse(CryptoPriceBase):
    """加密货币价格响应"""
    lastUpdated: datetime = Field(alias="last_updated", description="最后更新时间")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

