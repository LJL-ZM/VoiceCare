# AI 面试准备助手

帮助求职者准备面试的 AI 应用。

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
uvicorn main:app --reload --port 8000
```

### 3. 访问文档

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 接口文档

### 提问接口

**POST** `/ask`

**请求：**
```json
{
  "question": "如何做自我介绍"
}
```

**响应：**
```json
{
  "code": 200,
  "answer": "好的，我来教你如何做自我介绍..."
}
```

## 项目结构

```
backend/
├── main.py           # FastAPI 入口
└── requirements.txt  # 依赖
```