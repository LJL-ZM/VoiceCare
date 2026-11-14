"""
MaaS 语音转写服务
刘嘉龙
"""

import json
from loguru import logger
from app.config import settings

# TODO: 华为云 MaaS SDK
# from huaweicloudsdkcore.auth.credentials import BasicCredentials
# from huaweicloudsdkcore.region.region import Region
# from huaweicloudsdkmaas.v2 import MaasClient, RecognizeAudioRequest, RecognizeAudioReq


async def transcribe_audio(audio_path: str) -> tuple[str, list]:
    """
    调用 MaaS 语音转写接口
    
    Args:
        audio_path: 音频文件路径
    
    Returns:
        (转写文本, 时间戳列表)
        timestamps 格式: [{"word": "厨房", "start_ms": 120, "end_ms": 480}]
    """
    try:
        # TODO: 实际 MaaS 调用
        # credentials = BasicCredentials(settings.maas_ak, settings.maas_sk)
        # client = MaasClient.new_builder() \
        #     .with_credentials(credentials) \
        #     .with_region(Region.value_of("cn-north-4")) \
        #     .build()
        # 
        # request = RecognizeAudioRequest()
        # request.body = RecognizeAudioReq(
        #     audio_url=audio_path,
        #     format="wav",
        #     need_word_info=True
        # )
        # response = client.recognize_audio(request)
        # 
        # text = response.result.text
        # timestamps = [
        #     {"word": w.word, "start_ms": w.start_ms, "end_ms": w.end_ms}
        #     for w in response.result.word_info
        # ]
        
        # Mock 数据（开发阶段使用）
        text = "这是一个厨房，厨房里有冰箱、灶台和水槽。"
        timestamps = [
            {"word": "这是", "start_ms": 100, "end_ms": 500},
            {"word": "一个", "start_ms": 550, "end_ms": 800},
            {"word": "厨房", "start_ms": 850, "end_ms": 1200},
            {"word": "厨房", "start_ms": 1300, "end_ms": 1600},
            {"word": "里", "start_ms": 1650, "end_ms": 1750},
            {"word": "有", "start_ms": 1800, "end_ms": 2000},
            {"word": "冰箱", "start_ms": 2100, "end_ms": 2500},
            {"word": "灶台", "start_ms": 2600, "end_ms": 3000},
            {"word": "和", "start_ms": 3100, "end_ms": 3200},
            {"word": "水槽", "start_ms": 3300, "end_ms": 3700},
        ]
        
        logger.info(f"MaaS 转写完成: text_length={len(text)}")
        return text, timestamps
        
    except Exception as e:
        logger.error(f"MaaS 转写失败: {e}")
        raise