"""
测试真实市场数据获取
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from app.exchange.paper_trading import PaperTradingExchange


async def test_real_market_data():
    """测试获取真实市场数据"""
    
    print("=" * 60)
    print("测试获取真实市场数据（CoinGecko）")
    print("=" * 60)
    print()
    
    # 创建模拟交易所实例（不需要 API 密钥）
    exchange = PaperTradingExchange()
    
    try:
        # 测试 1：获取 BTC 价格
        print("1. 获取 BTC 实时价格...")
        btc_ticker = await exchange.get_ticker("BTC")
        print(f"   ✓ BTC/USDT")
        print(f"     当前价格: ${btc_ticker['last']:,.2f}")
        print(f"     24h 最高: ${btc_ticker['high']:,.2f}")
        print(f"     24h 最低: ${btc_ticker['low']:,.2f}")
        print(f"     买价: ${btc_ticker['bid']:,.2f}")
        print(f"     卖价: ${btc_ticker['ask']:,.2f}")
        print()
        
        # 测试 2：批量获取多个币种
        print("2. 批量获取多个币种价格...")
        symbols = ["BTC", "ETH", "XRP", "SOL", "BNB", "ADA"]
        tickers = await exchange.get_multiple_tickers(symbols)
        
        for symbol in symbols:
            ticker_symbol = f"{symbol}/USDT"
            if ticker_symbol in tickers:
                ticker = tickers[ticker_symbol]
                print(f"   ✓ {symbol:5} ${ticker['last']:>10,.2f}")
        print()
        
        # 测试 3：模拟交易（使用真实价格）
        print("3. 模拟交易（使用真实市场价格）...")
        order = await exchange.create_market_order(
            symbol="BTC",
            side="buy",
            amount=0.01,
            leverage=10
        )
        print(f"   ✓ 模拟买入订单")
        print(f"     订单 ID: {order['id'][:20]}...")
        print(f"     交易对: {order['symbol']}")
        print(f"     方向: {order['side']}")
        print(f"     数量: {order['amount']} BTC")
        print(f"     成交价: ${order['price']:,.2f}")
        print(f"     成本: ${order['cost']:,.2f}")
        print()
        
        # 测试 4：获取 K 线数据
        print("4. 获取 K 线数据...")
        ohlcv = await exchange.fetch_ohlcv("BTC", timeframe="1h", limit=5)
        print(f"   ✓ 获取最近 5 根 1小时 K线")
        for i, candle in enumerate(ohlcv[-3:], 1):
            timestamp, open_price, high, low, close, volume = candle
            print(f"     {i}. 开: ${open_price:,.2f} 高: ${high:,.2f} "
                  f"低: ${low:,.2f} 收: ${close:,.2f}")
        print()
        
        print("=" * 60)
        print("✓ 所有测试通过！")
        print("=" * 60)
        print()
        print("说明:")
        print("- ✓ 使用真实的 CoinGecko 市场数据")
        print("- ✓ 无需 API 密钥（读取公开数据）")
        print("- ✓ 无地理位置限制")
        print("- ✓ 交易是模拟的（不会执行真实订单）")
        print("- ✓ 适合测试和开发")
        print()
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await exchange.close()


async def main():
    await test_real_market_data()


if __name__ == "__main__":
    asyncio.run(main())

