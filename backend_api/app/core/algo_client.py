"""
算法服务客户端 - 调用孟浩的 analyze_features()
刘嘉龙
"""

import sys
import os
from loguru import logger

# 添加算法模块路径
# sys.path.append(os.path.join(os.path.dirname(__file__), "../../core_algorithm"))


async def call_analyze_features(text: str, timestamps: list) -> dict:
    """
    调用孟浩的算法分析函数
    
    Args:
        text: 转写文本
        timestamps: 时间戳列表 [{"word": "厨房", "start_ms": 120, "end_ms": 480}]
    
    Returns:
        算法分析结果
    """
    try:
        # TODO: 实际调用孟浩的模块
        # from core_algorithm.feature_extractor import analyze_features
        # result = analyze_features(text, timestamps)
        
        # Mock 数据（开发阶段使用）
        result = {
            "psd": 0.24,
            "ttr": 0.65,
            "pause_count": 7,
            "speech_rate": 2.8,
            "semantic_coherence": 0.82,
            "shap_values": {"psd": 0.35, "ttr": -0.12, "speech_rate": 0.21},
            "baseline_score": 0.41,
            "deviation": 0.27,
            "score": 0.68,
            "risk_level": "medium",
        }
        
        logger.info(f"算法分析完成: risk_level={result['risk_level']}, score={result['score']}")
        return result
        
    except Exception as e:
        logger.error(f"算法调用失败: {e}")
        raise