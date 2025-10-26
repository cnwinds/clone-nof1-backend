"""
交易所工厂
"""
from typing import Optional
from app.exchange.base import BaseExchange
from app.exchange.binance import BinanceExchange
from app.exchange.coinbase import CoinbaseExchange
from app.exchange.paper_trading import PaperTradingExchange
from app.core.config import settings


class ExchangeFactory:
    """交易所工厂类"""
    
    @staticmethod
    def create_exchange(
        exchange_name: str,
        trading_mode: str,
        api_key: Optional[str] = None,
        secret: Optional[str] = None
    ) -> BaseExchange:
        """
        创建交易所实例
        
        Args:
            exchange_name: 交易所名称 (binance/coinbase)
            trading_mode: 交易模式 (paper/real)
            api_key: API 密钥（真实交易时需要）
            secret: API 密钥（真实交易时需要）
            
        Returns:
            BaseExchange 实例
        """
        # 模拟交易模式
        if trading_mode == "paper":
            return PaperTradingExchange()
        
        # 真实交易模式
        if exchange_name == "binance":
            api_key = api_key or settings.BINANCE_API_KEY
            secret = secret or settings.BINANCE_SECRET
            return BinanceExchange(api_key, secret)
        
        elif exchange_name == "coinbase":
            api_key = api_key or settings.COINBASE_API_KEY
            secret = secret or settings.COINBASE_SECRET
            return CoinbaseExchange(api_key, secret)
        
        else:
            raise ValueError(f"不支持的交易所: {exchange_name}")

