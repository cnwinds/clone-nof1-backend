"""
赛季监控任务
"""
from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.services.season_service import SeasonService
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.season_monitor.check_season_status")
def check_season_status():
    """检查赛季状态"""
    db = SessionLocal()
    try:
        # 检查并完成到期的赛季
        SeasonService.check_and_complete_seasons(db)
        
        # 检查并淘汰资金亏完的模型
        SeasonService.check_and_eliminate_models(db)
        
        # 更新排名
        active_seasons = SeasonService.get_all_seasons(db, status="active")
        for season in active_seasons:
            SeasonService.get_season_leaderboard(db, season.id)
        
        return {"success": True, "message": "赛季状态检查完成"}
        
    except Exception as e:
        logger.error(f"赛季监控任务失败: {e}")
        return {"success": False, "message": str(e)}
    finally:
        db.close()

