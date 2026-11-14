"""
盘古大模型简报生成服务
刘嘉龙
"""

import json
from loguru import logger
from app.config import settings

# TODO: 盘古大模型 API
# import requests


async def generate_report(algo_result: dict, text: str) -> str:
    """
    调用盘古大模型生成大白话简报
    
    Args:
        algo_result: 算法分析结果
        text: 转写文本
    
    Returns:
        简报文本
    """
    try:
        risk_level = algo_result.get("risk_level", "unknown")
        score = algo_result.get("score", 0)
        deviation = algo_result.get("deviation", 0)
        shap_values = algo_result.get("shap_values", {})
        
        # 构建 Prompt
        prompt = f"""
你是一个阿尔茨海默病早期筛查的 AI 助手。根据以下分析结果，生成一段大白话简报给老人的子女。

**分析结果**：
- 风险等级：{risk_level}
- 风险评分：{score}
- 相对基线偏离度：{deviation}
- 主要特征贡献：{json.dumps(shap_values, ensure_ascii=False)}
- 老人本次语音内容：{text}

**要求**：
1. 用通俗易懂的语言，避免专业术语
2. 给出具体建议（如"建议安排一次社区复核"）
3. 语气温暖，不要引起恐慌
4. 控制在 100 字以内

**输出格式**：
直接输出简报文本，不要有其他内容。
"""
        
        # TODO: 实际盘古 API 调用
        # response = requests.post(
        #     settings.pangu_endpoint,
        #     headers={"Authorization": f"Bearer {settings.pangu_api_key}"},
        #     json={"prompt": prompt}
        # )
        # report_text = response.json()["result"]
        
        # Mock 数据（开发阶段使用）
        if risk_level == "low":
            report_text = "母亲近期表现稳定，各项指标都在正常范围内。继续保持每天几分钟的语音交流，我们持续监测就好。"
        elif risk_level == "medium":
            report_text = "母亲近期停顿变多，词汇多样性有些下降。建议安排一次社区复核，早发现早干预，不用太担心。"
        else:
            report_text = "母亲近期变化比较明显，建议尽快到正规医院做一次专业评估。我们一起陪伴她，积极面对。"
        
        logger.info(f"简报生成完成: risk_level={risk_level}")
        return report_text
        
    except Exception as e:
        logger.error(f"简报生成失败: {e}")
        raise