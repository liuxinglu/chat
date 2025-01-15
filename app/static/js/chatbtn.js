let messageInd = 0
document.addEventListener('DOMContentLoaded', () => {
    const chatButton = document.getElementById('minichat-button');
    const chatBox = document.getElementById('minichat-box');
    const closeButton = document.querySelector('.close-button');


    closeButton.addEventListener('click', () => {
        chatBox.style.display = 'none';
    });

    let isDragging = false;
    let offsetX, offsetY;
    let dX,dY;

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
    chatButton.addEventListener('mousedown', (e) => {
        isDragging = true;
        offsetX = e.clientX - chatButton.getBoundingClientRect().left;
        offsetY = e.clientY - chatButton.getBoundingClientRect().top;
        dX = e.clientX;
        dY = e.clientY;
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });

    function onMouseMove(e) {
        if (chatBox.style.display == 'block') {
            if (isDragging) {
                chatBox.style.left = `${e.clientX - offsetX}px`;
                chatBox.style.top = `${e.clientY - offsetY}px`;
                chatBox.style.height = chatBox.style.height;
            }
        }
        else {
            if (isDragging) {
                chatButton.style.left = `${e.clientX - offsetX}px`;
                chatButton.style.top = `${e.clientY - offsetY}px`;
                chatButton.style.height = chatButton.style.height;
            }
        }
    }

    function onMouseUp(e) {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }

    chatButton.addEventListener('click', (e) => {
        if (Math.abs(e.clientX - dX) < 1 && Math.abs(e.clientY - dY) < 1) {
            chatBox.style.display = 'block';
        }
    });
});

function minisendMessage() {
        const userInput = document.getElementById('umessage').value;
        if (!userInput) return;

        // 在页面显示用户的消息
        miniappendMessage('miniuser-message', '用户: '  + userInput);
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
                miniappendMessage('minibot-message', '回复: ' + data.reply);
            } else {
                miniappendMessage('minibot-message', '回复: 无法获取回复');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            miniappendMessage('minibot-message', `回复: 请求失败 (${error.message})`);
        });
    }

    function miniappendMessage(className, message) {
        const chatBox = document.getElementById('minichat-content');
        const messageElement = document.createElement('div');
        messageElement.className = 'message ' + className;
        messageElement.style.whiteSpace = 'pre-wrap';
        messageElement.id = 'message' + messageInd;
        chatBox.appendChild(messageElement);
        minitypeText('message'+ messageInd, message, 10)
        messageInd++;

    }

    //打印机效果
    function minitypeText(elementId, text, speed) {
        const element = document.getElementById(elementId);
        let index = 0;
        const minitype = () => {
          if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(minitype, speed);
            const chatBox = document.getElementById('minichat-content');
            chatBox.scrollTop = chatBox.scrollHeight;
          }
        };
        minitype();
    }
