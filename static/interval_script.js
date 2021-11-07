var roomName, roomSocket
var audio

const stringPlay = "PLAY"
const stringPause = "PAUSE"
const stringContinue = "CONTINUE"


function SyncContinue(){
      roomSocket.send(JSON.stringify({
         'type':'sync',
         'message': stringContinue,
         'time': Date.now(),
         'delta': 1000,
         'action': stringContinue
     }));
}

function SyncPlay(){
     roomSocket.send(JSON.stringify({
         'type':'sync',
         'message': 'play',
         'time': Date.now(),
         'delta': 1000,
         'action': stringPlay
     }));
}

function SyncPause(){
     roomSocket.send(JSON.stringify({
         'type':'sync',
         'message': 'pause',
         'time': Date.now(),
         'delta': 1000,
         'action': stringPause
     }));
}

function AudioPlay(){
    audio.currentTime=0
    audio.play()
}

function AudioPause(){
    audio.pause()
}

function AudioContinue(){
    audio.play()
}

$(document).ready(function(){
       audio = document.querySelector("#customAudio")
       roomName = JSON.parse(document.getElementById('room-name').textContent);
       roomSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/app/'
            + roomName
            + '/'
       );

       roomSocket.onmessage = function(e) {
            console.debug("socket message")
            const data = JSON.parse(e.data);
            audioAction = data.action.toString().toUpperCase()
            msg = data.message
            src_time = parseInt(data.time,10)
            delta =  parseInt(data.delta,10)

            if (audioAction==stringPlay){
                setTimeout(AudioPlay,delta-(parseInt(Date.now(),10)-src_time))
            } else if (audioAction==stringPause){
                setTimeout(AudioPause,delta-(parseInt(Date.now(),10)-src_time))
            } else if (audioAction==stringContinue){
                setTimeout(AudioContinue, delta-(parseInt(Date.now(),10)-src_time))
            }
        };

        roomSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
})

