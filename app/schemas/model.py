"""
AI 模型 Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AIModelBase(BaseModel):
    """AI 模型基础字段"""
    name: str = Field(..., description="内部名称")
    display_name: str = Field(..., description="显示名称")
    color: str = Field(..., description="图表颜色")
    icon: Optional[str] = Field(None, description="图标")
    description: Optional[str] = Field(None, description="描述")
    llm_provider: str = Field(..., description="LLM 提供商: openai/anthropic/qwen")
    llm_model: str = Field(..., description="LLM 模型名称")
    strategy_prompt: str = Field(..., description="交易策略提示词")
    trading_mode: str = Field("paper", description="交易模式: paper/real")
    exchange_name: str = Field("binance", description="交易所名称")
    execution_interval: int = Field(15, description="执行间隔（分钟）")


class AIModelCreate(AIModelBase):
    """创建 AI 模型"""
    pass


class AIModelUpdate(BaseModel):
    """更新 AI 模型"""
    display_name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    strategy_prompt: Optional[str] = None
    trading_mode: Optional[str] = None
    exchange_name: Optional[str] = None
    execution_interval: Optional[int] = None
    status: Optional[str] = None


class AIModelResponse(AIModelBase):
    """AI 模型响应"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

