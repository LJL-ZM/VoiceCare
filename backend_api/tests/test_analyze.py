"""
分析接口测试
刘嘉龙
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "VoiceCare" in response.json()["message"]


def test_analyze_without_file():
    """测试缺少音频文件"""
    response = client.post("/api/analyze", data={"user_id": "u001", "task_type": "picture"})
    assert response.status_code == 422  # 缺少文件，验证错误


def test_analyze_mock():
    """测试分析接口（Mock）"""
    # 模拟音频文件
    import io
    audio_content = b"fake audio content"
    
    response = client.post(
        "/api/analyze",
        data={"user_id": "u001", "task_type": "picture"},
        files={"audio_file": ("test.wav", audio_content, "audio/wav")},
    )
    
    # 由于是 Mock，预期返回成功
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "data" in data
    assert "risk_level" in data["data"]


def test_history():
    """测试历史趋势接口"""
    response = client.get("/api/history?user_id=u001")
    assert response.status_code == 200
    assert response.json()["code"] == 200