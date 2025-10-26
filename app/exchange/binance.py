"""
Binance 交易所实现
"""
import ccxt.async_support as ccxt
from typing import Dict, List, Optional
from app.exchange.base import BaseExchange
import logging

logger = logging.getLogger(__name__)


class BinanceExchange(BaseExchange):
    """Binance 交易所"""
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__(api_key, secret)
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',  # 使用期货合约
            }
        })
    
    async def get_ticker(self, symbol: str) -> Dict:
        """获取实时价格"""
        try:
            symbol = self.format_symbol(symbol)
            ticker = await self.exchange.fetch_ticker(symbol)
            return {
                'symbol': ticker['symbol'],
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high': ticker['high'],
                'low': ticker['low'],
                'volume': ticker['baseVolume'],
                'timestamp': ticker['timestamp']
            }
        except Exception as e:
            logger.error(f"获取价格失败 {symbol}: {e}")
            raise
    
    async def get_multiple_tickers(self, symbols: List[str]) -> Dict[str, Dict]:
        """批量获取价格"""
        try:
            formatted_symbols = [self.format_symbol(s) for s in symbols]
            tickers = await self.exchange.fetch_tickers(formatted_symbols)
            
            result = {}
            for symbol, ticker in tickers.items():
                result[symbol] = {
                    'symbol': ticker['symbol'],
                    'last': ticker['last'],
                    'bid': ticker['bid'],
                    'ask': ticker['ask'],
                    'high': ticker['high'],
                    'low': ticker['low'],
                    'volume': ticker['baseVolume'],
                    'timestamp': ticker['timestamp']
                }
            return result
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
        """创建市价单"""
        try:
            symbol = self.format_symbol(symbol)
            
            # 设置杠杆
            if leverage > 1:
                await self.exchange.set_leverage(leverage, symbol)
            
            # 创建订单
            order = await self.exchange.create_market_order(symbol, side, amount)
            
            return {
                'id': order['id'],
                'symbol': order['symbol'],
                'side': order['side'],
                'price': order.get('price', order.get('average', 0)),
                'amount': order['amount'],
                'cost': order['cost'],
                'timestamp': order['timestamp']
            }
        except Exception as e:
            logger.error(f"创建订单失败 {symbol} {side} {amount}: {e}")
            raise
    
    async def fetch_balance(self) -> Dict:
        """获取账户余额"""
        try:
            balance = await self.exchange.fetch_balance()
            return balance['total']
        except Exception as e:
            logger.error(f"获取余额失败: {e}")
            raise
    
    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 100
    ) -> List[List]:
        """获取 K 线数据"""
        try:
            symbol = self.format_symbol(symbol)
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            logger.error(f"获取 K 线失败 {symbol}: {e}")
            raise
    
    async def close(self):
        """关闭连接"""
        await self.exchange.close()

