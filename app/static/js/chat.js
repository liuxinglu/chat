function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput) return;

    // 在页面显示用户的消息
    appendMessage('user-message', '用户: '  + userInput);
    document.getElementById('userInput').value = '';

    // 发送请求到后端
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.reply) {
            appendMessage('bot-message', '碎嘴子: ' + data.reply);
        } else {
            appendMessage('bot-message', '碎嘴子: 无法获取回复');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('bot-message', '碎嘴子: 请求失败');
    });
}

function appendMessage(className, message) {
    const chatBox = document.getElementById('chatBox');
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + className;
    messageElement.textContent = message;
    messageElement.style.whiteSpace = 'pre-wrap';
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}