let messageIndex = 0
//发送消息
function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput) return;

    // 在页面显示用户的消息
    appendMessage('user-message', '用户: '  + userInput);
    document.getElementById('userInput').value = '';

    // 发送请求到后端
    fetch('/pageops/getModel', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        fetch('/' + data.model + '/chat', {
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
                appendMessage('bot-message', '回复: ' + data.reply);
            } else {
                appendMessage('bot-message', '回复: 无法获取回复');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('bot-message', `回复: 请求失败 (${error.message})`);
        });
    })
    .catch(error => {
            console.error('Error:', error);
            appendMessage('bot-message', '获取模型失败');
    });
}

function appendMessage(className, message) {
    const chatBox = document.getElementById('chatBox');
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + className;
    messageElement.style.whiteSpace = 'pre-wrap';
    messageElement.id = 'message' + messageIndex;
    chatBox.appendChild(messageElement);
     typeText('message'+ messageIndex, message, 10)
     messageIndex++;

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
    appendMessage('user-message', '用户: '  + "提取关键字");
    document.getElementById('userInput').value = '';

    // 发送请求到后端
    fetch('/pageops/getModel', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        fetch('/' + data.model + '/getKeyword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput+ "提取关键字" })
        })
        .then(response => response.json())
        .then(data => {
            if (data.reply) {
                appendMessage('bot-message', '回复: ' + data.reply);
            } else {
                appendMessage('bot-message', '回复: 无法获取回复');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('bot-message', '回复: 请求失败');
        });
    })
    .catch(error => {
            console.error('Error:', error);
            appendMessage('bot-message', '获取模型失败');
    });
}


// 显示上传历史列表
function displayUploadHistory(files="none") {
    const historyList = document.getElementById("uploadHistory");
    historyList.innerHTML = ""; // 清空之前的历史记录
    if(files === "none") {
        // 遍历上传历史数组，生成列表项
        uploadHistoryList.forEach((record, index) => {
            const listItem = document.createElement("li");
            listItem.className = "list-group-item d-flex justify-content-between align-items-center";
            listItem.id = `uploadItem-${index}`; // 为每个列表项设置唯一 ID

            listItem.innerHTML = `
                <span id="fileName-${index}">${record.fileName}</span>
                <div>
                    <span class="text-muted me-3" style="font-size: 0.6rem;">${record.time}</span>
                    <button class="btn btn-outline-primary btn-sm" onclick="viewFile(${index})">查看</button>
                </div>
            `;
            historyList.appendChild(listItem);
        });
    }
    else {
        uploadHistoryList = [];
        files.forEach((file, index) => {
            const listItem = document.createElement("li");
            listItem.className = "list-group-item d-flex justify-content-between align-items-center";
            listItem.id = `uploadItem-${index}`; // 为每个列表项设置唯一 ID
            listItem.innerHTML = `
                <span id="fileName-${index}">${file.filename} </span>
                <div>
                    <span class="text-muted me-3" style="font-size: 0.6rem;">${new Date(file.upload_date).toLocaleString()}</span>
                    <button class="btn btn-outline-primary btn-sm" onclick="viewFileContent(${index})">查看</button>
                </div>
            `;

            historyList.appendChild(listItem);
            uploadHistoryList.push({ fileName: file.filename, time: new Date(file.upload_date).toLocaleString(), content: file.content });
        });
    }
}

// 查看文件内容并显示在result区域
function viewFileContent(index) {
//    const fileName = uploadHistoryList[index].fileName;
//    fetch(`/fileops/getFile?filename=${encodeURIComponent(fileName)}`)
//                .then(response => response.json())
//                .then(data => {
//                    // 将返回结果展示在页面上
//                    document.getElementById('result').innerText = data.text;
//                })
//                .catch(error => console.error('Error:', error));
    const resultDiv = document.getElementById("result");
    const fileContent = uploadHistoryList[index].content;
    resultDiv.innerHTML = `${fileContent}`;
}


// 高亮显示刚上传的文件
function highlightNewUpload(index) {
    const listItem = document.getElementById(`uploadItem-${index}`);
//    const listItem = document.getElementById(`fileName-${index}`);
    if (listItem) {
        listItem.classList.add("highlight-animation"); // 添加高亮动画类
    }
}

// 滚动到列表底部
function scrollToLatestUpload() {
    const historyList = document.getElementById("uploadHistory");
    historyList.scrollTop = historyList.scrollHeight; // 将滚动位置设置为列表的最大高度
}