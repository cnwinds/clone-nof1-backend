"""
AI 模型服务
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import AIModel
from app.schemas.model import AIModelCreate, AIModelUpdate
import uuid


class ModelService:
    """AI 模型服务"""
    
    @staticmethod
    def get_all_models(db: Session) -> List[AIModel]:
        """获取所有模型"""
        return db.query(AIModel).all()
    
    @staticmethod
    def get_active_models(db: Session) -> List[AIModel]:
        """获取激活的模型（参与交易的模型）"""
        return db.query(AIModel).filter(AIModel.status == "active").all()
    
    @staticmethod
    def get_model_by_id(db: Session, model_id: str) -> Optional[AIModel]:
        """根据 ID 获取模型"""
        return db.query(AIModel).filter(AIModel.id == model_id).first()
    
    @staticmethod
    def get_model_by_name(db: Session, name: str) -> Optional[AIModel]:
        """根据名称获取模型"""
        return db.query(AIModel).filter(AIModel.name == name).first()
    
    @staticmethod
    def create_model(db: Session, model_data: AIModelCreate) -> AIModel:
        """创建模型"""
        model = AIModel(
            id=str(uuid.uuid4()),
            **model_data.model_dump()
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    
    @staticmethod
    def update_model(
        db: Session,
        model_id: str,
        model_data: AIModelUpdate
    ) -> Optional[AIModel]:
        """更新模型"""
        model = ModelService.get_model_by_id(db, model_id)
        if not model:
            return None
        
        update_data = model_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        
        db.commit()
        db.refresh(model)
        return model
    
    @staticmethod
    def delete_model(db: Session, model_id: str) -> bool:
        """删除模型"""
        model = ModelService.get_model_by_id(db, model_id)
        if not model:
            return False
        
        db.delete(model)
        db.commit()
        return True

