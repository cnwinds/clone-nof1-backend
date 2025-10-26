"""
策略执行任务
"""
from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models import Season, SeasonModel, ValueHistory
from app.strategy.llm_strategy import LLMStrategy
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.strategy_runner.run_all_strategies")
def run_all_strategies():
    """运行所有活跃赛季的策略"""
    db = SessionLocal()
    try:
        # 获取所有活跃的赛季
        active_seasons = db.query(Season).filter(Season.status == "active").all()
        
        logger.info(f"找到 {len(active_seasons)} 个活跃赛季")
        
        for season in active_seasons:
            # 获取该赛季的所有活跃模型
            season_models = db.query(SeasonModel).filter(
                SeasonModel.season_id == season.id,
                SeasonModel.status == "active"
            ).all()
            
            logger.info(f"赛季 {season.name} 有 {len(season_models)} 个活跃模型")
            
            for sm in season_models:
                try:
                    # 检查是否到了执行时间
                    # 简化：每次都执行（实际可以根据 execution_interval 判断）
                    logger.info(f"执行策略: 赛季={season.name}, 模型={sm.model.display_name}")
                    
                    # 创建策略实例并执行
                    strategy = LLMStrategy(db)
                    result = asyncio.run(strategy.execute(sm.id))
                    
                    if result["success"]:
                        logger.info(f"策略执行成功: {result['message']}")
                    else:
                        logger.warning(f"策略执行失败: {result['message']}")
                    
                except Exception as e:
                    logger.error(f"执行策略失败 {sm.id}: {e}")
                    continue
        
        return {"success": True, "message": f"处理了 {len(active_seasons)} 个赛季"}
        
    except Exception as e:
        logger.error(f"运行策略任务失败: {e}")
        return {"success": False, "message": str(e)}
    finally:
        db.close()


@celery_app.task(name="app.tasks.strategy_runner.record_value_history")
def record_value_history():
    """记录所有活跃模型的价值历史"""
    db = SessionLocal()
    try:
        # 获取所有活跃的赛季模型
        season_models = db.query(SeasonModel).filter(
            SeasonModel.status == "active"
        ).all()
        
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        
        for sm in season_models:
            try:
                # 创建价值历史记录
                value_history = ValueHistory(
                    season_model_id=sm.id,
                    timestamp=timestamp,
                    value=sm.current_value
                )
                db.add(value_history)
            except Exception as e:
                logger.error(f"记录价值历史失败 {sm.id}: {e}")
                continue
        
        db.commit()
        logger.info(f"记录了 {len(season_models)} 个模型的价值历史")
        
        return {"success": True, "count": len(season_models)}
        
    except Exception as e:
        logger.error(f"记录价值历史任务失败: {e}")
        db.rollback()
        return {"success": False, "message": str(e)}
    finally:
        db.close()

