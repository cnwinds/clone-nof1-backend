"""
FastAPI 主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import models, seasons, trades, positions, chats, prices
import logging

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Alpha Arena 多模型加密货币交易竞技场后端 API"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(models.router, prefix="/api", tags=["models"])
app.include_router(seasons.router, prefix="/api", tags=["seasons"])
app.include_router(trades.router, prefix="/api", tags=["trades"])
app.include_router(positions.router, prefix="/api", tags=["positions"])
app.include_router(chats.router, prefix="/api", tags=["chats"])
app.include_router(prices.router, prefix="/api", tags=["prices"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Alpha Arena API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)

