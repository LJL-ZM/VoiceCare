"""
分析业务逻辑服务
刘嘉龙
"""

from datetime import datetime
from sqlalchemy.orm import Session
from loguru import logger
from app.models.record import AnalysisRecord


async def process_analysis(
    db: Session,
    user_id: str,
    task_type: str,
    audio_path: str,
    text: str,
    timestamps: list,
    algo_result: dict,
    report_text: str,
) -> dict:
    """
    保存分析结果到数据库
    """
    try:
        record = AnalysisRecord(
            user_id=user_id,
            task_type=task_type,
            audio_path=audio_path,
            text=text,
            psd=algo_result.get("psd"),
            ttr=algo_result.get("ttr"),
            pause_count=algo_result.get("pause_count"),
            speech_rate=algo_result.get("speech_rate"),
            semantic_coherence=algo_result.get("semantic_coherence"),
            score=algo_result.get("score"),
            deviation=algo_result.get("deviation"),
            baseline_score=algo_result.get("baseline_score"),
            risk_level=algo_result.get("risk_level"),
            shap_values=algo_result.get("shap_values"),
            report_text=report_text,
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        logger.info(f"分析结果已保存: record_id={record.id}")
        return {"id": record.id, **algo_result}
        
    except Exception as e:
        db.rollback()
        logger.error(f"保存分析结果失败: {e}")
        raise


async def get_user_history(db: Session, user_id: str) -> list:
    """
    获取用户历史风险分数
    """
    try:
        records = db.query(AnalysisRecord).filter(
            AnalysisRecord.user_id == user_id
        ).order_by(AnalysisRecord.created_at.asc()).all()
        
        return [
            {
                "date": record.created_at.strftime("%Y-%m-%d"),
                "score": record.score,
                "risk_level": record.risk_level,
            }
            for record in records
        ]
        
    except Exception as e:
        logger.error(f"获取历史记录失败: {e}")
        raise