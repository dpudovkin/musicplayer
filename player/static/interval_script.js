var roomName, roomSocket
var audio

const stringPlay = "PLAY"
const stringPause = "PAUSE"
const stringContinue = "CONTINUE"
const stringSync = "SYNC"


function SyncContinue(){
      roomSocket.send(JSON.stringify({
         'type':'sync',
         'message': stringContinue,
         'time': Date.now(),
         'action': stringContinue
     }));
}

function SyncPlay(){
     roomSocket.send(JSON.stringify({
         'type':'sync',
         'message': 'play',
         'time': Date.now(),
         'action': stringPlay
     }));
}

function SyncTime(){
      roomSocket.send(JSON.stringify({
                'action': "SYNC",
                'src_time': 0,
                'js_time':  parseInt(Date.now(),10)
      }));
}

function StartSyncTime(){
      roomSocket.send(JSON.stringify({
                'action': "START_SYNC",
      }));
}

function SyncPause(){
     roomSocket.send(JSON.stringify({
         'type':'sync',
         'message': 'pause',
         'time': Date.now(),
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
            if (audioAction == stringSync){
                sendSyncMessage(data)
                return
            }

            audioAction = data.action.toString().toUpperCase()
            msg = data.message
            src_time = parseInt(data.time,10)
            delta =  parseInt(data.delta,10)
            if (audioAction==stringPlay){
                //setTimeout(AudioPlay,delta-(parseInt(Date.now(),10)-src_time))
                //setTimeout(AudioPlay,200-delta)
                AudioPlay()
            } else if (audioAction==stringPause){
                //setTimeout(AudioPause,delta-(parseInt(Date.now(),10)-src_time))
                //setTimeout(AudioPause,200-delta)
                AudioPause()
            } else if (audioAction==stringContinue){
                AudioContinue()
               // setTimeout(AudioContinue,200-delta)
                //setTimeout(AudioContinue, delta-(parseInt(Date.now(),10)-src_time))
            }

            var a = 1
        };

        function sendSyncMessage(data){
              roomSocket.send(JSON.stringify({
                'js_time':  parseInt(Date.now(),10),
                'src_time': data.src_time,
                'action': stringSync,
                'type':'sync'
              }));
        }

        roomSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
})

