"""
模拟交易实现（不调用真实 API）
"""
from typing import Dict, List, Optional
from app.exchange.base import BaseExchange
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class PaperTradingExchange(BaseExchange):
    """模拟交易交易所"""
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__(api_key, secret)
        # 使用 CoinGecko 获取真实市场价格（无地理限制）
        from app.exchange.coingecko import CoinGeckoExchange
        self.exchange = CoinGeckoExchange()
        self.virtual_balance = {'USDT': 10000.0}  # 虚拟余额
        self.virtual_positions = {}  # 虚拟持仓
    
    async def get_ticker(self, symbol: str) -> Dict:
        """获取实时价格（使用 CoinGecko）"""
        try:
            return await self.exchange.get_ticker(symbol)
        except Exception as e:
            logger.error(f"获取价格失败 {symbol}: {e}")
            raise
    
    async def get_multiple_tickers(self, symbols: List[str]) -> Dict[str, Dict]:
        """批量获取价格（使用 CoinGecko）"""
        try:
            return await self.exchange.get_multiple_tickers(symbols)
        except Exception as e:
            logger.error(f"批量获取价格失败: {e}")
            raise
    
    async def create_market_order(
        self,
        symbol: str,
        side: str,
        amount: float,
        leverage: int = 1
    ) -> Dict:
        """创建模拟市价单（不执行真实交易）"""
        try:
            symbol = self.format_symbol(symbol)
            
            # 获取当前市场价格
            ticker = await self.get_ticker(symbol)
            price = ticker['last']
            
            # 计算订单成本
            cost = price * amount
            
            # 模拟订单执行
            order_id = str(uuid.uuid4())
            timestamp = int(datetime.utcnow().timestamp() * 1000)
            
            logger.info(f"模拟交易: {side} {amount} {symbol} @ {price}, 成本: {cost}")
            
            return {
                'id': order_id,
                'symbol': symbol,
                'side': side,
                'price': price,
                'amount': amount,
                'cost': cost,
                'timestamp': timestamp
            }
        except Exception as e:
            logger.error(f"创建模拟订单失败 {symbol} {side} {amount}: {e}")
            raise
    
    async def fetch_balance(self) -> Dict:
        """获取虚拟账户余额"""
        return self.virtual_balance.copy()
    
    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 100
    ) -> List[List]:
        """获取 K 线数据（使用 CoinGecko）"""
        try:
            return await self.exchange.fetch_ohlcv(symbol, timeframe, limit)
        except Exception as e:
            logger.error(f"获取 K 线失败 {symbol}: {e}")
            raise
    
    async def close(self):
        """关闭连接"""
        await self.exchange.close()

