// Intellius Chat Service JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages');
    const messageForm = document.getElementById('messageForm');
    const messageInput = document.getElementById('messageInput');

    // 메시지 전송
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (message) {
            addMessage('user', message);
            messageInput.value = '';
            
            // 간단한 봇 응답 시뮬레이션
            setTimeout(() => {
                addMessage('bot', `안녕하세요! "${message}"라고 하셨군요.`);
            }, 1000);
        }
    });

    // 메시지 추가 함수
    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${sender === 'user' ? '사용자' : '봇'}:</strong> ${text}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // 초기 메시지
    addMessage('bot', '안녕하세요! Intellius Chat Service에 오신 것을 환영합니다.');
});
