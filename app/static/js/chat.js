//发送消息
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

//打印机效果
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

let uploadHistory = []; // 存储上传历史的数组

//上传文件
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

        const uploadTime = new Date().toLocaleString();
        // 将文件名和时间添加到上传历史数组
        u = document.getElementById('fileInput')
        uploadHistory.push({ fileName: u.files[0].name, time: uploadTime, content: data.text });
        // 更新页面上的上传历史显示
        displayUploadHistory();
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
    appendMessage('user-message', '用户: '  + "提取关键字");
    document.getElementById('userInput').value = '';

    // 发送请求到后端
    fetch('/openapi/getKeyword', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput+ "提取关键字" })
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


// 显示上传历史列表
function displayUploadHistory() {
    const historyList = document.getElementById("uploadHistory");
    historyList.innerHTML = ""; // 清空之前的历史记录

    // 遍历上传历史数组，生成列表项
    uploadHistory.forEach((record, index) => {
        const listItem = document.createElement("li");
        listItem.className = "list-group-item d-flex justify-content-between align-items-center";

        listItem.innerHTML = `
            <span>${record.fileName}</span>
            <div>
                <span class="text-muted me-3" style="font-size: 0.9rem;">${record.time}</span>
                <button class="btn btn-outline-primary btn-sm" onclick="viewFile(${index})">查看文件</button>
            </div>
        `;
        historyList.appendChild(listItem);
    });
}

// 查看文件内容并显示在result区域
function viewFile(index) {
    const resultDiv = document.getElementById("result");
    const fileContent = uploadHistory[index].content;
    resultDiv.innerHTML = `<strong>文件内容:</strong><br>${fileContent}`;
}
