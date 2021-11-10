$(document).ready(function(){

        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const playCommand = 'play', pauseCommand = 'pause', nextVoteCommand = 'vote';
        const audioUpdateCommand = 'audio_update';
        const userConnectCommand = 'user_connect', userDisconnectCommand = 'user_disconnect';
        const voteUpdateCommand = 'vote_update';
        const actionHeader = 'action';

        const connectedCount = document.querySelector('#connected')
        const votedCount = document.querySelector('#voted')

        const roomSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/app/'
            + roomName
            + '/'
        );

        const playBtn = document.querySelector('#playButton');
        const pauseBtn = document.querySelector('#pauseButton');
        const nextBtn = document.querySelector('#nextButton');
        const audio =  document.querySelector('audio')
        const songText = document.querySelector('#songText')

        roomSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            msg = data.action;

            if (msg == null){
                console.log('Null message');
                return;
            }

            if (msg.toLowerCase()==playCommand){
               audio.play();
            }

            if (msg.toLowerCase()==pauseCommand){
                audio.pause();
            }

            if (msg.toLowerCase()==nextVoteCommand){
                //nextBtn.click();
                // next track
            }

            if (msg.toLowerCase()==audioUpdateCommand){
                // audio update for the next track
                audio.src = data.src;
                songText.innerHTML =  data.text;
            }

            if (msg.toLowerCase()==userConnectCommand || msg.toLowerCase()==userDisconnectCommand){
                //data.user_list
                connectedCount.innerHTML = data.users.length
                console.log(data.users)
                console.log(data.username)

            }

            if (msg.toLowerCase()==voteUpdateCommand){
                votedCount.innerHTML = data.vote_count
                console.log(data.vote_count)
            }
        };

        roomSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };


        playBtn.addEventListener("click", () => {
            roomSocket.send(JSON.stringify({
                'action': playCommand,
                'source': 'front'
            }));
        });

        pauseBtn.addEventListener("click", () => {
            roomSocket.send(JSON.stringify({
                'action': pauseCommand
            }));
        });

        nextBtn.addEventListener("click", () => {
            roomSocket.send(JSON.stringify({
                'action': nextVoteCommand
            }));
        });





})