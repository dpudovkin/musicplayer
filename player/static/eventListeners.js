//document.querySelector('.fa-step-forward').addEventListener("click", function() {
//  Console.debug('next')
//});
//
//document.querySelector('.fa-step-backward').addEventListener("click", function() {
//  Console.debug('back')
//});
$(document).ready(function(){
        const playBtn = document.querySelector('button');
        playBtn.addEventListener("click", () => {
            //console.log(playBtn.title);
        });

        const mediaPlayer = document.querySelector('audio');

        mediaPlayer.addEventListener("loadeddata", () =>{
            console.log("loadeddata")
        })
        mediaPlayer.addEventListener("canplay", () =>{
            console.log("canplay")
        })
        mediaPlayer.addEventListener("canplaythrough", () =>{
            console.log("canplaythrough")
        })

    })
