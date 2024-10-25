// app/static/js/chat.js
document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send');
    const messageInput = document.getElementById('message');
    const messagesDiv = document.getElementById('messages');
    const usernameInput = document.getElementById('username');

    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        const username = usernameInput.value.trim() || 'Guest';

        if (message === '') return;

        appendMessage('user', message);
        messageInput.value = '';

        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message, username: username })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('bot', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('bot', '抱歉，我遇到了一个问题。');
        });
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(sender);
        messageElement.textContent = message;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});
