"""
分析记录模型
刘嘉龙
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class AnalysisRecord(Base):
    """分析记录表"""
    __tablename__ = "analysis_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), index=True, nullable=False, comment="用户ID")
    task_type = Column(String(20), nullable=False, comment="任务类型")
    audio_path = Column(String(500), comment="音频存储路径(OBS)")
    audio_duration = Column(Float, comment="音频时长(秒)")
    text = Column(Text, comment="转写文本")
    
    # 特征指标
    psd = Column(Float, comment="静默时间占比")
    ttr = Column(Float, comment="词汇多样性")
    pause_count = Column(Integer, comment="停顿次数")
    speech_rate = Column(Float, comment="语速(字/秒)")
    semantic_coherence = Column(Float, comment="语义连贯性")
    
    # 风险评分
    score = Column(Float, comment="风险评分")
    deviation = Column(Float, comment="相对基线偏离度")
    baseline_score = Column(Float, comment="历史基线分数")
    risk_level = Column(String(20), comment="风险等级")
    
    # SHAP 归因
    shap_values = Column(JSON, comment="SHAP 特征归因")
    
    # 简报
    report_text = Column(Text, comment="Agent 简报文本")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    __mapper_args__ = {"eager_defaults": True}