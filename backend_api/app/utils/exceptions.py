"""
自定义异常
刘嘉龙
"""


class VoiceCareException(Exception):
    """VoiceCare 基础异常"""
    pass


class AudioUploadException(VoiceCareException):
    """音频上传异常"""
    pass


class TranscriptionException(VoiceCareException):
    """语音转写异常"""
    pass


class AnalysisException(VoiceCareException):
    """分析异常"""
    pass


class ReportGenerationException(VoiceCareException):
    """简报生成异常"""
    pass