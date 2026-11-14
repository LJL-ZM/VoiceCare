"""
日志配置
刘嘉龙
"""

import sys
from loguru import logger
from app.config import settings


def setup_logging():
    """配置日志"""
    # 移除默认 handler
    logger.remove()
    
    # 控制台输出
    logger.add(
        sys.stdout,
        level="DEBUG" if settings.debug else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    
    # 文件输出
    logger.add(
        "logs/voicare_{time:YYYY-MM-DD}.log",
        level="INFO",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    return logger


# 初始化日志
logger = setup_logging()