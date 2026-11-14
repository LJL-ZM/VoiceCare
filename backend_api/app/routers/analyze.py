"""
分析接口 - 上传音频并触发分析
刘嘉龙
"""

import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from loguru import logger

from app.database import get_db
from app.services.audio_service import upload_to_obs
from app.services.maas_service import transcribe_audio
from app.services.pangu_service import generate_report
from app.services.analysis_service import process_analysis
from app.core.algo_client import call_analyze_features


router = APIRouter(prefix="/analyze", tags=["分析"])


@router.post("", summary="上传音频并触发分析")
async def analyze_audio(
    user_id: str = Form(..., description="用户ID，如 u001"),
    task_type: str = Form(..., description="任务类型：picture/story/voicemail"),
    audio_file: UploadFile = File(..., description="音频文件 wav/mp3"),
    db: Session = Depends(get_db),
):
    """
    上传音频文件，触发语音分析并返回风险分层结果。
    
    **流程**：
    1. 上传音频到 OBS
    2. 调用 MaaS 转写
    3. 调用算法模块分析特征
    4. 调用盘古大模型生成简报
    5. 保存到数据库
    6. 返回结果
    """
    try:
        # 1. 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as tmp:
            content = await audio_file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        logger.info(f"收到音频文件: user_id={user_id}, task_type={task_type}, 文件大小={len(content)} bytes")
        
        # 2. 上传到 OBS
        audio_path = await upload_to_obs(tmp_path, user_id, task_type)
        logger.info(f"音频已上传 OBS: {audio_path}")
        
        # 3. 调用 MaaS 转写
        text, timestamps = await transcribe_audio(tmp_path)
        logger.info(f"转写完成: text_length={len(text)}, timestamps_count={len(timestamps)}")
        
        # 4. 调用算法分析
        algo_result = await call_analyze_features(text, timestamps)
        logger.info(f"算法分析完成: risk_level={algo_result.get('risk_level')}, score={algo_result.get('score')}")
        
        # 5. 调用盘古生成简报
        report_text = await generate_report(algo_result, text)
        logger.info("简报生成完成")
        
        # 6. 保存到数据库
        result = await process_analysis(
            db=db,
            user_id=user_id,
            task_type=task_type,
            audio_path=audio_path,
            text=text,
            timestamps=timestamps,
            algo_result=algo_result,
            report_text=report_text,
        )
        
        # 7. 清理临时文件
        os.unlink(tmp_path)
        
        return {
            "code": 200,
            "msg": "success",
            "data": {
                "risk_level": algo_result["risk_level"],
                "score": algo_result["score"],
                "deviation": algo_result["deviation"],
                "shap_explanation": algo_result["shap_values"],
                "report_text": report_text,
            }
        }
        
    except Exception as e:
        logger.error(f"分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")