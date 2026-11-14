"""
VoiceCare 后端配置
刘嘉龙
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from loguru import logger


class Settings(BaseSettings):
    """应用配置"""
    
    # 服务配置
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    debug: bool = False
    
    # 华为云 MaaS
    maas_endpoint: str = "https://maas.cn-north-4.myhuaweicloud.com"
    maas_ak: str = ""
    maas_sk: str = ""
    
    # 盘古大模型
    pangu_endpoint: str = "https://pangu.cn-north-4.myhuaweicloud.com"
    pangu_api_key: str = ""
    
    # 华为云 OBS
    obs_endpoint: str = "https://obs.cn-north-4.myhuaweicloud.com"
    obs_ak: str = ""
    obs_sk: str = ""
    obs_bucket: str = "voiccare-audio"
    
    # 数据库
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "voicare"
    db_user: str = "root"
    db_password: str = ""
    
    # 算法阈值
    baseline_threshold: float = 0.3
    medium_threshold: float = 0.5
    high_threshold: float = 0.7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = Settings()