"""
自动化聊天 Schema
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime


class TradingDecision(BaseModel):
    """交易决策"""
    symbol: str
    quantity: float
    action: str  # HOLD/BUY/SELL/WATCH/MONITOR/RESERVE
    confidence: int = Field(..., ge=0, le=100, description="信心度 0-100")


class ChatSection(BaseModel):
    """聊天部分"""
    type: str  # USER_PROMPT/CHAIN_OF_THOUGHT/TRADING_DECISIONS
    content: Any  # str 或 List[TradingDecision]
    expanded: bool = False


class AutomatedChatBase(BaseModel):
    """自动化聊天基础字段"""
    seasonModelId: str = Field(..., alias="season_model_id")
    content: str = Field(..., description="摘要内容")
    userPrompt: Optional[str] = Field(None, alias="user_prompt")
    chainOfThought: Optional[str] = Field(None, alias="chain_of_thought")
    tradingDecisions: Optional[List[dict]] = Field(None, alias="trading_decisions")

    model_config = ConfigDict(populate_by_name=True)


class AutomatedChatCreate(AutomatedChatBase):
    """创建自动化聊天"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True)


class AutomatedChatResponse(AutomatedChatBase):
    """自动化聊天响应"""
    id: str
    timestamp: datetime
    createdAt: datetime = Field(alias="created_at")
    
    # 前端需要的额外字段
    modelName: Optional[str] = Field(None, alias="model_name")
    icon: Optional[str] = None
    expandable: bool = True
    sections: Optional[List[ChatSection]] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, protected_namespaces=())

