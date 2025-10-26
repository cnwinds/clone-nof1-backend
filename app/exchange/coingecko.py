"""
CoinGecko 价格数据源（无地理限制）
"""
import httpx
from typing import Dict, List, Optional
from app.exchange.base import BaseExchange
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class CoinGeckoExchange(BaseExchange):
    """CoinGecko 数据源（用于获取价格，不支持交易）"""
    
    # CoinGecko 币种 ID 映射
    SYMBOL_MAP = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "XRP": "ripple",
        "SOL": "solana",
        "BNB": "binancecoin",
        "ADA": "cardano",
        "DOGE": "dogecoin",
        "DOT": "polkadot",
        "MATIC": "matic-network",
        "AVAX": "avalanche-2",
    }
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        super().__init__(api_key, secret)
        self.base_url = "https://api.coingecko.com/api/v3"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _get_coin_id(self, symbol: str) -> str:
        """获取 CoinGecko 币种 ID"""
        symbol = symbol.replace("/USDT", "").replace("/USD", "").upper()
        return self.SYMBOL_MAP.get(symbol, symbol.lower())
    
    async def get_ticker(self, symbol: str) -> Dict:
        """获取实时价格（从 CoinGecko）"""
        try:
            coin_id = self._get_coin_id(symbol)
            
            # 调用 CoinGecko API
            url = f"{self.base_url}/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_last_updated_at": "true"
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if coin_id not in data:
                raise ValueError(f"未找到币种: {symbol}")
            
            coin_data = data[coin_id]
            price = coin_data.get("usd", 0)
            
            # 获取更详细的数据（包含高低点）
            detail_url = f"{self.base_url}/coins/{coin_id}"
            detail_params = {
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "false",
                "developer_data": "false"
            }
            
            detail_response = await self.client.get(detail_url, params=detail_params)
            detail_data = detail_response.json()
            
            market_data = detail_data.get("market_data", {})
            
            return {
                'symbol': f"{symbol.upper()}/USDT",
                'last': price,
                'bid': price * 0.9999,  # 模拟买价（略低）
                'ask': price * 1.0001,  # 模拟卖价（略高）
                'high': market_data.get("high_24h", {}).get("usd", price * 1.05),
                'low': market_data.get("low_24h", {}).get("usd", price * 0.95),
                'volume': coin_data.get("usd_24h_vol", 0),
                'timestamp': coin_data.get("last_updated_at", int(datetime.utcnow().timestamp())) * 1000
            }
            
        except Exception as e:
            logger.error(f"获取价格失败 {symbol}: {e}")
            raise
    
    async def get_multiple_tickers(self, symbols: List[str]) -> Dict[str, Dict]:
        """批量获取价格"""
        try:
            # 转换为 CoinGecko ID
            coin_ids = [self._get_coin_id(s) for s in symbols]
            
            # 批量获取价格
            url = f"{self.base_url}/simple/price"
            params = {
                "ids": ",".join(coin_ids),
                "vs_currencies": "usd",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_last_updated_at": "true"
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            result = {}
            for symbol, coin_id in zip(symbols, coin_ids):
                if coin_id in data:
                    coin_data = data[coin_id]
                    price = coin_data.get("usd", 0)
                    
                    ticker_symbol = f"{symbol.upper()}/USDT"
                    result[ticker_symbol] = {
                        'symbol': ticker_symbol,
                        'last': price,
                        'bid': price * 0.9999,
                        'ask': price * 1.0001,
                        'high': price * 1.05,  # 简化处理
                        'low': price * 0.95,
                        'volume': coin_data.get("usd_24h_vol", 0),
                        'timestamp': coin_data.get("last_updated_at", int(datetime.utcnow().timestamp())) * 1000
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
        """创建模拟市价单"""
        try:
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
                'symbol': f"{symbol}/USDT",
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
        return {'USDT': 10000.0}
    
    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = '1h',
        limit: int = 100
    ) -> List[List]:
        """获取 K 线数据（简化实现）"""
        try:
            coin_id = self._get_coin_id(symbol)
            
            # CoinGecko 提供的历史数据（天级别）
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": "7",  # 最近7天
                "interval": "hourly"
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            prices = data.get("prices", [])
            
            # 转换为 OHLCV 格式 [timestamp, open, high, low, close, volume]
            ohlcv = []
            for i, price_point in enumerate(prices[-limit:]):
                timestamp, price = price_point
                ohlcv.append([
                    timestamp,
                    price,  # open
                    price * 1.01,  # high (简化)
                    price * 0.99,  # low (简化)
                    price,  # close
                    0  # volume (CoinGecko 单独提供)
                ])
            
            return ohlcv
            
        except Exception as e:
            logger.error(f"获取 K 线失败 {symbol}: {e}")
            raise
    
    async def close(self):
        """关闭连接"""
        await self.client.aclose()

