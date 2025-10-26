"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """应用设置"""
    
    # 应用基础配置
    APP_NAME: str = "Alpha Arena API"
    ENV: str = "development"
    API_PORT: int = 3001
    LOG_LEVEL: str = "INFO"
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/alpha_arena"
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS 配置
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # LLM API 密钥
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    MODELSCOPE_API_KEY: str = ""  # 通义千问 (ModelScope API)
    DEEPSEEK_API_KEY: str = ""
    
    # 交易所 API
    BINANCE_API_KEY: str = ""
    BINANCE_SECRET: str = ""
    COINBASE_API_KEY: str = ""
    COINBASE_SECRET: str = ""
    
    # 赛季设置
    DEFAULT_INITIAL_CAPITAL: float = 10000.0
    
    @property
    def cors_origins_list(self) -> List[str]:
        """将 CORS origins 字符串转换为列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取设置实例（单例）"""
    return Settings()


# 全局设置实例
settings = get_settings()

