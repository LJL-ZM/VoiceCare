"""
VoiceCare 后端服务 - 主入口
刘嘉龙 - 华为云后端开发
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.routers import analyze, history
from app.database import init_db
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("VoiceCare 后端服务启动中...")
    logger.info(f"环境: {'开发' if settings.DEBUG else '生产'}")
    
    # 初始化数据库
    init_db()
    logger.info("数据库初始化完成")
    
    yield
    
    logger.info("VoiceCare 后端服务关闭")


app = FastAPI(
    title="VoiceCare API",
    description="阿尔茨海默病早期风险分层系统 - 后端服务",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(analyze.router, prefix="/api", tags=["分析"])
app.include_router(history.router, prefix="/api", tags=["历史"])


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "VoiceCare Backend",
        "version": "1.0.0"
    }


@app.get("/", tags=["根路径"])
async def root():
    """根路径重定向到健康检查"""
    return {
        "message": "VoiceCare API 服务",
        "docs": "/docs",
        "health": "/health"
    }