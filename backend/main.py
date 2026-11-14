"""
AI 面试准备助手 - 后端服务
支持多专业面试模拟
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
    description="帮助求职者准备面试的 AI 应用 - 支持多专业",
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
    
    conn.commit()
    conn.close()

init_db()

# 请求模型
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

class Question(BaseModel):
    question: str
    target_company: Optional[str] = None
    major_category: Optional[str] = None
    profile_id: Optional[int] = None

# 专业分类
MAJOR_CATEGORIES = {
    "理工科": ["计算机科学", "电子信息", "机械工程", "土木工程", "化学工程", "材料科学", "数学", "物理学", "生物科学", "环境工程", "航空航天", "软件工程", "通信工程", "自动化"],
    "文史类": ["汉语言文学", "历史学", "哲学", "新闻传播学", "英语", "日语", "法语", "德语", "翻译", "广告学", "广播电视学"],
    "经管类": ["会计学", "金融学", "工商管理", "市场营销", "人力资源管理", "财务管理", "国际经济与贸易", "经济学", "电子商务", "物流管理"],
    "法学类": ["法学", "社会学", "政治学与行政学", "国际政治", "思想政治教育"],
    "教育类": ["教育学", "学前教育", "小学教育", "体育教育", "特殊教育", "教育技术学"],
    "医学类": ["临床医学", "护理学", "药学", "口腔医学", "预防医学", "中医学", "康复治疗学"],
    "艺术类": ["音乐学", "美术学", "艺术设计", "舞蹈学", "戏剧影视文学", "广播电视编导", "动画", "视觉传达设计"],
    "农学类": ["农学", "林学", "动物医学", "园艺", "植物保护", "水产养殖学"],
}

# 通用面试问题
FAQ_GENERAL = {
    "自我介绍": "好的，我来教你如何做自我介绍。自我介绍要简洁有力，包含：基本信息、教育背景、实习/项目经验、为什么选择这个岗位。时长控制在 1-2 分钟。",
    "你的优点是什么": "这个问题要突出与岗位相关的能力。比如：沟通能力强、学习能力强、有责任心、团队协作好。建议准备 2-3 个优点，每个用具体事例说明。",
    "你的缺点是什么": "这个问题要真诚，但要给出改进方案。比如：我有时候过于追求完美，但我正在学习如何平衡效率与质量。避免说与岗位相关的致命缺点。",
    "为什么选择我们公司": "这个问题要展示你对公司的了解。比如：贵公司在行业内的地位、企业文化、发展前景。建议提前研究公司业务和价值观。",
    "你的职业规划是什么": "这个问题要展示你的上进心和规划能力。比如：短期希望在岗位上积累经验，中期希望成为团队骨干，长期希望成为行业专家。",
    "你遇到过什么困难": "这个问题要展示你的解决问题的能力。选择一个真实的困难，说明你是如何分析和解决的。",
    "你还有什么问题要问我": "这个问题要展示你的积极态度。可以问：团队的工作方式、公司的培训体系、岗位的发展空间、晋升机制等。",
}

# 专业相关面试问题
FAQ_MAJOR = {
    # 理工科
    "计算机科学": {
        "技术栈": "请介绍你熟悉的技术栈，以及你在项目中的应用经验。",
        "项目经验": "请详细介绍你做过的一个项目，包括技术选型、遇到的挑战和解决方案。",
        "算法题": "请手写一个快速排序算法，并解释其时间复杂度。",
        "面向对象": "请解释面向对象编程的三大特性：封装、继承、多态。",
    },
    "电子信息": {
        "电路设计": "请介绍你做过的电路设计项目。",
        "信号处理": "请解释傅里叶变换及其在信号处理中的应用。",
        "嵌入式": "你有哪些嵌入式开发经验？用过哪些微控制器？",
    },
    "机械工程": {
        "CAD软件": "你熟练使用哪些 CAD 软件？",
        "机械设计": "请介绍你做过的机械设计项目。",
        "材料选择": "机械设计中如何选择合适的材料？",
    },
    "土木工程": {
        "结构设计": "请介绍你参与过的结构设计项目。",
        "施工管理": "你对施工管理有什么了解？",
        "工程预算": "如何做工程预算和成本控制？",
    },
    # 经管类
    "会计学": {
        "财务报表": "请介绍三大财务报表及其关系。",
        "会计准则": "你了解哪些会计准则？",
        "审计": "你对审计工作有什么了解？",
    },
    "金融学": {
        "金融市场": "请介绍你对金融市场的理解。",
        "风险管理": "如何做风险管理？",
        "投资分析": "请介绍你做过的投资分析案例。",
    },
    "工商管理": {
        "管理理论": "请介绍你熟悉的管理理论。",
        "团队管理": "如何管理一个团队？",
        "战略规划": "如何做企业战略规划？",
    },
    "市场营销": {
        "营销策略": "请介绍一个成功的营销案例。",
        "品牌建设": "如何做品牌建设？",
        "市场调研": "你做过哪些市场调研项目？",
    },
    # 医学类
    "临床医学": {
        "临床经验": "请介绍你的临床实习经历。",
        "病例分析": "请分析一个典型病例。",
        "医患沟通": "如何与患者进行有效沟通？",
    },
    "护理学": {
        "护理操作": "请介绍你掌握的护理操作技能。",
        "急救知识": "你有哪些急救知识和经验？",
        "患者护理": "如何做好患者护理工作？",
    },
    # 教育类
    "教育学": {
        "教学方法": "请介绍你了解的教学方法。",
        "课程设计": "如何设计一门课程？",
        "教育理念": "你的教育理念是什么？",
    },
    "学前教育": {
        "幼儿特点": "请介绍幼儿的年龄特点。",
        "游戏教学": "如何通过游戏进行教学？",
        "家园合作": "如何与家长沟通合作？",
    },
    # 法学类
    "法学": {
        "法律知识": "请介绍你熟悉的法律领域。",
        "案例分析": "请分析一个典型案例。",
        "法律文书": "你写过哪些法律文书？",
    },
    # 文史类
    "汉语言文学": {
        "文学素养": "请介绍你最喜欢的一部文学作品。",
        "写作能力": "你有哪些写作经验？",
        "语文教学": "如何教好语文课？",
    },
    "新闻传播学": {
        "新闻写作": "请展示你的新闻写作能力。",
        "媒体运营": "你有哪些新媒体运营经验？",
        "舆情分析": "如何做舆情分析？",
    },
    # 艺术类
    "艺术设计": {
        "设计作品": "请展示你的设计作品。",
        "设计软件": "你熟练使用哪些设计软件？",
        "设计理念": "你的设计理念是什么？",
    },
    "音乐学": {
        "音乐技能": "请展示你的音乐技能。",
        "音乐教学": "如何教好音乐课？",
        "音乐创作": "你有哪些音乐创作经验？",
    },
}

# 公司定制化答案
COMPANY_SPECIFIC = {
    "华为": {
        "为什么选择我们公司": "华为是全球领先的 ICT 基础设施和智能终端提供商。我非常认同华为'以客户为中心，以奋斗者为本'的价值观。我希望在华为这样技术驱动、充满挑战的环境中成长。",
        "你的优点是什么": "我具备扎实的专业基础和快速学习能力，这与华为'持续学习、持续创新'的理念契合。同时我有良好的团队协作能力。",
    },
    "腾讯": {
        "为什么选择我们公司": "腾讯是中国领先的互联网公司，'用户为本，科技向善'的使命深深吸引了我。我希望在腾讯这样以产品为导向、注重用户体验的环境中，用技术创造社会价值。",
        "你的优点是什么": "我对互联网产品有深入理解，具备产品思维和专业能力的双重优势。这与腾讯'一切以用户价值为依归'的理念高度契合。",
    },
    "阿里": {
        "为什么选择我们公司": "阿里巴巴'让天下没有难做的生意'的使命让我深受触动。我希望在阿里这样以商业创新为核心的公司，用专业能力推动商业进步。",
        "你的优点是什么": "我具备商业敏感度和创新能力，能够理解专业与商业的结合。这与阿里'客户第一、员工第二、股东第三'的价值观高度契合。",
    },
    "字节跳动": {
        "为什么选择我们公司": "字节跳动是全球领先的内容平台公司，'激发创造，丰富生活'的使命让我向往。我希望在字节这样快速迭代、数据驱动的环境中，用专业能力连接用户。",
        "你的优点是什么": "我具备快速学习能力和数据驱动思维，能够适应字节跳动的快速迭代文化。",
    },
}

@app.post("/api/profile")
async def save_profile(profile: UserProfile):
    """保存用户画像"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM user_profile ORDER BY id DESC LIMIT 1")
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE user_profile SET
                school = ?, major = ?, major_category = ?, interests = ?,
                target_company = ?, target_position = ?, expected_salary = ?,
                work_location = ?, industry = ?, experience_years = ?, skills = ?,
                self_evaluation = ?, strengths = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            profile.school, profile.major, profile.major_category, profile.interests,
            profile.target_company, profile.target_position, profile.expected_salary,
            profile.work_location, profile.industry, profile.experience_years,
            profile.skills, profile.self_evaluation, profile.strengths, existing[0]
        ))
        profile_id = existing[0]
    else:
        cursor.execute('''
            INSERT INTO user_profile 
            (school, major, major_category, interests, target_company, target_position,
             expected_salary, work_location, industry, experience_years, skills,
             self_evaluation, strengths)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            profile.school, profile.major, profile.major_category, profile.interests,
            profile.target_company, profile.target_position, profile.expected_salary,
            profile.work_location, profile.industry, profile.experience_years,
            profile.skills, profile.self_evaluation, profile.strengths
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
        columns = ['id', 'school', 'major', 'major_category', 'interests', 'target_company',
                   'target_position', 'expected_salary', 'work_location', 'industry',
                   'experience_years', 'skills', 'self_evaluation', 'strengths', 'created_at', 'updated_at']
        profile = dict(zip(columns, row))
        return {"code": 200, "data": profile}
    
    return {"code": 200, "data": None}

@app.post("/api/ask")
async def ask(question: Question):
    """回答面试问题"""
    target_company = question.target_company
    major_category = question.major_category
    
    # 先检查是否有公司定制答案
    if target_company and target_company in COMPANY_SPECIFIC:
        company_answers = COMPANY_SPECIFIC[target_company]
        for key, value in company_answers.items():
            if key in question.question:
                return {
                    "code": 200,
                    "answer": value,
                    "company": target_company
                }
    
    # 检查专业相关问题
    if major_category and major_category in FAQ_MAJOR:
        major_questions = FAQ_MAJOR[major_category]
        for key, value in major_questions.items():
            if key in question.question:
                return {
                    "code": 200,
                    "answer": value,
                    "major_category": major_category
                }
    
    # 检查通用问题
    for key, value in FAQ_GENERAL.items():
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

@app.get("/api/majors")
async def get_majors():
    """获取专业列表"""
    return {"code": 200, "data": MAJOR_CATEGORIES}

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