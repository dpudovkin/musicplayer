$(document).ready(function(){

        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const roomSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/app/'
            + roomName
            + '/'
        );

        roomSocket.onmessage = function(e) {
            var playBtn = document.querySelector('button');
            const data = JSON.parse(e.data);
            msg = data.message



            if (msg.toLowerCase()==playBtn.title.toLowerCase()){
               playBtn.click()
            }
        };

        roomSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        const playBtn = document.querySelector('button');
        playBtn.addEventListener("click", () => {
            console.log(playBtn.title);
            roomSocket.send(JSON.stringify({
                'message': playBtn.title
            }));
        });

})