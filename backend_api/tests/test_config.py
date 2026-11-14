"""
配置文件测试
"""

import pytest
from app.config import Settings


def test_settings_default():
    """测试默认配置"""
    settings = Settings()
    assert settings.server_port == 8000
    assert settings.debug is False


def test_settings_thresholds():
    """测试阈值配置"""
    settings = Settings()
    assert settings.baseline_threshold == 0.3
    assert settings.medium_threshold == 0.5
    assert settings.high_threshold == 0.7