const API_BASE_URL = 'http://localhost:8000';

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
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
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

function quickAsk(question) {
    document.getElementById('questionInput').value = question;
    ask();
}

function addMessage(sender, text) {
    const container = document.getElementById('chatContainer');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = sender === 'bot' ? '🤖' : '👤';
    
    messageDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="text">${text}</div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function showLoading() {
    const container = document.getElementById('chatContainer');
    
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

function removeLoading(id) {
    const loading = document.getElementById(id);
    if (loading) {
        loading.remove();
    }
}

// 回车发送
document.getElementById('questionInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        ask();
    }
});