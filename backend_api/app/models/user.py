"""
用户模型
刘嘉龙
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False, comment="用户ID")
    name = Column(String(100), comment="姓名")
    gender = Column(String(10), comment="性别")
    age = Column(Integer, comment="年龄")
    phone = Column(String(20), comment="手机号")
    emergency_contact = Column(String(100), comment="紧急联系人")
    emergency_phone = Column(String(20), comment="紧急联系人电话")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    __mapper_args__ = {"eager_defaults": True}