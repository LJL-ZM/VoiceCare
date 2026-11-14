"""
AI 面试准备助手 - 后端服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
import os

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

# 数据库初始化
DB_PATH = "interview_prep.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 用户画像表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school TEXT,
            major TEXT,
            interests TEXT,
            target_company TEXT,
            target_position TEXT,
            expected_salary TEXT,
            work_location TEXT,
            industry TEXT,
            experience_years INTEGER,
            skills TEXT,
            self_evaluation TEXT,
            strengths TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 面试记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER,
            question TEXT,
            answer TEXT,
            score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES user_profile (id)
        )
    ''')
    
    # 面试评分表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER,
            overall_score INTEGER,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES user_profile (id)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# 请求模型
class UserProfile(BaseModel):
    school: Optional[str] = ""
    major: Optional[str] = ""
    interests: Optional[str] = ""
    target_company: Optional[str] = ""
    target_position: Optional[str] = ""
    expected_salary: Optional[str] = ""
    work_location: Optional[str] = ""
    industry: Optional[str] = ""
    experience_years: Optional[int] = 0
    skills: Optional[str] = ""
    self_evaluation: Optional[str] = ""
    strengths: Optional[str] = ""

class Question(BaseModel):
    question: str
    target_company: Optional[str] = None
    profile_id: Optional[int] = None

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

# 公司定制化答案
COMPANY_SPECIFIC = {
    "华为": {
        "为什么选择我们公司": "华为是全球领先的 ICT 基础设施和智能终端提供商。我非常认同华为'以客户为中心，以奋斗者为本'的价值观。我希望在华为这样技术驱动、充满挑战的环境中成长，为通信技术的发展贡献力量。",
        "你的优点是什么": "我具备扎实的技术基础和快速学习能力，这与华为'持续学习、持续创新'的理念契合。同时我有良好的团队协作能力，能够适应华为的奋斗文化。",
        "你的职业规划是什么": "短期希望在华为的技术岗位上深耕，成为某一领域的专家；中期希望参与重大项目，积累项目管理经验；长期希望成为技术架构师或团队负责人。",
    },
    "腾讯": {
        "为什么选择我们公司": "腾讯是中国领先的互联网公司，'用户为本，科技向善'的使命深深吸引了我。我希望在腾讯这样以产品为导向、注重用户体验的环境中，用技术创造社会价值。",
        "你的优点是什么": "我对互联网产品有深入理解，具备产品思维和技术能力的双重优势。这与腾讯'一切以用户价值为依归'的理念高度契合。",
        "你的职业规划是什么": "短期希望深入了解腾讯的产品体系和技术栈；中期希望参与核心产品的开发；长期希望成为产品技术负责人。",
    },
    "阿里": {
        "为什么选择我们公司": "阿里巴巴'让天下没有难做的生意'的使命让我深受触动。我希望在阿里这样以商业创新为核心的公司，用技术推动商业进步。",
        "你的优点是什么": "我具备商业敏感度和技术创新能力，能够理解技术与商业的结合。这与阿里'客户第一、员工第二、股东第三'的价值观高度契合。",
        "你的职业规划是什么": "短期希望深入理解阿里的商业生态；中期希望参与核心商业项目；长期希望成为商业技术专家。",
    },
    "字节跳动": {
        "为什么选择我们公司": "字节跳动是全球领先的内容平台公司，'激发创造，丰富生活'的使命让我向往。我希望在字节这样快速迭代、数据驱动的环境中，用技术连接用户。",
        "你的优点是什么": "我具备快速学习能力和数据驱动思维，能够适应字节跳动的快速迭代文化。同时我对内容产品有深入理解。",
        "你的职业规划是什么": "短期希望掌握字节的技术栈和产品方法论；中期希望参与核心内容产品的开发；长期希望成为技术负责人。",
    },
}

@app.post("/api/profile")
async def save_profile(profile: UserProfile):
    """保存用户画像"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查是否已有画像
    cursor.execute("SELECT id FROM user_profile ORDER BY id DESC LIMIT 1")
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE user_profile SET
                school = ?, major = ?, interests = ?, target_company = ?,
                target_position = ?, expected_salary = ?, work_location = ?,
                industry = ?, experience_years = ?, skills = ?,
                self_evaluation = ?, strengths = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            profile.school, profile.major, profile.interests, profile.target_company,
            profile.target_position, profile.expected_salary, profile.work_location,
            profile.industry, profile.experience_years, profile.skills,
            profile.self_evaluation, profile.strengths, existing[0]
        ))
        profile_id = existing[0]
    else:
        cursor.execute('''
            INSERT INTO user_profile 
            (school, major, interests, target_company, target_position, expected_salary,
             work_location, industry, experience_years, skills, self_evaluation, strengths)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            profile.school, profile.major, profile.interests, profile.target_company,
            profile.target_position, profile.expected_salary, profile.work_location,
            profile.industry, profile.experience_years, profile.skills,
            profile.self_evaluation, profile.strengths
        ))
        profile_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return {"code": 200, "message": "保存成功", "profile_id": profile_id}

@app.get("/api/profile")
async def get_profile():
    """获取用户画像"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        columns = ['id', 'school', 'major', 'interests', 'target_company', 'target_position',
                   'expected_salary', 'work_location', 'industry', 'experience_years',
                   'skills', 'self_evaluation', 'strengths', 'created_at', 'updated_at']
        profile = dict(zip(columns, row))
        return {"code": 200, "data": profile}
    
    return {"code": 200, "data": None}

@app.post("/api/ask")
async def ask(question: Question):
    """回答面试问题"""
    target_company = question.target_company
    
    # 先检查是否有公司定制答案
    if target_company and target_company in COMPANY_SPECIFIC:
        company_answers = COMPANY_SPECIFIC[target_company]
        for key, value in company_answers.items():
            if key in question.question:
                # 保存记录
                if question.profile_id:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO interview_records (profile_id, question, answer, score)
                        VALUES (?, ?, ?, ?)
                    ''', (question.profile_id, question.question, value, 90))
                    conn.commit()
                    conn.close()
                
                return {
                    "code": 200,
                    "answer": value,
                    "company": target_company
                }
    
    # 再检查是否在 FAQ 中
    for key, value in FAQ.items():
        if key in question.question:
            return {
                "code": 200,
                "answer": value
            }
    
    # 如果不在 FAQ 中，返回通用回答
    return {
        "code": 200,
        "answer": f"这是一个很好的问题！关于这个问题，我建议你可以从以下几个方面思考：\n1. 问题的核心是什么\n2. 你有哪些相关经验\n3. 你打算如何解决\n\n如果你正在准备{target_company or '目标公司'}的面试，可以告诉我更多细节，我会给出更具体的建议。"
    }

@app.get("/api/history")
async def get_history(profile_id: int = None):
    """获取面试历史"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if profile_id:
        cursor.execute('''
            SELECT question, answer, score, created_at 
            FROM interview_records 
            WHERE profile_id = ? 
            ORDER BY created_at DESC 
            LIMIT 20
        ''', (profile_id,))
    else:
        cursor.execute('''
            SELECT question, answer, score, created_at 
            FROM interview_records 
            ORDER BY created_at DESC 
            LIMIT 20
        ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "question": row[0],
            "answer": row[1],
            "score": row[2],
            "created_at": row[3]
        })
    
    return {"code": 200, "data": history}

@app.get("/api/health")
async def health():
    """健康检查"""
    return {"status": "ok"}