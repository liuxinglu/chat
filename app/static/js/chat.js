function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput) return;

    // 在页面显示用户的消息
    appendMessage('user-message', '用户: '  + userInput);
    document.getElementById('userInput').value = '';

    // 发送请求到后端
    fetch('/openapi/chat', {
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
    messageElement.style.whiteSpace = 'pre-wrap';
    messageElement.id = 'message ' + Date.now()
    chatBox.scrollTop = chatBox.scrollHeight;
    chatBox.appendChild(messageElement);
     typeText('message '+ Date.now(), message, 10)
}

function typeText(elementId, text, speed) {
    const element = document.getElementById(elementId);
    let index = 0;
    const type = () => {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      }
    };
    type();
}

 function uploadFile() {
    var form = document.getElementById('uploadForm');
    var formData = new FormData(form);

    fetch('/fileops/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
            document.getElementById('result').innerText = '';
        } else {
            document.getElementById('result').innerText = data.text;
            document.getElementById('keywords').innerText = "关键字："+data.keywords;
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('An error occurred while uploading the file.');
        document.getElementById('result').innerText = '';
    });
}

