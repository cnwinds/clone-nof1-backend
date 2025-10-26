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


@router.get("/prices")
async def get_prices(db: Session = Depends(get_db)):
    """获取加密货币价格"""
    try:
        prices = PriceService.get_all_prices(db)
        
        # 构建响应数据
        prices_data = []
        for price in prices:
            price_dict = CryptoPriceResponse.model_validate(price).model_dump(by_alias=False)
            prices_data.append(price_dict)
        
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


@router.get("/prices/{symbol}")
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
            data=CryptoPriceResponse.model_validate(price).model_dump(by_alias=False),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)},
            timestamp=datetime.utcnow()
        )

