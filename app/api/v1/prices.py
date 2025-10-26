"""
加密货币价格 API 端点
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.price_service import PriceService
from app.schemas.price import CryptoPriceResponse
from app.schemas.common import APIResponse
from datetime import datetime

router = APIRouter()


@router.get("/prices", response_model=APIResponse[List[CryptoPriceResponse]])
async def get_prices(db: Session = Depends(get_db)):
    """获取加密货币价格"""
    try:
        prices = PriceService.get_all_prices(db)
        
        # 构建响应数据（兼容前端格式）
        prices_data = []
        for price in prices:
            price_dict = CryptoPriceResponse.model_validate(price).model_dump()
            # 前端期望的字段映射
            price_dict["price_change_percentage_24h"] = price_dict.get("price_change_24h")
            prices_data.append(CryptoPriceResponse(**price_dict))
        
        return APIResponse(
            success=True,
            data=prices_data,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )


@router.get("/prices/{symbol}", response_model=APIResponse[CryptoPriceResponse])
async def get_price(symbol: str, db: Session = Depends(get_db)):
    """获取单个币种价格"""
    try:
        price = PriceService.get_price_by_symbol(db, symbol.upper())
        if not price:
            return APIResponse(
                success=False,
                error={"code": "PRICE_NOT_FOUND", "message": "价格数据不存在"},
                timestamp=datetime.utcnow()
            )
        
        return APIResponse(
            success=True,
            data=CryptoPriceResponse.model_validate(price),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )

