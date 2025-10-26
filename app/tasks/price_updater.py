"""
价格更新任务
"""
from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.services.price_service import PriceService
from app.services.position_service import PositionService
import logging
import asyncio

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.price_updater.update_crypto_prices")
def update_crypto_prices():
    """更新加密货币价格"""
    db = SessionLocal()
    try:
        asyncio.run(PriceService.update_crypto_prices(db))
        return {"success": True, "message": "价格更新成功"}
    except Exception as e:
        logger.error(f"更新价格任务失败: {e}")
        return {"success": False, "message": str(e)}
    finally:
        db.close()


@celery_app.task(name="app.tasks.price_updater.update_positions_prices")
def update_positions_prices():
    """更新所有持仓的当前价格"""
    db = SessionLocal()
    try:
        asyncio.run(PositionService.update_positions_prices(db))
        return {"success": True, "message": "持仓价格更新成功"}
    except Exception as e:
        logger.error(f"更新持仓价格任务失败: {e}")
        return {"success": False, "message": str(e)}
    finally:
        db.close()

