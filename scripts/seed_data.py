"""
种子数据脚本 - 初始化演示模型和赛季
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, Base, engine
from app.models import AIModel, Season, SeasonModel, ValueHistory
from app.core.config import settings
from app.utils.html_cleaner import clean_prompt_text
from datetime import datetime, timedelta
import uuid

def create_demo_models(db):
    """创建演示模型"""
    models_data = [
        {
            "id": "qwen3-max",
            "name": "qwen3-max",
            "display_name": "QWEN3 MAX",
            "color": "#9370db",
            "icon": "✦",
            "description": "阿里通义千问3 Max，性能卓越",
            "llm_provider": "qwen",
            "llm_model": "Qwen/Qwen3-235B-A22B-Instruct-2507",
            "strategy_prompt": clean_prompt_text("你是一个保守型交易者，偏好做多，杠杆5-10x，只在明确趋势中交易。"),
            "trading_mode": "paper",
            "exchange_name": "binance",
            "execution_interval": 15,
            "status": "active"  # ✓ 激活
        },
        {
            "id": "deepseek-v3",
            "name": "deepseek-v3",
            "display_name": "DEEPSEEK V3",
            "color": "#00bfff",
            "icon": "◇",
            "description": "DeepSeek V3，强大的推理能力",
            "llm_provider": "deepseek",
            "llm_model": "deepseek-chat",
            "strategy_prompt": clean_prompt_text("你是一个理性的量化交易者，基于数据和趋势分析，杠杆5-12x，重视风险控制。"),
            "trading_mode": "paper",
            "exchange_name": "binance",
            "execution_interval": 15,
            "status": "active"  # ✓ 激活
        },
        {
            "id": "gpt-6",
            "name": "gpt-6",
            "display_name": "GPT-6",
            "color": "#00d4aa",
            "icon": "◆",
            "description": "OpenAI GPT-4 Turbo，强大的推理能力",
            "llm_provider": "openai",
            "llm_model": "gpt-4-turbo-preview",
            "strategy_prompt": clean_prompt_text("你是一个平衡型交易者，做多做空都考虑，杠杆5-15x，善于捕捉趋势。"),
            "trading_mode": "paper",
            "exchange_name": "binance",
            "execution_interval": 20,
            "status": "inactive"  # ✗ 未激活
        },
        {
            "id": "claude-opus",
            "name": "claude-opus",
            "display_name": "CLAUDE OPUS",
            "color": "#ffa500",
            "icon": "●",
            "description": "Anthropic Claude 3 Opus，细致的分析能力",
            "llm_provider": "anthropic",
            "llm_model": "claude-3-opus-20240229",
            "strategy_prompt": clean_prompt_text("你是一个激进型交易者，积极做空做多，杠杆10-20x，捕捉短期机会。"),
            "trading_mode": "paper",
            "exchange_name": "binance",
            "execution_interval": 10,
            "status": "inactive"  # ✗ 未激活
        },
        {
            "id": "gemini-ultra",
            "name": "gemini-ultra",
            "display_name": "GEMINI ULTRA",
            "color": "#4285f4",
            "icon": "★",
            "description": "Google Gemini Ultra（模拟）",
            "llm_provider": "openai",  # 使用 OpenAI 替代
            "llm_model": "gpt-4",
            "strategy_prompt": clean_prompt_text("你是一个数据驱动型交易者，基于技术指标，杠杆8-12x。"),
            "trading_mode": "paper",
            "exchange_name": "binance",
            "execution_interval": 15,
            "status": "inactive"  # ✗ 未激活
        },
        {
            "id": "llama3-405b",
            "name": "llama3-405b",
            "display_name": "LLAMA3 405B",
            "color": "#ff6b6b",
            "icon": "▲",
            "description": "Meta Llama 3 405B（模拟）",
            "llm_provider": "anthropic",  # 使用 Claude 替代
            "llm_model": "claude-3-sonnet-20240229",
            "strategy_prompt": clean_prompt_text("你是一个趋势跟随者，只做强趋势，杠杆3-8x，严格止损。"),
            "trading_mode": "paper",
            "exchange_name": "binance",
            "execution_interval": 25,
            "status": "inactive"  # ✗ 未激活
        },
    ]
    
    models = []
    active_models = []
    for model_data in models_data:
        status = model_data.pop("status")
        model = AIModel(**model_data, status=status)
        db.add(model)
        models.append(model)
        if status == "active":
            active_models.append(model)
    
    db.commit()
    print(f"✓ 创建了 {len(models)} 个演示模型")
    print(f"  - 激活模型: {len(active_models)} 个")
    for model in active_models:
        print(f"    • {model.display_name} ({model.llm_provider})")
    print(f"  - 未激活模型: {len(models) - len(active_models)} 个")
    return active_models  # 只返回激活的模型


def create_demo_season(db, models):
    """创建演示赛季"""
    # 创建一个从现在开始的 30 天赛季
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(days=30)
    
    season = Season(
        id=str(uuid.uuid4()),
        name="2025 Q1 Alpha Arena 竞技赛",
        description="首届 AI 交易模型竞技赛：QWEN3 MAX vs DEEPSEEK V3，各自初始资金 $10,000",
        initial_capital=10000.0,
        start_time=start_time,
        end_time=end_time,
        status="active"  # 直接设为活跃
    )
    db.add(season)
    db.flush()
    
    # 为每个模型创建赛季实例
    for model in models:
        season_model = SeasonModel(
            id=str(uuid.uuid4()),
            season_id=season.id,
            model_id=model.id,
            initial_value=10000.0,
            current_value=10000.0,
            available_cash=10000.0,
            performance=0,
            status="active"
        )
        db.add(season_model)
        db.flush()
        
        # 创建初始价值历史
        value_history = ValueHistory(
            season_model_id=season_model.id,
            timestamp=int(start_time.timestamp() * 1000),
            value=10000.0
        )
        db.add(value_history)
    
    db.commit()
    print(f"✓ 创建了赛季: {season.name}")
    print(f"  - 赛季 ID: {season.id}")
    print(f"  - 开始时间: {start_time}")
    print(f"  - 结束时间: {end_time}")
    print(f"  - 参与模型: {len(models)} 个")
    
    return season


def main():
    """主函数"""
    db = SessionLocal()
    
    try:
        print("="* 50)
        print("Alpha Arena 种子数据初始化")
        print("="* 50)
        print()
        
        # 检查是否已有数据
        existing_models = db.query(AIModel).count()
        if existing_models > 0:
            print(f"⚠ 数据库中已有 {existing_models} 个模型")
            
            # Docker 环境中自动清除，本地开发询问
            import os
            is_docker = os.path.exists('/.dockerenv')
            
            if is_docker:
                print("检测到 Docker 环境，自动清除现有数据...")
                response = 'y'
            else:
                response = input("是否清除现有数据并重新初始化？(y/N): ")
            
            if response.lower() != 'y':
                print("取消初始化")
                return
            
            # 清除现有数据
            print("正在清除现有数据...")
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            print("✓ 数据已清除")
            print()
        
        # 创建演示数据
        print("1. 创建演示模型...")
        models = create_demo_models(db)
        print()
        
        print("2. 创建演示赛季...")
        season = create_demo_season(db, models)
        print()
        
        print("="* 50)
        print("✓ 初始化完成！")
        print("="* 50)
        print()
        print("下一步:")
        print("1. 启动 API 服务器: uvicorn app.main:app --reload")
        print("2. 启动 Celery Worker: celery -A app.tasks.celery_app worker --loglevel=info")
        print("3. 启动 Celery Beat: celery -A app.tasks.celery_app beat --loglevel=info")
        print()
        print(f"API 文档: http://localhost:{settings.API_PORT}/docs")
        print()
        
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

