"""
AI 面试准备助手 - 后端服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="AI 面试准备助手",
    description="帮助求职者准备面试的 AI 应用",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

# 预设常见面试问题答案
FAQ = {
    "自我介绍": "好的，我来教你如何做自我介绍。自我介绍要简洁有力，包含：基本信息、教育背景、工作经验、为什么选择我们公司。时长控制在 1-2 分钟。",
    "你的优点是什么": "这个问题要突出与岗位相关的能力。比如：沟通能力强、学习能力强、有责任心。建议准备 2-3 个优点，每个用具体事例说明。",
    "你的缺点是什么": "这个问题要真诚，但要给出改进方案。比如：我有时候过于追求完美，但我正在学习如何平衡效率与质量。避免说与岗位相关的致命缺点。",
    "为什么选择我们公司": "这个问题要展示你对公司的了解。比如：贵公司在行业内的地位、企业文化、发展前景。建议提前研究公司业务和价值观。",
    "你的职业规划是什么": "这个问题要展示你的上进心和规划能力。比如：短期希望在岗位上积累经验，中期希望成为团队骨干，长期希望成为行业专家。",
    "你遇到过什么困难": "这个问题要展示你的解决问题的能力。选择一个真实的困难，说明你是如何分析和解决的。",
    "你还有什么问题要问我": "这个问题要展示你的积极态度。可以问：团队的工作方式、公司的培训体系、岗位的发展空间等。",
}

@app.post("/ask")
async def ask(question: Question):
    """
    回答面试问题
    """
    # 先检查是否在 FAQ 中
    for key, value in FAQ.items():
        if key in question.question:
            return {
                "code": 200,
                "answer": value
            }
    
    # 如果不在 FAQ 中，返回通用回答
    return {
        "code": 200,
        "answer": "这是一个很好的问题！关于这个问题，我建议你可以从以下几个方面思考：\n1. 问题的核心是什么\n2. 你有哪些相关经验\n3. 你打算如何解决\n\n如果你需要更具体的建议，可以告诉我更多细节。"
    }

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI 面试准备助手 API",
        "docs": "/docs",
        "health": "/health"
    }