# VoiceCare 后端服务

阿尔茨海默病早期风险分层系统 - 后端 API 服务

## 快速开始

### 1. 安装依赖

```bash
cd backend_api
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填写华为云凭证：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 华为云 MaaS
HUAWEI_CLOUD_MAAS_AK=your_maas_ak
HUAWEI_CLOUD_MAAS_SK=your_maas_sk

# 盘古大模型
PANGU_API_KEY=your_pangu_key

# 华为云 OBS
OBS_ACCESS_KEY=your_obs_ak
OBS_SECRET_KEY=your_obs_sk

# 数据库
DB_HOST=your_rds_host.mysql.rds.aliyuncs.com
DB_PASSWORD=your_db_password
```

### 3. 启动服务

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问文档

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 接口文档

### 接口 1：上传音频并触发分析

**POST** `/api/analyze`

**请求**（multipart/form-data）：
- `user_id`: 用户 ID，如 u001
- `task_type`: 任务类型（picture/story/voicemail）
- `audio_file`: 音频文件（wav/mp3）

**响应**：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "risk_level": "medium",
    "score": 0.68,
    "deviation": 0.27,
    "shap_explanation": { "psd": 0.35, "ttr": -0.12 },
    "report_text": "母亲近期停顿变多，建议安排一次社区复核。"
  }
}
```

### 接口 2：获取历史趋势

**GET** `/api/history?user_id=u001`

**响应**：
```json
{
  "code": 200,
  "data": [
    { "date": "2023-10-01", "score": 0.2 },
    { "date": "2023-10-08", "score": 0.5 },
    { "date": "2023-10-15", "score": 0.68 }
  ]
}
```

## 项目结构

```
backend_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # ORM 模型
│   ├── routers/             # 路由
│   ├── services/            # 业务逻辑
│   ├── utils/               # 工具函数
│   └── core/                # 算法集成
├── migrations/              # 数据库建表 SQL
├── tests/                   # 测试
├── requirements.txt         # 依赖
├── .env.example            # 环境变量模板
└── .env                    # 本地环境变量（不提交）
```

## 开发进度

| 模块 | 状态 | 负责人 |
|------|------|--------|
| 基础框架 | ✅ 完成 | 刘嘉龙 |
| 数据库模型 | ✅ 完成 | 刘嘉龙 |
| MaaS 转写 | 🔄 待调试 | 刘嘉龙 |
| 盘古简报 | 🔄 待调试 | 刘嘉龙 |
| 算法集成 | ⏳ 待对接 | 孟浩 |

## 视频录制

开发过程录屏存储路径：`D:\VoiceCare\videos`

录制指南见：`docs/OBS安装与使用指南.md`

## 团队协作

- **分支**：feature-backend（刘嘉龙）
- **合并**：PR 需至少 1 人 approve
- **接口契约**：冻结，修改前必须同步团队

---

开发者：刘嘉龙
最后更新：2026-11-14