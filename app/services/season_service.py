"""
赛季服务（核心业务逻辑）
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models import Season, SeasonModel, AIModel, ValueHistory
from app.schemas.season import SeasonCreate, SeasonUpdate
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class SeasonService:
    """赛季服务"""
    
    @staticmethod
    def get_all_seasons(
        db: Session,
        status: Optional[str] = None
    ) -> List[Season]:
        """获取所有赛季"""
        query = db.query(Season)
        if status:
            query = query.filter(Season.status == status)
        return query.order_by(Season.created_at.desc()).all()
    
    @staticmethod
    def get_season_by_id(db: Session, season_id: str) -> Optional[Season]:
        """根据 ID 获取赛季"""
        return db.query(Season).options(
            joinedload(Season.season_models).joinedload(SeasonModel.model)
        ).filter(Season.id == season_id).first()
    
    @staticmethod
    def get_active_season(db: Session) -> Optional[Season]:
        """获取当前活跃的赛季"""
        return db.query(Season).filter(Season.status == "active").first()
    
    @staticmethod
    def create_season(db: Session, season_data: SeasonCreate) -> Season:
        """创建赛季"""
        try:
            # 创建赛季
            season = Season(
                id=str(uuid.uuid4()),
                name=season_data.name,
                description=season_data.description,
                initial_capital=season_data.initial_capital,
                start_time=season_data.start_time,
                end_time=season_data.end_time,
                status="pending"
            )
            db.add(season)
            db.flush()
            
            # 为每个模型创建赛季实例
            for model_id in season_data.model_ids:
                model = db.query(AIModel).filter(AIModel.id == model_id).first()
                if not model:
                    logger.warning(f"模型 {model_id} 不存在，跳过")
                    continue
                
                season_model = SeasonModel(
                    id=str(uuid.uuid4()),
                    season_id=season.id,
                    model_id=model_id,
                    initial_value=season_data.initial_capital,
                    current_value=season_data.initial_capital,
                    available_cash=season_data.initial_capital,
                    status="active"
                )
                db.add(season_model)
                
                # 创建初始价值历史记录
                value_history = ValueHistory(
                    season_model_id=season_model.id,
                    timestamp=int(datetime.utcnow().timestamp() * 1000),
                    value=season_data.initial_capital
                )
                db.add(value_history)
            
            db.commit()
            db.refresh(season)
            
            logger.info(f"创建赛季成功: {season.name}")
            return season
            
        except Exception as e:
            logger.error(f"创建赛季失败: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def start_season(db: Session, season_id: str) -> Optional[Season]:
        """启动赛季"""
        season = SeasonService.get_season_by_id(db, season_id)
        if not season:
            return None
        
        if season.status != "pending":
            logger.warning(f"赛季 {season_id} 状态不是 pending，无法启动")
            return None
        
        season.status = "active"
        db.commit()
        db.refresh(season)
        
        logger.info(f"赛季 {season.name} 已启动")
        return season
    
    @staticmethod
    def end_season(db: Session, season_id: str) -> Optional[Season]:
        """结束赛季"""
        season = SeasonService.get_season_by_id(db, season_id)
        if not season:
            return None
        
        season.status = "completed"
        
        # 将所有活跃的模型标记为已完成
        db.query(SeasonModel).filter(
            SeasonModel.season_id == season_id,
            SeasonModel.status == "active"
        ).update({"status": "completed"})
        
        db.commit()
        db.refresh(season)
        
        logger.info(f"赛季 {season.name} 已结束")
        return season
    
    @staticmethod
    def update_season(
        db: Session,
        season_id: str,
        season_data: SeasonUpdate
    ) -> Optional[Season]:
        """更新赛季"""
        season = SeasonService.get_season_by_id(db, season_id)
        if not season:
            return None
        
        update_data = season_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(season, field, value)
        
        db.commit()
        db.refresh(season)
        return season
    
    @staticmethod
    def get_season_leaderboard(db: Session, season_id: str) -> List[SeasonModel]:
        """获取赛季排行榜"""
        season_models = db.query(SeasonModel).options(
            joinedload(SeasonModel.model)
        ).filter(
            SeasonModel.season_id == season_id
        ).order_by(
            SeasonModel.performance.desc()
        ).all()
        
        # 更新排名
        for idx, sm in enumerate(season_models, 1):
            sm.rank = idx
        db.commit()
        
        return season_models
    
    @staticmethod
    def check_and_eliminate_models(db: Session):
        """检查并淘汰资金亏完的模型"""
        season_models = db.query(SeasonModel).filter(
            SeasonModel.status == "active",
            SeasonModel.current_value <= 0
        ).all()
        
        for sm in season_models:
            sm.status = "eliminated"
            sm.eliminated_at = datetime.utcnow()
            logger.info(f"模型 {sm.model_id} 在赛季 {sm.season_id} 中被淘汰")
        
        if season_models:
            db.commit()
    
    @staticmethod
    def check_and_complete_seasons(db: Session):
        """检查并完成到期的赛季"""
        now = datetime.utcnow()
        seasons = db.query(Season).filter(
            Season.status == "active",
            Season.end_time <= now
        ).all()
        
        for season in seasons:
            SeasonService.end_season(db, season.id)

