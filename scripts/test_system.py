"""
系统测试脚本 - 验证核心功能
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from app.core.database import SessionLocal
from app.models import Season, SeasonModel
from app.strategy.llm_strategy import LLMStrategy
from app.services.price_service import PriceService
from app.services.position_service import PositionService


async def test_price_update():
    """测试价格更新"""
    print("测试 1: 价格更新...")
    db = SessionLocal()
    try:
        await PriceService.update_crypto_prices(db)
        prices = PriceService.get_all_prices(db)
        print(f"  ✓ 成功更新 {len(prices)} 个币种价格")
        for price in prices[:3]:
            print(f"    - {price.symbol}: ${price.current_price}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    finally:
        db.close()


async def test_strategy_execution():
    """测试策略执行"""
    print("\n测试 2: 策略执行...")
    db = SessionLocal()
    try:
        # 获取第一个活跃的赛季模型
        season_model = db.query(SeasonModel).filter(
            SeasonModel.status == "active"
        ).first()
        
        if not season_model:
            print("  ⚠ 没有找到活跃的赛季模型，请先运行 seed_data.py")
            return
        
        print(f"  执行模型: {season_model.model.display_name}")
        
        strategy = LLMStrategy(db)
        result = await strategy.execute(season_model.id)
        
        if result["success"]:
            print(f"  ✓ {result['message']}")
        else:
            print(f"  ⚠ {result['message']}")
            
    except Exception as e:
        print(f"  ✗ 失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


async def test_position_update():
    """测试持仓更新"""
    print("\n测试 3: 持仓价格更新...")
    db = SessionLocal()
    try:
        await PositionService.update_positions_prices(db)
        print("  ✓ 持仓价格更新成功")
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    finally:
        db.close()


def test_database_connection():
    """测试数据库连接"""
    print("测试 0: 数据库连接...")
    db = SessionLocal()
    try:
        seasons = db.query(Season).all()
        models = db.query(SeasonModel).all()
        print(f"  ✓ 数据库连接成功")
        print(f"    - 赛季数: {len(seasons)}")
        print(f"    - 模型实例数: {len(models)}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")
    finally:
        db.close()


async def main():
    print("=" * 50)
    print("Alpha Arena 系统测试")
    print("=" * 50)
    print()
    
    # 测试数据库连接
    test_database_connection()
    
    # 测试价格更新
    await test_price_update()
    
    # 测试策略执行（可选，需要 LLM API 密钥）
    print("\n⚠ 策略执行测试需要配置 LLM API 密钥")
    response = input("是否测试策略执行？(y/N): ")
    if response.lower() == 'y':
        await test_strategy_execution()
    
    # 测试持仓更新
    await test_position_update()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

