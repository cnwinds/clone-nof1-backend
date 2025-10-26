"""
加密货币价格服务
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import CryptoPrice
from app.exchange.factory import ExchangeFactory
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PriceService:
    """价格服务"""
    
    # 默认跟踪的币种
    DEFAULT_SYMBOLS = ["BTC", "ETH", "XRP", "SOL", "BNB", "ADA"]
    
    @staticmethod
    def get_all_prices(db: Session) -> List[CryptoPrice]:
        """获取所有价格"""
        return db.query(CryptoPrice).all()
    
    @staticmethod
    def get_price_by_symbol(db: Session, symbol: str) -> Optional[CryptoPrice]:
        """根据符号获取价格"""
        return db.query(CryptoPrice).filter(CryptoPrice.symbol == symbol).first()
    
    @staticmethod
    async def update_crypto_prices(db: Session, symbols: Optional[List[str]] = None):
        """更新加密货币价格"""
        try:
            symbols = symbols or PriceService.DEFAULT_SYMBOLS
            
            # 使用模拟交易获取价格（无需 API 密钥）
            exchange = ExchangeFactory.create_exchange("binance", "paper")
            tickers = await exchange.get_multiple_tickers(symbols)
            await exchange.close()
            
            now = datetime.utcnow()
            
            for symbol in symbols:
                ticker_symbol = f"{symbol}/USDT"
                if ticker_symbol not in tickers:
                    continue
                
                ticker = tickers[ticker_symbol]
                
                # 查找或创建价格记录
                price_record = PriceService.get_price_by_symbol(db, symbol)
                
                if price_record:
                    # 更新现有记录
                    price_record.current_price = ticker["last"]
                    price_record.high_24h = ticker.get("high")
                    price_record.low_24h = ticker.get("low")
                    price_record.last_updated = now
                else:
                    # 创建新记录
                    price_record = CryptoPrice(
                        id=f"{symbol.lower()}-usd",
                        symbol=symbol,
                        name=symbol,  # 简化处理
                        current_price=ticker["last"],
                        high_24h=ticker.get("high"),
                        low_24h=ticker.get("low"),
                        last_updated=now
                    )
                    db.add(price_record)
            
            db.commit()
            logger.info(f"更新了 {len(symbols)} 个币种的价格")
            
        except Exception as e:
            logger.error(f"更新价格失败: {e}")
            db.rollback()

