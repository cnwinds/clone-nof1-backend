"""
交易所基础接口
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from decimal import Decimal


class BaseExchange(ABC):
    """交易所基础抽象类"""
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        self.api_key = api_key
        self.secret = secret
    
    @abstractmethod
    async def get_ticker(self, symbol: str) -> Dict:
        """
        获取实时价格
        
        Returns:
            {
                'symbol': 'BTC/USDT',
                'last': 45000.0,
                'bid': 44999.0,
                'ask': 45001.0,
                'high': 46000.0,
                'low': 44000.0,
                'volume': 1234.56
            }
        """
        pass
    
    @abstractmethod
    async def get_multiple_tickers(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        批量获取价格
        
        Returns:
            {
                'BTC/USDT': {...},
                'ETH/USDT': {...}
            }
        """
        pass
    
    @abstractmethod
    async def create_market_order(
        self,
        symbol: str,
        side: str,
        amount: float,
        leverage: int = 1
    ) -> Dict:
        """
        创建市价单
        
        Args:
            symbol: 交易对，如 'BTC/USDT'
            side: 'buy' 或 'sell'
            amount: 数量
            leverage: 杠杆倍数
            
        Returns:
            {
                'id': 'order_123',
                'symbol': 'BTC/USDT',
                'side': 'buy',
                'price': 45000.0,
                'amount': 0.1,
                'cost': 4500.0,
                'timestamp': 1234567890
            }
        """
        pass
    
    @abstractmethod
    async def fetch_balance(self) -> Dict:
        """
        获取账户余额
        
        Returns:
            {
                'USDT': {
                    'free': 10000.0,
                    'used': 5000.0,
                    'total': 15000.0
                }
            }
        """
        pass
    
    @abstractmethod
    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 100
    ) -> List[List]:
        """
        获取 K 线数据
        
        Args:
            symbol: 交易对
            timeframe: 时间周期，如 '1m', '5m', '1h', '1d'
            limit: 数量限制
            
        Returns:
            [
                [timestamp, open, high, low, close, volume],
                ...
            ]
        """
        pass
    
    def format_symbol(self, symbol: str) -> str:
        """
        格式化交易对符号
        BTC -> BTC/USDT
        """
        if '/' in symbol:
            return symbol
        return f"{symbol}/USDT"

