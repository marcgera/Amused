var g_playlistitems;
var g_currentPlaylistItemIndex;
var g_playing1;
var g_audioElement1;
var g_audioElement2;
var g_Duration1;
var g_Duration2;
var g_TimePassed1=0;
var g_TimePassed2=0;
var g_fadeVolume = 1;
var g_fadeTime = 3000;
var g_FadeTimerInterval = 100;
var g_FadeDelta;
var g_TransitionUngoing = false;


$(document).ready(function () {

    g_FadeDelta = g_FadeTimerInterval / g_fadeTime;
    g_audioElement1 = document.createElement('audio');
    g_audioElement2 = document.createElement('audio');
    g_Audio1FadingInProgress = false;
    g_Audio2FadingInProgress = false;
    g_Duration1 = 99999;
    g_Duration2 = 99999;
    g_video1 = $('#video1')[0];
    g_video2 = $('#video2')[0];

    g_video1.addEventListener('loadedmetadata', function () {
        g_Duration1 = g_video1.duration.toFixed(2);
        updateDurationDiv();
    }, false);

    g_video1.addEventListener('loadedmetadata', function () {
        g_Duration2 = g_video2.duration.toFixed(2);
        updateDurationDiv();
    }, false);

    function updateDurationDiv(){
        dur = 'VideoDuration: ';
        dur = dur.concat( g_Duration1.toString() , ' - ' , g_Duration2.toString()); 
        vd = $('#videoDuration')[0];
        vd.innerHTML  = dur;
    }

    function updateVideoTimePassedDiv(){
        dur = 'Video Time passed: ';
        dur = dur.concat( g_TimePassed1.toString() , ' - ' , g_TimePassed2.toString()); 
        if(g_TransitionUngoing){
            dur = dur.concat('  Fading...');
        }
        vd = $('#videoTimePassed')[0];
        vd.innerHTML  = dur;
    }

    g_video1.addEventListener("timeupdate", function () {
        g_TimePassed1 = g_video1.currentTime.toFixed(2);
        if (g_video1.currentTime > g_Duration1 - g_fadeTime/1000 && !g_TransitionUngoing) {
            g_TransitionUngoing = true;
            g_fadeVolume = 1;
        }
        updateVideoTimePassedDiv();
    });

    g_video2.addEventListener("timeupdate", function () {
        g_TimePassed2 = g_video2.currentTime.toFixed(2);
        if (g_video2.currentTime > g_Duration2 - g_fadeTime/1000 && !g_TransitionUngoing) {
            g_TransitionUngoing = true;
            g_fadeVolume = 1;
        }
        updateVideoTimePassedDiv();
    });

    g_video1.addEventListener("timeupdate", function () {
        $("#currentTimeVideo1").text("Current second Video 1:" + g_audioElement1.currentTime.toFixed(2));

    });

    g_video1.addEventListener("timeupdate", function () {
        $("#currentTimeVideo2").text("Current second Video 2:" + g_audioElement2.currentTime.toFixed(2));
    });




    function fadeComplete() {
        alert('fade complete');
    }

    $.get("/getPlaylistItems2", function (data, status) {
        g_playlistitems = JSON.parse(data);
        preLoadMedia();
    });


    $('#play').on('click', function () {
        doPlay();
    })

    $('#stop').on('click', function () {
        doStop();
    })

    

    function preLoadMedia(){
        g_currentPlaylistItem = 0;
        g_playing1 = true;
        g_currentPlaylistItemIndex = 0;
        plItem = g_playlistitems[0];
        srcAudio = '../static/music/' + plItem.music_name;
        srcVideo =  '../static/video/' + plItem.videos_name;
        g_audioElement1.setAttribute('src', srcAudio);
        g_video1.setAttribute('src',srcVideo);

        if (g_playlistitems.length>1){
            plItem = g_playlistitems[1];
            srcAudio = '../static/music/' + plItem.music_name;
            srcVideo =  '../static/video/' + plItem.videos_name;
            g_audioElement2.setAttribute('src', srcAudio);
            g_video2.setAttribute('src',srcVideo);
        }

        g_video1.volume = 0;
        g_video2.volume = 0;
        g_video1.style.opacity ='1';
        g_video2.style.opacity ='0';
    }

    function doPlay() {
        g_audioElement1.play();
        g_video1.play();
    }

    function doStop() {
        g_audioElement1.pause();
        g_audioElement2.pause();
        g_video1.pause();
        g_video2.pause();
    }

    function playNext() {

        if (g_currentPlaylistItemIndex == g_playlistitems.length - 1) {
            g_currentPlaylistItemIndex = 0;
        }
        else {
            g_currentPlaylistItemIndex = g_currentPlaylistItemIndex + 1;
        }

        plItem = g_playlistitems[g_currentPlaylistItemIndex];
        srcAudio = '../static/music/' + plItem.music_name;
        srcVideo = '../static/video/' + plItem.videos_name;

        if (g_playing1) {
            audioElement = g_audioElement2;
            videoElement = g_video2;
            g_Audio2FadingInProgress = false;
            g_playing1 = false;
        }
        else {
            audioElement = g_audioElement1;
            videoElement = g_video1;
            g_Audio1FadingInProgress = false;
            g_playing1 = true;
        }

        g_audioElement1.volume = 1;
        g_audioElement2.volume = 1;

        audioElement.setAttribute('src', srcAudio);
        videoElement.setAttribute('src', srcVideo);
        audioElement.play();
        videoElement.play();
    }

    function getCurrentAudioElement() {
        if (g_playing1) {
            return g_audioElement1;
        }
        else {
            return g_audioElement2;
        }
    }

    function getCurrentVideoElement() {
        if (g_playing1) {
            return g_video1;
        }
        else {
            return g_video2;
        }
    }

    function getNextVideoElement() {
        if (!g_playing1) {
            return g_video1;
        }
        else {
            return g_video2;
        }
    }


    function fade() {
        current_frame = 0;
        my_timer = setInterval(setVolume(), 200);
    }

    tmr = setInterval(() => {
        if (!g_TransitionUngoing) {return}
        $("#currentVolume2").text('Fadevolume:' + g_fadeVolume.toString());
        currentAudio = getCurrentAudioElement();
        currentVideo = getCurrentVideoElement();
       
        currentAudio.volume = g_fadeVolume;
        currentVideo.style.opacity = g_fadeVolume.toString();
        getNextVideoElement().style.opacity = (1-g_fadeVolume).toString();

        g_fadeVolume = g_fadeVolume-g_FadeDelta;
        if (g_fadeVolume<0){
            g_TransitionUngoing = false;
            currentAudio.pause();
            currentVideo.style.opacity ='0';

            currentVideo.pause();
            g_fadeVolume = 1;
            playNext();
        }

    }, g_FadeTimerInterval);



});