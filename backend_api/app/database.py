"""
数据库连接与模型
刘嘉龙
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from loguru import logger
from app.config import settings

# 数据库连接 URL
DATABASE_URL = f"mysql+mysqlconnector://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明式基类
Base: DeclarativeMeta = declarative_base()


def get_db():
    """获取数据库会话（依赖注入）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库（创建表）"""
    try:
        # 导入所有模型，确保 SQLAlchemy 能识别
        from app.models import user, record, history  # noqa: F401
        
        # 创建表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建/验证完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise