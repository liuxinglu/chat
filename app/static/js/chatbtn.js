let messageInd = 0
document.addEventListener('DOMContentLoaded', () => {
    const chatButton = document.getElementById('minichat-button');
    const chatBox = document.getElementById('minichat-box');
    const closeButton = document.querySelector('.close-button');

    chatButton.addEventListener('click', () => {
        chatBox.style.display = 'block';
    });

    closeButton.addEventListener('click', () => {
        chatBox.style.display = 'none';
    });

    let isDragging = false;
    let offsetX, offsetY;

    const draggableElements = chatBox.querySelectorAll('.minichat-header, .minichat-box');
    draggableElements.forEach(element => {
        element.addEventListener('mousedown', (e) => {
            isDragging = true;
            offsetX = e.clientX - chatBox.getBoundingClientRect().left;
            offsetY = e.clientY - chatBox.getBoundingClientRect().top;
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
    });

    function onMouseMove(e) {
        if (isDragging) {
            chatBox.style.left = `${e.clientX - offsetX}px`;
            chatBox.style.top = `${e.clientY - offsetY}px`;
            chatBox.style.height = chatBox.style.height
        }
    }

    function onMouseUp() {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }
});

function sendMessage() {
        const userInput = document.getElementById('umessage').value;
        if (!userInput) return;

        // 在页面显示用户的消息
        appendMessage('miniuser-message', '用户: '  + userInput);
        document.getElementById('umessage').value = '';

        // 发送请求到后端
        fetch('/xinghuo/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
        .then(data => {
            if (data.reply) {
                appendMessage('minibot-message', '回复: ' + data.reply);
            } else {
                appendMessage('minibot-message', '回复: 无法获取回复');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('minibot-message', `回复: 请求失败 (${error.message})`);
        });
    }

    function appendMessage(className, message) {
        const chatBox = document.getElementById('minichat-content');
        const messageElement = document.createElement('div');
        messageElement.className = 'message ' + className;
        messageElement.style.whiteSpace = 'pre-wrap';
        messageElement.id = 'message' + messageInd;
        chatBox.appendChild(messageElement);
        typeText('message'+ messageInd, message, 10)
        messageInd++;

    }

    //打印机效果
    function typeText(elementId, text, speed) {
        const element = document.getElementById(elementId);
        let index = 0;
        const type = () => {
          if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
            const chatBox = document.getElementById('minichat-content');
            chatBox.scrollTop = chatBox.scrollHeight;
          }
        };
        type();
    }
