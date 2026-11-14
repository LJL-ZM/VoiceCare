const API_BASE_URL = 'http://localhost:8000';
let currentProfile = null;
let currentPage = 'home';
let token = localStorage.getItem('token') || null;
let userId = localStorage.getItem('user_id') || null;

// 页面模板
const pages = {
    home: `
        <div class="card">
            <div class="card-header">
                <h2>🎯 欢迎使用 AI 面试准备助手</h2>
            </div>
            <p style="color: var(--text-secondary); margin-top: 10px;">帮助你准备面试，提升求职成功率</p>
            <p style="color: var(--text-tertiary); margin-top: 8px; font-size: 13px;">支持理工科、文史类、经管类、法学类、教育类、医学类、艺术类、农学类等专业</p>
        </div>
        
        <div class="home-cards">
            <div class="home-card" onclick="navigateTo('profile')">
                <div class="icon">👤</div>
                <h3>我的画像</h3>
                <p>配置你的个人信息和求职目标，获取定制化面试建议</p>
            </div>
            
            <div class="home-card" onclick="navigateTo('chat')">
                <div class="icon">💬</div>
                <h3>面试对话</h3>
                <p>与 AI 对话，练习常见面试问题，获取针对性建议</p>
            </div>
            
            <div class="home-card" onclick="navigateTo('companies')">
                <div class="icon">🏢</div>
                <h3>公司推荐</h3>
                <p>根据目标城市和行业，为你推荐优质公司</p>
            </div>
            
            <div class="home-card" onclick="navigateTo('history')">
                <div class="icon">📋</div>
                <h3>历史记录</h3>
                <p>查看之前的面试练习记录，回顾和改进</p>
            </div>
        </div>
        
        <div class="card" style="margin-top: 24px;">
            <div class="card-header">
                <h2>💡 使用指南</h2>
            </div>
            <ul style="line-height: 2; color: var(--text-secondary); font-size: 14px;">
                <li>1. 先注册/登录账号</li>
                <li>2. 在「我的画像」中配置你的专业和求职目标</li>
                <li>3. 在「面试对话」中练习面试问题</li>
                <li>4. 在「公司推荐」中查看适合你的公司</li>
            </ul>
        </div>
    `,

    login: `
        <div class="card" style="max-width: 400px; margin: 50px auto;">
            <div class="card-header">
                <h2>🔐 登录</h2>
            </div>
            
            <div class="form-group">
                <label>用户名</label>
                <input type="text" id="loginUsername" placeholder="输入用户名">
            </div>
            
            <div class="form-group">
                <label>密码</label>
                <input type="password" id="loginPassword" placeholder="输入密码">
            </div>
            
            <button class="btn btn-primary" style="width: 100%;" onclick="login()">登录</button>
            
            <p style="text-align: center; margin-top: 20px; font-size: 13px; color: var(--text-tertiary);">
                还没有账号？<a href="#register" style="color: var(--accent);">注册</a>
            </p>
        </div>
    `,

    register: `
        <div class="card" style="max-width: 400px; margin: 50px auto;">
            <div class="card-header">
                <h2>📝 注册</h2>
            </div>
            
            <div class="form-group">
                <label>用户名</label>
                <input type="text" id="registerUsername" placeholder="输入用户名">
            </div>
            
            <div class="form-group">
                <label>邮箱</label>
                <input type="email" id="registerEmail" placeholder="输入邮箱">
            </div>
            
            <div class="form-group">
                <label>密码</label>
                <input type="password" id="registerPassword" placeholder="输入密码（至少6位）">
            </div>
            
            <button class="btn btn-primary" style="width: 100%;" onclick="register()">注册</button>
            
            <p style="text-align: center; margin-top: 20px; font-size: 13px; color: var(--text-tertiary);">
                已有账号？<a href="#login" style="color: var(--accent);">登录</a>
            </p>
        </div>
    `,

    profile: `
        <div class="card">
            <div class="card-header">
                <h2>👤 我的画像</h2>
                <button class="btn btn-primary" onclick="saveProfile()">保存</button>
            </div>
            
            <div class="form-group">
                <label>学校</label>
                <input type="text" id="school" placeholder="输入你的学校">
            </div>
            
            <div class="form-group">
                <label>专业类别</label>
                <select id="majorCategory" onchange="updateMajorSelect()">
                    <option value="">选择专业类别</option>
                    <option value="理工科">理工科</option>
                    <option value="文史类">文史类</option>
                    <option value="经管类">经管类</option>
                    <option value="法学类">法学类</option>
                    <option value="教育类">教育类</option>
                    <option value="医学类">医学类</option>
                    <option value="艺术类">艺术类</option>
                    <option value="农学类">农学类</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>具体专业</label>
                <select id="major">
                    <option value="">先选择专业类别</option>
                </select>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>目标城市</label>
                    <input type="text" id="targetCity" placeholder="如：北京、上海、深圳">
                </div>
                
                <div class="form-group">
                    <label>行业偏好</label>
                    <select id="industry">
                        <option value="">选择行业</option>
                        <option value="互联网">互联网</option>
                        <option value="金融">金融</option>
                        <option value="教育">教育</option>
                        <option value="医疗">医疗</option>
                        <option value="制造">制造</option>
                        <option value="其他">其他</option>
                    </select>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>目标公司</label>
                    <select id="targetCompany" onchange="updateTargetBadge()">
                        <option value="">选择目标公司</option>
                        <option value="华为">华为</option>
                        <option value="腾讯">腾讯</option>
                        <option value="阿里">阿里</option>
                        <option value="字节跳动">字节跳动</option>
                        <option value="百度">百度</option>
                        <option value="美团">美团</option>
                        <option value="京东">京东</option>
                        <option value="其他">其他</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>目标岗位</label>
                    <input type="text" id="targetPosition" placeholder="如：前端开发、会计、教师">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>期望薪资</label>
                    <input type="text" id="expectedSalary" placeholder="如：15k-20k">
                </div>
                
                <div class="form-group">
                    <label>工作经验</label>
                    <select id="experienceYears">
                        <option value="0">应届生</option>
                        <option value="1">1年</option>
                        <option value="2">2年</option>
                        <option value="3">3年</option>
                        <option value="5">5年以上</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label>技能标签</label>
                <input type="text" id="skills" placeholder="如：Python, JavaScript, 会计从业资格证">
            </div>
            
            <div class="form-group">
                <label>自我评价</label>
                <textarea id="selfEvaluation" rows="3" placeholder="简单描述你的优势和特点"></textarea>
            </div>
            
            <div class="form-group">
                <label>优势</label>
                <textarea id="strengths" rows="3" placeholder="你的核心竞争力是什么"></textarea>
            </div>
        </div>
    `,

    chat: `
        <div class="card">
            <div class="card-header">
                <h2>💬 面试对话</h2>
            </div>
            <p style="color: var(--text-tertiary); font-size: 13px;">选择专业类别后，可以练习专业相关的面试问题</p>
        </div>
        
        <div class="card" style="padding: 20px;">
            <div class="form-group" style="margin-bottom: 16px;">
                <label style="font-size: 12px;">当前专业类别</label>
                <select id="chatMajorCategory" onchange="updateChatMajor()" style="padding: 10px 14px; font-size: 13px;">
                    <option value="">通用面试问题</option>
                    <option value="理工科">理工科</option>
                    <option value="文史类">文史类</option>
                    <option value="经管类">经管类</option>
                    <option value="法学类">法学类</option>
                    <option value="教育类">教育类</option>
                    <option value="医学类">医学类</option>
                    <option value="艺术类">艺术类</option>
                    <option value="农学类">农学类</option>
                </select>
            </div>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message bot">
                <div class="avatar">🤖</div>
                <div class="text">
                    <p><strong>你好！我是面试准备助手 🎯</strong></p>
                    <p>我可以帮助你准备面试，包括：</p>
                    <ul>
                        <li>回答常见面试问题</li>
                        <li>提供专业相关的面试问题</li>
                        <li>根据目标公司定制回答</li>
                    </ul>
                    <p>请先选择你的专业类别，然后开始提问吧！</p>
                </div>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="questionInput" placeholder="输入你的面试问题..." autofocus>
            <button onclick="ask()">发送</button>
        </div>
        
        <div class="quick-questions">
            <button onclick="quickAsk('自我介绍')">💬 自我介绍</button>
            <button onclick="quickAsk('你的优点是什么')">💪 你的优点</button>
            <button onclick="quickAsk('你的缺点是什么')">⚠️ 你的缺点</button>
            <button onclick="quickAsk('为什么选择我们公司')">🏢 为什么选择我们</button>
            <button onclick="quickAsk('你的职业规划是什么')">📈 职业规划</button>
        </div>
    `,

    companies: `
        <div class="card">
            <div class="card-header">
                <h2>🏢 公司推荐</h2>
            </div>
            <p style="color: var(--text-tertiary); font-size: 13px;">根据你的目标城市和行业，为你推荐优质公司</p>
        </div>
        
        <div class="card" style="padding: 20px;">
            <div class="form-row">
                <div class="form-group">
                    <label>目标城市</label>
                    <input type="text" id="recommendCity" placeholder="如：北京、上海、深圳" onchange="loadRecommendations()">
                </div>
                
                <div class="form-group">
                    <label>行业</label>
                    <select id="recommendIndustry" onchange="loadRecommendations()">
                        <option value="">所有行业</option>
                        <option value="互联网">互联网</option>
                        <option value="金融">金融</option>
                        <option value="教育">教育</option>
                        <option value="医疗">医疗</option>
                        <option value="制造">制造</option>
                        <option value="智能硬件">智能硬件</option>
                        <option value="新能源">新能源</option>
                    </select>
                </div>
            </div>
        </div>
        
        <div class="companies-list" id="companiesList">
            <p style="text-align: center; color: var(--text-tertiary); padding: 40px;">选择城市和行业查看推荐公司</p>
        </div>
    `,

    history: `
        <div class="card">
            <div class="card-header">
                <h2>📋 历史记录</h2>
            </div>
            <div class="history-list" id="historyList">
                <p style="text-align: center; color: var(--text-tertiary); padding: 40px;">暂无历史记录</p>
            </div>
        </div>
    `
};

// 初始化应用
function init() {
    // 检查登录状态
    if (token && userId) {
        document.getElementById('navLogin').style.display = 'none';
        document.getElementById('navLogout').style.display = 'flex';
    } else {
        document.getElementById('navLogin').style.display = 'flex';
        document.getElementById('navLogout').style.display = 'none';
    }
    
    // 监听路由变化
    window.addEventListener('hashchange', handleRoute);
    
    // 初始加载
    handleRoute();
    
    // 如果已登录，加载用户画像
    if (token && userId) {
        loadProfile();
    }
}

// 处理路由
function handleRoute() {
    const hash = window.location.hash || '#home';
    const page = hash.substring(1);
    
    // 检查是否需要登录
    if (['profile', 'chat', 'companies', 'history'].includes(page) && !token) {
        window.location.hash = '#login';
        return;
    }
    
    if (pages[page]) {
        currentPage = page;
        document.getElementById('pageContent').innerHTML = pages[page];
        document.getElementById('pageTitle').textContent = document.querySelector(`[data-page="${page}"] .label`).textContent;
        
        // 更新导航状态
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.dataset.page === page) {
                link.classList.add('active');
            }
        });
        
        // 如果是画像页面，加载画像
        if (page === 'profile' && token) {
            loadProfile();
        }
        
        // 如果是公司推荐页面，加载推荐
        if (page === 'companies' && token) {
            loadRecommendations();
        }
        
        // 如果是历史记录页面，加载历史
        if (page === 'history' && token) {
            loadHistory();
        }
    }
}

// 导航到指定页面
function navigateTo(page) {
    window.location.hash = page;
}

// 注册
async function register() {
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    if (!username || !email || !password) {
        alert('请填写所有字段');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
            alert('注册成功！请登录');
            window.location.hash = '#login';
        } else {
            alert(data.detail || '注册失败');
        }
    } catch (error) {
        alert('注册失败，请重试');
    }
}

// 登录
async function login() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        alert('请填写用户名和密码');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
            // 保存 token 和 user_id
            token = data.token;
            userId = data.user_id;
            localStorage.setItem('token', token);
            localStorage.setItem('user_id', userId);
            
            // 更新导航
            document.getElementById('navLogin').style.display = 'none';
            document.getElementById('navLogout').style.display = 'flex';
            
            // 跳转到首页
            window.location.hash = '#home';
        } else {
            alert(data.detail || '登录失败');
        }
    } catch (error) {
        alert('登录失败，请重试');
    }
}

// 登出
function logout() {
    token = null;
    userId = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    
    document.getElementById('navLogin').style.display = 'flex';
    document.getElementById('navLogout').style.display = 'none';
    
    window.location.hash = '#home';
}

// 更新专业选择列表
function updateMajorSelect() {
    const category = document.getElementById('majorCategory').value;
    const majorSelect = document.getElementById('major');
    
    const majors = {
        "理工科": ["计算机科学", "电子信息", "机械工程", "土木工程", "化学工程", "材料科学", "数学", "物理学", "生物科学", "环境工程", "软件工程", "通信工程", "自动化"],
        "文史类": ["汉语言文学", "历史学", "哲学", "新闻传播学", "英语", "日语", "翻译", "广告学"],
        "经管类": ["会计学", "金融学", "工商管理", "市场营销", "人力资源管理", "财务管理", "国际经济与贸易", "经济学"],
        "法学类": ["法学", "社会学", "政治学与行政学", "思想政治教育"],
        "教育类": ["教育学", "学前教育", "小学教育", "体育教育", "教育技术学"],
        "医学类": ["临床医学", "护理学", "药学", "口腔医学", "预防医学", "中医学"],
        "艺术类": ["音乐学", "美术学", "艺术设计", "舞蹈学", "戏剧影视文学", "视觉传达设计"],
        "农学类": ["农学", "林学", "动物医学", "园艺", "植物保护"],
    };
    
    majorSelect.innerHTML = '<option value="">选择具体专业</option>';
    
    if (category && majors[category]) {
        majors[category].forEach(major => {
            const option = document.createElement('option');
            option.value = major;
            option.textContent = major;
            majorSelect.appendChild(option);
        });
    }
}

// 加载用户画像
async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/profile`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        if (data.data) {
            currentProfile = data.data;
            document.getElementById('school').value = currentProfile.school || '';
            document.getElementById('majorCategory').value = currentProfile.major_category || '';
            document.getElementById('targetCity').value = currentProfile.target_city || '';
            document.getElementById('industry').value = currentProfile.industry || '';
            document.getElementById('targetCompany').value = currentProfile.target_company || '';
            document.getElementById('targetPosition').value = currentProfile.target_position || '';
            document.getElementById('expectedSalary').value = currentProfile.expected_salary || '';
            document.getElementById('experienceYears').value = currentProfile.experience_years || 0;
            document.getElementById('skills').value = currentProfile.skills || '';
            document.getElementById('selfEvaluation').value = currentProfile.self_evaluation || '';
            document.getElementById('strengths').value = currentProfile.strengths || '';
            
            if (currentProfile.major_category) {
                updateMajorSelect();
                if (currentProfile.major) {
                    document.getElementById('major').value = currentProfile.major;
                }
            }
            
            updateTargetBadge();
        }
    } catch (error) {
        console.log('加载画像失败');
    }
}

// 保存用户画像
async function saveProfile() {
    const profile = {
        school: document.getElementById('school').value,
        major: document.getElementById('major').value,
        major_category: document.getElementById('majorCategory').value,
        target_city: document.getElementById('targetCity').value,
        industry: document.getElementById('industry').value,
        target_company: document.getElementById('targetCompany').value,
        target_position: document.getElementById('targetPosition').value,
        expected_salary: document.getElementById('expectedSalary').value,
        experience_years: parseInt(document.getElementById('experienceYears').value) || 0,
        skills: document.getElementById('skills').value,
        self_evaluation: document.getElementById('selfEvaluation').value,
        strengths: document.getElementById('strengths').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/profile`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(profile)
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
            currentProfile = profile;
            updateTargetBadge();
            alert('保存成功！');
        }
    } catch (error) {
        alert('保存失败，请重试');
    }
}

// 更新目标公司徽章
function updateTargetBadge() {
    const company = document.getElementById('targetCompany').value;
    const badge = document.getElementById('targetBadge');
    
    if (company) {
        badge.innerHTML = `<span class="company-badge">🎯 ${company}</span>`;
    } else {
        badge.innerHTML = '';
    }
}

// 更新聊天专业
function updateChatMajor() {
    // 可以在这里添加专业相关的提示
}

// 提问
async function ask() {
    const input = document.getElementById('questionInput');
    const question = input.value.trim();
    
    if (!question) return;
    
    // 添加用户消息
    addMessage('user', question);
    input.value = '';
    
    // 显示加载
    const loadingId = showLoading();
    
    try {
        const targetCompany = document.getElementById('targetCompany').value;
        const majorCategory = document.getElementById('chatMajorCategory').value;
        
        const response = await fetch(`${API_BASE_URL}/api/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                question: question,
                target_company: targetCompany,
                major_category: majorCategory
            })
        });
        
        const data = await response.json();
        
        // 移除加载
        removeLoading(loadingId);
        
        // 添加机器人消息
        addMessage('bot', data.answer);
        
    } catch (error) {
        removeLoading(loadingId);
        addMessage('bot', '请求失败，请重试');
    }
}

// 快速提问
function quickAsk(question) {
    if (currentPage !== 'chat') {
        navigateTo('chat');
    }
    setTimeout(() => {
        document.getElementById('questionInput').value = question;
        ask();
    }, 100);
}

// 添加消息
function addMessage(sender, text) {
    const container = document.getElementById('chatContainer');
    if (!container) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = sender === 'bot' ? '🤖' : '👤';
    
    let formattedText = text.replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="text">${formattedText}</div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

// 显示加载
function showLoading() {
    const container = document.getElementById('chatContainer');
    if (!container) return;
    
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot';
    loadingDiv.id = 'loading';
    
    loadingDiv.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="text">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    container.appendChild(loadingDiv);
    container.scrollTop = container.scrollHeight;
    
    return 'loading';
}

// 移除加载
function removeLoading(id) {
    const loading = document.getElementById(id);
    if (loading) {
        loading.remove();
    }
}

// 加载公司推荐
async function loadRecommendations() {
    const city = document.getElementById('recommendCity').value;
    const industry = document.getElementById('recommendIndustry').value;
    
    try {
        const params = new URLSearchParams();
        if (city) params.append('city', city);
        if (industry) params.append('industry', industry);
        
        const response = await fetch(`${API_BASE_URL}/api/companies/recommend?${params}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        const list = document.getElementById('companiesList');
        if (data.data && data.data.length > 0) {
            list.innerHTML = data.data.map(company => `
                <div class="company-item">
                    <div class="company-header">
                        <h3>${company.name}</h3>
                        <span class="tag">${company.city}</span>
                        <span class="tag">${company.industry}</span>
                    </div>
                    <p style="color: var(--text-secondary); font-size: 13px; margin-top: 8px;">${company.description}</p>
                    <a href="${company.website}" target="_blank" style="color: var(--accent); font-size: 13px; margin-top: 8px; display: inline-block;">官网 →</a>
                </div>
            `).join('');
        } else {
            list.innerHTML = '<p style="text-align: center; color: var(--text-tertiary); padding: 40px;">没有找到匹配的公司</p>';
        }
    } catch (error) {
        console.log('加载推荐失败');
    }
}

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/history`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            const historyList = document.getElementById('historyList');
            historyList.innerHTML = data.data.map(item => `
                <div class="history-item">
                    <div class="question">${item.question}</div>
                    <div class="answer">${item.answer}</div>
                    <div class="meta">
                        <span>${new Date(item.created_at).toLocaleString()}</span>
                        <span class="score">${item.score || 90}分</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.log('加载历史失败');
    }
}

// 回车发送
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && currentPage === 'chat') {
        ask();
    }
});

// 页面加载时初始化
window.onload = init;