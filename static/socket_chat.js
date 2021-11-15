$(document).ready(function(){
    let chat = document.querySelector("#chat")
    let input = document.querySelector("#messageInput")
    let btnSubmit = document.querySelector("#sendMsg")

    const roomName = JSON.parse(document.getElementById('room-name').textContent);



const webSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/'+ roomName+'/');
    webSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            chat.innerHTML += '<div><b> ' + data.username + ' </b></div>'
            chat.innerHTML += '<div class="msg">' + data.text + '</div>'
    };

    webSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
            alert("Chat socket closed unexpectedly. Try to reload page!");
    };

    btnSubmit.addEventListener("click", () => {
            message = input.value;
            webSocket.send(JSON.stringify({
                'text': message
            }));
            input.value = '';
    })
})