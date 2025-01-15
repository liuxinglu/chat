let ticketIndex = 0
//发送消息
function sendUserMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput) return;

    // 在页面显示用户的消息
    appendMessage('user-message', '用户: '  + userInput);
    document.getElementById('userInput').value = '';

    // 发送请求到后端
    fetch('/servicedesk/ticketDesc', {
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
            appendMessage('bot-message', data.reply);
        } else {
            appendMessage('bot-message', '无法获取回复');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('bot-message', `回复: 请求失败 (${error.message})`);
    });
}

function appendMessage(className, message) {
    const chatBox = document.getElementById('chatBox');
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + className;
    messageElement.style.whiteSpace = 'pre-wrap';
    messageElement.id = 'message' + ticketIndex;
    chatBox.appendChild(messageElement);
    typeText('message'+ ticketIndex, message, 10)
    ticketIndex++;

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
        const chatBox = document.getElementById('chatBox');
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    };
    type();
}

uploadHistoryList = []; // 存储上传历史的数组

//上传文件
 function uploadFile() {
    var form = document.getElementById('uploadForm');
    var formData = new FormData(form);

    fetch('/domain/upload', {
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
        }

        const uploadTime = new Date().toLocaleString();
        // 将文件名和时间添加到上传历史数组
        u = document.getElementById('fileInput')
        uploadHistoryList.push({ fileName: u.files[0].name, time: uploadTime, content: data.text });
        // 更新页面上的上传历史显示
        displayUploadHistory();
        // 高亮显示刚上传的文件
        highlightNewUpload(uploadHistoryList.length - 1);
        // 滚动到最新上传的文件
        scrollToLatestUpload();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('An error occurred while uploading the file.');
        document.getElementById('result').innerText = '';
    });
}

//提取关键字
function getKeywords() {
    const userInput = document.getElementById('result').textContent;
    // 在页面显示用户的消息
//    appendMessage('user-message', '用户: '  + "提取关键字");
//    document.getElementById('userInput').value = '';

    // 发送请求到后端
    fetch('/pageops/getModel', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        fetch('/wenxin/getKeyword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput+ "提取关键字" })
        })
        .then(response => response.json())
        .then(data => {
            if (data.reply) {
                appendMessage('bot-message', data.reply);
            } else {
                appendMessage('bot-message', '无法获取回复');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('bot-message', '请求失败');
        });
    })
    .catch(error => {
            console.error('Error:', error);
            appendMessage('bot-message', '获取模型失败');
    });
}

// 滚动到列表底部
function scrollToLatestUpload() {
    const historyList = document.getElementById("uploadHistory");
    historyList.scrollTop = historyList.scrollHeight; // 将滚动位置设置为列表的最大高度
}

