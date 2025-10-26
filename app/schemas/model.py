"""
AI 模型 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class AIModelBase(BaseModel):
    """AI 模型基础字段"""
    name: str = Field(..., description="内部名称")
    displayName: str = Field(..., alias="display_name", description="显示名称")
    color: str = Field(..., description="图表颜色")
    icon: Optional[str] = Field(None, description="图标")
    description: Optional[str] = Field(None, description="描述")
    llmProvider: str = Field(..., alias="llm_provider", description="LLM 提供商: openai/anthropic/qwen")
    llmModel: str = Field(..., alias="llm_model", description="LLM 模型名称")
    strategyPrompt: str = Field(..., alias="strategy_prompt", description="交易策略提示词")
    tradingMode: str = Field("paper", alias="trading_mode", description="交易模式: paper/real")
    exchangeName: str = Field("binance", alias="exchange_name", description="交易所名称")
    executionInterval: int = Field(15, alias="execution_interval", description="执行间隔（分钟）")

    model_config = ConfigDict(populate_by_name=True)


class AIModelCreate(AIModelBase):
    """创建 AI 模型"""
    pass


class AIModelUpdate(BaseModel):
    """更新 AI 模型"""
    displayName: Optional[str] = Field(None, alias="display_name")
    color: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    strategyPrompt: Optional[str] = Field(None, alias="strategy_prompt")
    tradingMode: Optional[str] = Field(None, alias="trading_mode")
    exchangeName: Optional[str] = Field(None, alias="exchange_name")
    executionInterval: Optional[int] = Field(None, alias="execution_interval")
    status: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class AIModelResponse(AIModelBase):
    """AI 模型响应"""
    id: str
    status: str
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

