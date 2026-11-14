"""
AI 面试准备助手 - 后端服务
支持多专业面试模拟 + 用户认证 + 公司推荐
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta

app = FastAPI(
    title="AI 面试准备助手",
    description="帮助求职者准备面试的 AI 应用 - 支持多专业 + 用户认证",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 安全配置
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
security = HTTPBearer()

# 数据库初始化
DB_PATH = "interview_prep.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 用户画像表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            school TEXT,
            major TEXT,
            major_category TEXT,
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
            target_city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 面试记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question TEXT,
            answer TEXT,
            score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 公司推荐表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            industry TEXT NOT NULL,
            description TEXT,
            website TEXT,
            logo_url TEXT
        )
    ''')
    
    # 初始化公司数据
    cursor.execute("SELECT COUNT(*) FROM companies")
    if cursor.fetchone()[0] == 0:
        companies_data = [
            ("华为技术有限公司", "深圳", "互联网/通信", "全球领先的ICT基础设施和智能终端提供商", "https://www.huawei.com", ""),
            ("腾讯", "深圳", "互联网", "中国领先的互联网公司", "https://www.tencent.com", ""),
            ("阿里巴巴", "杭州", "互联网/电商", "让天下没有难做的生意", "https://www.alibaba.com", ""),
            ("字节跳动", "北京", "互联网/内容", "激发创造，丰富生活", "https://www.bytedance.com", ""),
            ("百度", "北京", "互联网/AI", "用科技让复杂的世界更简单", "https://www.baidu.com", ""),
            ("美团", "北京", "互联网/O2O", "帮大家吃得更好，生活更好", "https://www.meituan.com", ""),
            ("京东", "北京", "互联网/电商", "多快好省", "https://www.jd.com", ""),
            ("网易", "广州", "互联网/游戏", "游戏热爱者", "https://www.163.com", ""),
            ("小米", "北京", "智能硬件", "让每个人都能享受科技的乐趣", "https://www.mi.com", ""),
            ("滴滴出行", "北京", "互联网/出行", "让出行更美好", "https://www.didiglobal.com", ""),
            ("快手", "北京", "互联网/内容", "用技术提升每一个人独特的幸福感", "https://www.kuaishou.com", ""),
            ("携程", "上海", "互联网/旅游", "携程在手，说走就走", "https://www.ctrip.com", ""),
            ("哔哩哔哩", "上海", "互联网/内容", "你感兴趣的视频都在B站", "https://www.bilibili.com", ""),
            ("拼多多", "上海", "互联网/电商", "多实惠，多乐趣", "https://www.pinduoduo.com", ""),
            ("小红书", "上海", "互联网/内容", "标记我的生活", "https://www.xiaohongshu.com", ""),
            ("知乎", "北京", "互联网/内容", "有问题，上知乎", "https://www.zhihu.com", ""),
            ("联想", "北京", "智能硬件/计算机", "智能，为每一个可能", "https://www.lenovo.com", ""),
            ("OPPO", "东莞", "智能硬件", "至美科技", "https://www.oppo.com", ""),
            ("vivo", "东莞", "智能硬件", "让科技至简至美", "https://www.vivo.com", ""),
            ("大疆创新", "深圳", "智能硬件/无人机", "未来无所不能", "https://www.dji.com", ""),
            ("招商银行", "深圳", "金融", "招商银行，因您而变", "https://www.cmbchina.com", ""),
            ("平安银行", "深圳", "金融", "平安银行，真的不一样", "https://bank.pingan.com", ""),
            ("中信证券", "深圳", "金融", "中国领先的证券公司", "https://www.cs.ecitic.com", ""),
            ("万科", "深圳", "房地产", "万科，让建筑赞美生命", "https://www.vanke.com", ""),
            ("比亚迪", "深圳", "新能源汽车", "用技术创新，满足人们对美好生活的向往", "https://www.byd.com", ""),
            ("宁德时代", "宁德", "新能源", "创新，引领新能源未来", "https://www.catl.com", ""),
            ("药明康德", "上海", "医药/生物", "让天下没有难做的药", "https://www.wuxiapptec.com", ""),
            ("恒瑞医药", "连云港", "医药", "专注创新，守护健康", "https://www.hrs.com.cn", ""),
            ("迈瑞医疗", "深圳", "医疗设备", "成为守护人类健康的核心力量", "https://www.mindray.com", ""),
            ("新东方", "北京", "教育", "教育改变命运", "https://www.xdf.cn", ""),
            ("好未来", "北京", "教育", "用科技推动教育进步", "https://www.100tal.com", ""),
            ("中公教育", "北京", "教育", "让每个人都有更好的职业发展", "https://www.offcn.com", ""),
        ]
        
        cursor.executemany('''
            INSERT INTO companies (name, city, industry, description, website, logo_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', companies_data)
    
    conn.commit()
    conn.close()

init_db()

# 请求模型
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    school: Optional[str] = ""
    major: Optional[str] = ""
    major_category: Optional[str] = ""
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
    target_city: Optional[str] = ""

class Question(BaseModel):
    question: str
    target_company: Optional[str] = None
    major_category: Optional[str] = None

# 工具函数
def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(plain_password) == hashed_password

def create_token(user_id: int) -> str:
    """创建 JWT Token"""
    import jwt
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[int]:
    """验证 JWT Token"""
    import jwt
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """获取当前用户 ID"""
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user_id

# 专业分类
MAJOR_CATEGORIES = {
    "理工科": ["计算机科学", "电子信息", "机械工程", "土木工程", "化学工程", "材料科学", "数学", "物理学", "生物科学", "环境工程", "软件工程", "通信工程", "自动化"],
    "文史类": ["汉语言文学", "历史学", "哲学", "新闻传播学", "英语", "日语", "翻译", "广告学"],
    "经管类": ["会计学", "金融学", "工商管理", "市场营销", "人力资源管理", "财务管理", "国际经济与贸易", "经济学"],
    "法学类": ["法学", "社会学", "政治学与行政学", "思想政治教育"],
    "教育类": ["教育学", "学前教育", "小学教育", "体育教育", "教育技术学"],
    "医学类": ["临床医学", "护理学", "药学", "口腔医学", "预防医学", "中医学"],
    "艺术类": ["音乐学", "美术学", "艺术设计", "舞蹈学", "戏剧影视文学", "视觉传达设计"],
    "农学类": ["农学", "林学", "动物医学", "园艺", "植物保护"],
}

# 面试问题库
FAQ_GENERAL = {
    "自我介绍": "好的，我来教你如何做自我介绍。自我介绍要简洁有力，包含：基本信息、教育背景、实习/项目经验、为什么选择这个岗位。时长控制在 1-2 分钟。",
    "你的优点是什么": "这个问题要突出与岗位相关的能力。比如：沟通能力强、学习能力强、有责任心、团队协作好。建议准备 2-3 个优点，每个用具体事例说明。",
    "你的缺点是什么": "这个问题要真诚，但要给出改进方案。比如：我有时候过于追求完美，但我正在学习如何平衡效率与质量。避免说与岗位相关的致命缺点。",
    "为什么选择我们公司": "这个问题要展示你对公司的了解。比如：贵公司在行业内的地位、企业文化、发展前景。建议提前研究公司业务和价值观。",
    "你的职业规划是什么": "这个问题要展示你的上进心和规划能力。比如：短期希望在岗位上积累经验，中期希望成为团队骨干，长期希望成为行业专家。",
    "你遇到过什么困难": "这个问题要展示你的解决问题的能力。选择一个真实的困难，说明你是如何分析和解决的。",
    "你还有什么问题要问我": "这个问题要展示你的积极态度。可以问：团队的工作方式、公司的培训体系、岗位的发展空间、晋升机制等。",
}

FAQ_MAJOR = {
    "计算机科学": {
        "技术栈": "请介绍你熟悉的技术栈，以及你在项目中的应用经验。",
        "项目经验": "请详细介绍你做过的一个项目，包括技术选型、遇到的挑战和解决方案。",
        "算法题": "请手写一个快速排序算法，并解释其时间复杂度。",
    },
    "会计学": {
        "财务报表": "请介绍三大财务报表及其关系。",
        "会计准则": "你了解哪些会计准则？",
    },
    "教育学": {
        "教学方法": "请介绍你了解的教学方法。",
        "课程设计": "如何设计一门课程？",
    },
}

# 公司定制答案
COMPANY_SPECIFIC = {
    "华为": {
        "为什么选择我们公司": "华为是全球领先的ICT基础设施和智能终端提供商。我非常认同华为'以客户为中心，以奋斗者为本'的价值观。",
    },
    "腾讯": {
        "为什么选择我们公司": "腾讯是中国领先的互联网公司，'用户为本，科技向善'的使命深深吸引了我。",
    },
}

# API 路由
@app.post("/api/register")
async def register(user: UserRegister):
    """用户注册"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查用户名是否已存在
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (user.username, user.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    
    # 创建用户
    password_hash = hash_password(user.password)
    cursor.execute('''
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    ''', (user.username, user.email, password_hash))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"code": 200, "message": "注册成功", "user_id": user_id}

@app.post("/api/login")
async def login(user: UserLogin):
    """用户登录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (user.username,))
    result = cursor.fetchone()
    conn.close()
    
    if not result or not verify_password(user.password, result[1]):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    token = create_token(result[0])
    return {"code": 200, "message": "登录成功", "token": token, "user_id": result[0]}

@app.get("/api/me")
async def get_me(user_id: int = Depends(get_current_user)):
    """获取当前用户信息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {"code": 200, "data": {"id": user[0], "username": user[1], "email": user[2]}}

@app.post("/api/profile")
async def save_profile(profile: UserProfile, user_id: int = Depends(get_current_user)):
    """保存用户画像"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM user_profile WHERE user_id = ?", (user_id,))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE user_profile SET
                school = ?, major = ?, major_category = ?, interests = ?,
                target_company = ?, target_position = ?, expected_salary = ?,
                work_location = ?, industry = ?, experience_years = ?, skills = ?,
                self_evaluation = ?, strengths = ?, target_city = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (
            profile.school, profile.major, profile.major_category, profile.interests,
            profile.target_company, profile.target_position, profile.expected_salary,
            profile.work_location, profile.industry, profile.experience_years,
            profile.skills, profile.self_evaluation, profile.strengths, profile.target_city,
            user_id
        ))
    else:
        cursor.execute('''
            INSERT INTO user_profile 
            (user_id, school, major, major_category, interests, target_company, target_position,
             expected_salary, work_location, industry, experience_years, skills,
             self_evaluation, strengths, target_city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, profile.school, profile.major, profile.major_category, profile.interests,
            profile.target_company, profile.target_position, profile.expected_salary,
            profile.work_location, profile.industry, profile.experience_years,
            profile.skills, profile.self_evaluation, profile.strengths, profile.target_city
        ))
    
    conn.commit()
    conn.close()
    
    return {"code": 200, "message": "保存成功"}

@app.get("/api/profile")
async def get_profile(user_id: int = Depends(get_current_user)):
    """获取用户画像"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT school, major, major_category, interests, target_company, target_position,
               expected_salary, work_location, industry, experience_years, skills,
               self_evaluation, strengths, target_city
        FROM user_profile WHERE user_id = ?
    ''', (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        columns = ['school', 'major', 'major_category', 'interests', 'target_company',
                   'target_position', 'expected_salary', 'work_location', 'industry',
                   'experience_years', 'skills', 'self_evaluation', 'strengths', 'target_city']
        profile = dict(zip(columns, row))
        return {"code": 200, "data": profile}
    
    return {"code": 200, "data": None}

@app.post("/api/ask")
async def ask(question: Question, user_id: int = Depends(get_current_user)):
    """回答面试问题"""
    # 先检查是否有公司定制答案
    if question.target_company and question.target_company in COMPANY_SPECIFIC:
        for key, value in COMPANY_SPECIFIC[question.target_company].items():
            if key in question.question:
                return {"code": 200, "answer": value}
    
    # 检查专业相关问题
    if question.major_category and question.major_category in FAQ_MAJOR:
        major_questions = FAQ_MAJOR[question.major_category]
        for key, value in major_questions.items():
            if key in question.question:
                return {"code": 200, "answer": value}
    
    # 检查通用问题
    for key, value in FAQ_GENERAL.items():
        if key in question.question:
            return {"code": 200, "answer": value}
    
    return {"code": 200, "answer": f"这是一个很好的问题！建议从以下几个方面思考：\n1. 问题的核心是什么\n2. 你有哪些相关经验\n3. 你打算如何解决"}

@app.get("/api/companies/recommend")
async def recommend_companies(city: str = "", industry: str = "", user_id: int = Depends(get_current_user)):
    """推荐公司"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT name, city, industry, description, website FROM companies WHERE 1=1"
    params = []
    
    if city:
        query += " AND city LIKE ?"
        params.append(f"%{city}%")
    
    if industry:
        query += " AND industry LIKE ?"
        params.append(f"%{industry}%")
    
    query += " LIMIT 10"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    companies = []
    for row in rows:
        companies.append({
            "name": row[0],
            "city": row[1],
            "industry": row[2],
            "description": row[3],
            "website": row[4]
        })
    
    return {"code": 200, "data": companies}

@app.get("/api/majors")
async def get_majors():
    """获取专业列表"""
    return {"code": 200, "data": MAJOR_CATEGORIES}

@app.get("/api/history")
async def get_history(user_id: int = Depends(get_current_user)):
    """获取面试历史"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT question, answer, score, created_at 
        FROM interview_records 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 20
    ''', (user_id,))
    
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