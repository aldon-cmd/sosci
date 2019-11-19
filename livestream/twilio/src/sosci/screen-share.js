'use strict';

import Video from 'twilio-video';

class ScreenShare{
	constructor(room,programmablevideo){
		this.room = room;
		this.programmablevideo = programmablevideo;
		this.screen_track = null;
	}

	share_screen(){
		if(this.screen_track){
			this.unshare_screen();
			this.programmablevideo.create_local_tracks();
		}
	  
	  var stream = navigator.mediaDevices.getDisplayMedia().then(stream => {
	  this.screen_track = stream.getVideoTracks()[0];

	  this.screen_track.oninactive = ()=> {this.programmablevideo.create_local_tracks();};
	  var trackName = this.room.localParticipant.identity +'/screen-share'
	  var videoTrack = Video.LocalVideoTrack(this.screen_track,{name: trackName});
	  this.room.localParticipant.publishTrack(videoTrack);
	  document.getElementById('btn-share-screen').style.display = 'none';
	  document.getElementById('btn-unshare-screen').style.display = 'inline';
	  }); 
	}

	unshare_screen() {
		if(this.screen_track){
		  this.room.localParticipant.unpublishTrack(this.screen_track);
		  this.screen_track = null;
		  document.getElementById('btn-share-screen').style.display = 'inline';
		  document.getElementById('btn-unshare-screen').style.display = 'none';
		}
	}
}

export { ScreenShare }