const messagesArea = document.getElementById('messagesArea');
const userInput = document.getElementById('userInput');
const historyList = document.getElementById('historyList');

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Kullanıcı mesajını ekrana bas
    appendMessage(text, 'user');
    userInput.value = '';

    // Sol taraftaki geçmişe ekle
    addToHistory(text);

    // Düşünme efektini başlat
    const typingId = appendTypingIndicator();

    try {
        // Flask API'sine istek atıyoruz
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        const data = await response.json();
        
        // Efekti kaldır
        document.getElementById(typingId).remove();

        if (data.response) {
            appendMessage(data.response, 'ai');
        } else {
            appendMessage("Bir hata oluştu: " + data.error, 'ai');
        }
    } catch (error) {
        document.getElementById(typingId).remove();
        appendMessage("Sunucuya bağlanılamadı.", 'ai');
    }
}

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    
    const bubble = document.createElement('div');
    bubble.classList.add('msg-bubble');
    bubble.innerText = text;
    
    msgDiv.appendChild(bubble);
    messagesArea.appendChild(msgDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

function appendTypingIndicator() {
    const id = 'typing_' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'ai');
    msgDiv.id = id;

    const bubble = document.createElement('div');
    bubble.classList.add('msg-bubble');

    const indicator = document.createElement('div');
    indicator.classList.add('typing-indicator');
    indicator.innerHTML = '<span></span><span></span><span></span>';

    bubble.appendChild(indicator);
    msgDiv.appendChild(bubble);
    messagesArea.appendChild(msgDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
    return id;
}

function addToHistory(text) {
    const shortTitle = text.length > 25 ? text.substring(0, 25) + '...' : text;
    
    const item = document.createElement('div');
    item.classList.add('history-item');
    item.innerHTML = `<i class="fa-regular fa-message"></i> ${shortTitle}`;
    
    historyList.insertBefore(item, historyList.firstChild);
}

function clearChat() {
    messagesArea.innerHTML = `
        <div class="message ai">
            <div class="msg-bubble">
                Yeni bir seyahat planına hoş geldin! Keşfetmek istediğin yeni yerleri bana sorabilirsin. 🧭
            </div>
        </div>
    `;
}