"""
策略基础类
"""
from abc import ABC, abstractmethod
from typing import Dict, List
from sqlalchemy.orm import Session


class BaseStrategy(ABC):
    """交易策略基础抽象类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    async def execute(self, season_model_id: str) -> Dict:
        """
        执行策略
        
        Args:
            season_model_id: 赛季模型实例 ID
            
        Returns:
            {
                "success": bool,
                "message": str,
                "trades": List[Dict]
            }
        """
        pass
    
    @abstractmethod
    async def analyze_market(self, symbols: List[str]) -> Dict:
        """
        分析市场
        
        Args:
            symbols: 交易对列表
            
        Returns:
            市场分析结果
        """
        pass

