"""
历史趋势接口
刘嘉龙
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from loguru import logger

from app.database import get_db
from app.services.analysis_service import get_user_history


router = APIRouter(prefix="/history", tags=["历史"])


@router.get("", summary="获取用户历史趋势")
async def get_history(
    user_id: str = Query(..., description="用户ID，如 u001"),
    db: Session = Depends(get_db),
):
    """
    获取用户的历史风险分数，用于绘制折线图。
    """
    try:
        history = await get_user_history(db, user_id)
        
        return {
            "code": 200,
            "data": [
                {
                    "date": record["date"],
                    "score": record["score"],
                    "risk_level": record["risk_level"],
                }
                for record in history
            ]
        }
        
    except Exception as e:
        logger.error(f"获取历史失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取历史失败: {str(e)}")