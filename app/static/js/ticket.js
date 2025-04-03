var ticketIndex = 0

function viewHistory() {
    // 发送请求到后端
    fetch('/servicedesk/tickethistory', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) { throw new Error(`HTTP error! Status: ${response.status}`);}
        return response.json();
      })
    .then(data => {

    })
    .catch(error => { console.error('Error:', error.message);});
}

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
        body: JSON.stringify({ message: userInput, index: ticketIndex })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
    .then(data => {
        if (data.reply) {
            appendBox(data.reply);
        } else {
            appendMessage('bot-message', '无法获取回复');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('bot-message', `回复: 请求失败 (${error.message})`);
    });
}

function appendBox(content) {
    appendMessage('bot-message', content);
    var $chatbox = $('#chatBox');
    var $btn = $('<button>', {'class': 'btn btn-primary', text: 'submit & create ticket'}).attr('id', 'ticketSubmit' + (ticketIndex-1));
    $btn.on('click', function() { submitTicket(ticketIndex-1);});
    $chatbox.append($btn);
    var $btn1 = $('<button>', {'class': 'btn btn-primary', text: '👍'}).attr('id', 'ticketgood' + (ticketIndex-1));
    $btn1.on('click', function() { judgeTicket(ticketIndex-1, 1);});
    $chatbox.append($btn1);
    var $btn2 = $('<button>', {'class': 'btn btn-primary', text: '👎'}).attr('id', 'ticketbad' + (ticketIndex-1));
    $btn2.on('click', function() { judgeTicket(ticketIndex-1, 0);});
    $chatbox.append($btn2);
    var $hr = $('<hr>');
    $chatbox.append($hr);
}

function submitTicket(ind) {
    // 发送请求到后端
    fetch('/servicedesk/submitTicket', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ index: ind })
    })
    .then(response => {
        if (!response.ok) { throw new Error(`HTTP error! Status: ${response.status}`);}
        return response.json();
      })
    .then(data => {

    })
    .catch(error => { console.error('Error:', error.message);});
}

function judgeTicket(ind, goodorbad) {
// 发送请求到后端
    fetch('/servicedesk/goodorbad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ index: ind, goodorbad:goodorbad })
    })
    .then(response => {
        if (!response.ok) { throw new Error(`HTTP error! Status: ${response.status}`);}
        return response.json();
      })
    .then(data => {

    })
    .catch(error => { console.error('Error:', error.message);});
}

function appendMessage(className, message) {
    const chatBox = document.getElementById('chatBox');
    let messageElement = null;
    if(className == 'user-message'){
        messageElement = document.createElement('div');
    }
    else if(className == 'bot-message') {
        messageElement = document.createElement('textarea');
        messageElement.style.width = '100%';
        messageElement.style.height = '100%';
    }

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


