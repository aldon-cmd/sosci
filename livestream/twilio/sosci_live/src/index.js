'use strict';


import {ProgrammableVideo} from './programmable-video';
import {ProgrammableChat} from './programmable-chat';
import {ScreenShare} from './screen-share';

class Sosci{

    static init(identity,token){
    const programmablevideo = new ProgrammableVideo();
    programmablevideo.join(token);
    var room = programmablevideo.room;
    const screenshare = new ScreenShare(room);
    const ProgrammableChat = new ProgrammableChat(identity,token);

    document.getElementById('btn-share-screen').onclick = screenshare.share_screen;


    document.getElementById('btn-unshare-screen').onclick = screenshare.unshare_screen;


    // When we are about to transition away from this page, disconnect
    // from the room, if joined.
    window.addEventListener('beforeunload', programmablevideo.leaveRoomIfJoined);
  }
}


window.Sosci = Sosci;