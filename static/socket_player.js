$(document).ready(function(){

        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const playCommand = 'play', pauseCommand = 'pause', nextVoteCommand = 'vote';
        const audioUpdateCommand = 'audio_update';
        const userConnectCommand = 'user_connect', userDisconnectCommand = 'user_disconnect';
        const voteUpdateCommand = 'vote_update';
        const actionHeader = 'action'

        const likeCommand = 'like'
        const unlikeCommand = 'unlike'


//        const connectedCount = document.querySelector('#connected')
//        const votedCount = document.querySelector('#voted')

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



        var voted = 0;
        var connected =0;

        const playBtn = document.querySelector('#playButton');
        const pauseBtn = document.querySelector('#pauseButton');
        const nextBtn = document.querySelector('#nextButton');
        const audio =  document.querySelector('audio');
        const likeBtn = document.querySelector('#like-button');
        const songText = document.querySelector('#songText');
        const voteBar = document.querySelector('#vote-bar');

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


            if (msg.toLowerCase()==likeCommand){
                console.log('Like')
                likeBtn.className = "btn btn-danger";
                likeBtn.innerHTML="Unlike"
            }

            if (msg.toLowerCase()==unlikeCommand){
                console.log('UnLike')
                likeBtn.className = "btn btn-light";
                likeBtn.innerHTML="Like"
            }


            if (msg.toLowerCase()==userConnectCommand || msg.toLowerCase()==userDisconnectCommand){
                var avatars = new Array('/media/cat1.png', '/media/cat2.png', '/media/cat3.png');

                connected = data.users.length
                voteBar.style.width = ((voted/connected*100)+"%");
                voteBar.innerHTML = ((voted/connected*100)+"%");

                usersContainer.innerHTML=""
                for (let i = 0; i < data.users.length; i += 1) {
                    usersContainer.innerHTML+='<div class="col-1 m-2" align="center"> <div class="row">'+
                    '<img src="'+avatars[getRandomInt(avatars.length)]+'" style="height: 30pt; border-radius: 10%;">'+
                    '</div> <div class="row"> <small><b>'+data.users[i]+'</b></small></div></div>';
                }

                console.log(data.users)
                console.log(data.username)

            }

            if (msg.toLowerCase()==voteUpdateCommand){
                voted = data.vote_count
                voteBar.style.width = ((voted/connected*100)+"%");
                voteBar.innerHTML = ((voted/connected*100)+"%");
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

        likeBtn.addEventListener("click", () => {
            roomSocket.send(JSON.stringify({
                'action': likeCommand
            }));
        });
})

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}