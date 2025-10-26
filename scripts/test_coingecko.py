"""
快速测试 CoinGecko API（验证地理限制问题已解决）
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from app.exchange.coingecko import CoinGeckoExchange


async def main():
    print("🔍 测试 CoinGecko API 连接...")
    print("=" * 60)
    print()
    
    exchange = CoinGeckoExchange()
    
    try:
        # 测试获取 BTC 价格
        print("1️⃣  获取 BTC 价格...")
        btc = await exchange.get_ticker("BTC")
        print(f"   ✅ 成功！BTC 当前价格: ${btc['last']:,.2f}")
        print()
        
        # 测试批量获取
        print("2️⃣  批量获取 6 个币种...")
        symbols = ["BTC", "ETH", "XRP", "SOL", "BNB", "ADA"]
        tickers = await exchange.get_multiple_tickers(symbols)
        print(f"   ✅ 成功！获取了 {len(tickers)} 个币种")
        
        for symbol in symbols:
            key = f"{symbol}/USDT"
            if key in tickers:
                price = tickers[key]['last']
                print(f"      • {symbol}: ${price:,.2f}")
        print()
        
        print("=" * 60)
        print("🎉 测试通过！CoinGecko API 工作正常")
        print("=" * 60)
        print()
        print("✅ 无地理限制问题")
        print("✅ 无需 API 密钥")
        print("✅ 获取真实市场数据")
        print()
        print("现在可以启动完整系统了:")
        print("  1. docker-compose up -d mysql redis")
        print("  2. alembic upgrade head")
        print("  3. python scripts/seed_data.py")
        print("  4. uvicorn app.main:app --reload --port 3001")
        print()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()
        print("可能的原因:")
        print("  1. 网络连接问题")
        print("  2. CoinGecko API 暂时不可用")
        print("  3. 请求频率过高（等待1分钟后重试）")
        print()
        import traceback
        traceback.print_exc()
        
    finally:
        await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())

