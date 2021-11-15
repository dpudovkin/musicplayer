$(document).ready(function(){

        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const playCommand = 'play', pauseCommand = 'pause', nextVoteCommand = 'vote';
        const audioUpdateCommand = 'audio_update';
        const userConnectCommand = 'user_connect', userDisconnectCommand = 'user_disconnect';
        const voteUpdateCommand = 'vote_update';
        const actionHeader = 'action'


        const connectedCount = document.querySelector('#connected')
        const votedCount = document.querySelector('#voted')

        const audioImage = document.querySelector('#audio-image')
        const audioTitle = document.querySelector('#song-title')
        const usersContainer =  document.querySelector("#user-list")

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
                audioImage.src = data.img;
                audio.src = data.src;
                songText.innerHTML =  data.text;
                audioTitle.innerHTML =  data.title+" - "+data.artist

            }

            if (msg.toLowerCase()==userConnectCommand || msg.toLowerCase()==userDisconnectCommand){
                var avatars = new Array('/media/cat1.png', '/media/cat2.png', '/media/cat3.png');

                connectedCount.innerHTML = data.users.length
                usersContainer.innerHTML=""
                for (let i = 0; i < data.users.length; i += 1) {
                    usersContainer.innerHTML+="<div class='user-container'>"+
                    "<img class='user-image' src=" +avatars[getRandomInt(avatars.length)]+ ">" + "<b> " + data.users[i]+"</b></div>";
                }

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
            alert("Chat socket closed unexpectedly. Try to reload page!");
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

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}