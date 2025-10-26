"""
自动化聊天 API 端点
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models import AutomatedChat, SeasonModel
from app.schemas.chat import AutomatedChatResponse, ChatSection
from app.schemas.common import APIResponse
from datetime import datetime

router = APIRouter()


@router.get("/automated-chats", response_model=APIResponse[List[AutomatedChatResponse]])
async def get_chats(
    season_id: Optional[str] = Query(None, description="赛季 ID"),
    model_id: Optional[str] = Query(None, description="模型 ID"),
    limit: int = Query(50, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """获取自动化聊天记录"""
    try:
        query = db.query(AutomatedChat).join(SeasonModel)
        
        if season_id:
            query = query.filter(SeasonModel.season_id == season_id)
        
        if model_id:
            query = query.filter(SeasonModel.model_id == model_id)
        
        chats = query.order_by(AutomatedChat.timestamp.desc()).limit(limit).all()
        
        # 构建响应数据
        chats_data = []
        for chat in chats:
            chat_dict = AutomatedChatResponse.model_validate(chat).model_dump()
            chat_dict["model_name"] = chat.season_model.model.display_name
            chat_dict["icon"] = chat.season_model.model.icon
            
            # 构建可展开的 sections
            sections = [
                ChatSection(
                    type="USER_PROMPT",
                    content=chat.user_prompt or "",
                    expanded=False
                ),
                ChatSection(
                    type="CHAIN_OF_THOUGHT",
                    content=chat.chain_of_thought or "",
                    expanded=False
                ),
                ChatSection(
                    type="TRADING_DECISIONS",
                    content=chat.trading_decisions or [],
                    expanded=False
                )
            ]
            chat_dict["sections"] = sections
            chat_dict["expandable"] = True
            
            chats_data.append(AutomatedChatResponse(**chat_dict))
        
        return APIResponse(
            success=True,
            data=chats_data,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )

