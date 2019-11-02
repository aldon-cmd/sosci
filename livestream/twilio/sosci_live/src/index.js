'use strict';


import {ProgrammableVideo} from './programmable-video';
import {ProgrammableChat} from './programmable-chat';
import {ScreenShare} from './screen-share';

class Sosci{

    static init(identity,token){
    const programmablevideo = new ProgrammableVideo();
    var room;
    var screenshare;
    var programmablechat;
    var room_sid_input
    programmablevideo.join(token).then( function(active_room) { 

    room = active_room
    room_sid_input = document.getElementById('input-room-sid');   
    room_sid_input.value = room.sid

    screenshare = new ScreenShare(room);
    programmablechat = new ProgrammableChat(identity,token);

    document.getElementById('btn-share-screen').onclick = screenshare.share_screen;


    document.getElementById('btn-unshare-screen').onclick = screenshare.unshare_screen;


    // When we are about to transition away from this page, disconnect
    // from the room, if joined.
    window.addEventListener('beforeunload', programmablevideo.leaveRoomIfJoined);

    });

  }
}


window.Sosci = Sosci;