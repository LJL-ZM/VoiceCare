const API_BASE_URL = 'http://localhost:8000';
let currentProfile = null;
let currentPage = 'home';

// 页面模板
const pages = {
    home: `
        <div class="card">
            <h2>🎯 欢迎使用 AI 面试准备助手</h2>
            <p style="color: var(--text-light); margin-top: 10px;">帮助你准备面试，提升求职成功率</p>
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
            
            <div class="home-card" onclick="navigateTo('history')">
                <div class="icon">📋</div>
                <h3>历史记录</h3>
                <p>查看之前的面试练习记录，回顾和改进</p>
            </div>
        </div>
        
        <div class="card" style="margin-top: 25px;">
            <h2 style="margin-bottom: 15px;">💡 使用指南</h2>
            <ul style="line-height: 2; color: var(--text-light);">
                <li>1. 先在「我的画像」中配置你的信息</li>
                <li>2. 在「面试对话」中练习面试问题</li>
                <li>3. 查看「历史记录」回顾练习内容</li>
                <li>4. 配置目标公司后，AI 会给出定制化建议</li>
            </ul>
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
                <label>专业</label>
                <input type="text" id="major" placeholder="输入你的专业">
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
                    <input type="text" id="targetPosition" placeholder="如：前端开发">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>期望薪资</label>
                    <input type="text" id="expectedSalary" placeholder="如：15k-20k">
                </div>
                
                <div class="form-group">
                    <label>工作地点</label>
                    <input type="text" id="workLocation" placeholder="如：北京">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>行业偏好</label>
                    <select id="industry">
                        <option value="">选择行业</option>
                        <option value="互联网">互联网</option>
                        <option value="金融">金融</option>
                        <option value="制造业">制造业</option>
                        <option value="教育">教育</option>
                        <option value="医疗">医疗</option>
                        <option value="其他">其他</option>
                    </select>
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
                <input type="text" id="skills" placeholder="如：Python, JavaScript, React">
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
        <div class="chat-container" id="chatContainer">
            <div class="message bot">
                <div class="avatar">🤖</div>
                <div class="text">
                    <p><strong>你好！我是面试准备助手 🎯</strong></p>
                    <p>我可以帮助你准备面试，包括：</p>
                    <ul>
                        <li>回答常见面试问题</li>
                        <li>提供针对性的面试建议</li>
                        <li>根据目标公司定制回答</li>
                    </ul>
                    <p>请在左侧配置你的画像，然后开始提问吧！</p>
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

    history: `
        <div class="card">
            <div class="card-header">
                <h2>📋 历史记录</h2>
            </div>
            <div class="history-list" id="historyList">
                <p style="text-align: center; color: var(--text-light); padding: 40px;">暂无历史记录</p>
            </div>
        </div>
    `
};

// 初始化应用
function init() {
    // 监听路由变化
    window.addEventListener('hashchange', handleRoute);
    
    // 初始加载
    handleRoute();
    
    // 加载用户画像
    loadProfile();
    
    // 加载历史记录
    loadHistory();
}

// 处理路由
function handleRoute() {
    const hash = window.location.hash || '#home';
    const page = hash.substring(1);
    
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
        
        // 如果是聊天页面，加载历史
        if (page === 'chat') {
            loadHistory();
        }
    }
}

// 导航到指定页面
function navigateTo(page) {
    window.location.hash = page;
}

// 加载用户画像
async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/profile`);
        const data = await response.json();
        
        if (data.data) {
            currentProfile = data.data;
            document.getElementById('school').value = currentProfile.school || '';
            document.getElementById('major').value = currentProfile.major || '';
            document.getElementById('targetCompany').value = currentProfile.target_company || '';
            document.getElementById('targetPosition').value = currentProfile.target_position || '';
            document.getElementById('expectedSalary').value = currentProfile.expected_salary || '';
            document.getElementById('workLocation').value = currentProfile.work_location || '';
            document.getElementById('industry').value = currentProfile.industry || '';
            document.getElementById('experienceYears').value = currentProfile.experience_years || 0;
            document.getElementById('skills').value = currentProfile.skills || '';
            document.getElementById('selfEvaluation').value = currentProfile.self_evaluation || '';
            document.getElementById('strengths').value = currentProfile.strengths || '';
            
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
        target_company: document.getElementById('targetCompany').value,
        target_position: document.getElementById('targetPosition').value,
        expected_salary: document.getElementById('expectedSalary').value,
        work_location: document.getElementById('workLocation').value,
        industry: document.getElementById('industry').value,
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
        badge.innerHTML = `<span style="background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: white; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600;">🎯 ${company}</span>`;
    } else {
        badge.innerHTML = '';
    }
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
        
        const response = await fetch(`${API_BASE_URL}/api/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                question: question,
                target_company: targetCompany
            })
        });
        
        const data = await response.json();
        
        // 移除加载
        removeLoading(loadingId);
        
        // 添加机器人消息
        addMessage('bot', data.answer);
        
        // 保存到历史
        loadHistory();
        
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
    
    // 处理换行
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
        <div class="text">思考中...</div>
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

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/history`);
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            const historyList = document.getElementById('historyList');
            if (historyList) {
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