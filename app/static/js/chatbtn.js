let messageInd = 100000
document.addEventListener('DOMContentLoaded', () => {
    const chatButton = document.getElementById('minichat-button');
    const chatBox = document.getElementById('minichat-box');
    const closeButton = document.querySelector('.close-button');
    const minButton = document.getElementById('minimize-button');
    const maxButton = document.getElementById('maximize-button');
    let content = document.getElementById('minichat-content');

    let isMaximized;


    closeButton.addEventListener('click', () => {
        chatBox.style.display = 'none';
    });
    minButton.addEventListener('click', () => {
        if (!isMaximized) { // 如果当前不是最大化状态，则最小化
            chatBox.style.height = '60px'; // 你可以根据需要调整这个高度
//            chatBox.style.overflow = 'hidden';
//            chatBox.style.display = 'none';
            maxButton.textContent = '+'; // 更改按钮文本为表示可以恢复（最大化）的图标
        }
        isMaximized = false;
    });

    maxButton.addEventListener('click', () => {
        if (isMaximized) { // 如果当前是最大化状态，则恢复到原始大小
            chatBox.style.height = '330px'; // 恢复原始高度
            chatBox.style.overflow = 'auto';
            minButton.style.display = 'inline-block';
            maxButton.textContent = '+'; // 恢复按钮文本为表示可以最大化的图标
            content.style.height = '65%';
        } else { // 如果当前不是最大化状态，则最大化
            const viewportHeight = window.innerHeight;
            const buttonHeight = document.getElementById('minichat-button').offsetHeight;
            chatBox.style.height = `${viewportHeight - buttonHeight - 20}px`; // 减去按钮高度和一些间距
            chatBox.style.overflow = 'auto';
            minButton.style.display = 'inline-block';
            content.style.height = '86%';
        }
        isMaximized = !isMaximized;
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
        const chatBox1 = document.getElementById('minichat-content');
        const messageElement = document.createElement('div');
        messageElement.className = 'message ' + className;
        messageElement.style.whiteSpace = 'pre-wrap';
        messageElement.id = 'message' + messageInd;
        chatBox1.appendChild(messageElement);
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
