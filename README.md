# AI 面试准备助手

帮助求职者准备面试的 AI 应用。

## 项目结构

```
interview-prep-agent/
├── backend/           # 后端服务
│   ├── main.py        # FastAPI 入口
│   └── requirements.txt
├── frontend/          # 前端页面
│   ├── index.html
│   ├── style.css
│   └── app.js
├── docs/              # 申报书
│   └── README.md
└── README.md          # 项目说明
```

## 快速开始

### 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 启动前端

```bash
cd frontend
python -m http.server 8080
```

访问 http://localhost:8080

## 技术栈

- 前端：HTML + CSS + JavaScript
- 后端：FastAPI
- AI：盘古大模型

## 团队

- 刘嘉龙：全栈开发

## 赛程

- 华为 ICT 大赛 · 创新赛 · 赛题一
- 初赛提交：2026-12