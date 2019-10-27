class ScreenShare{
	constructor(room){
		this.room = room;
		this.screen_track = null;
	}

	share_screen(){
	  var stream = navigator.mediaDevices.getDisplayMedia().then(stream => {
	  this.screen_track = stream.getVideoTracks()[0];
	  var trackName = this.room.localParticipant.identity +'/screen-share'
	  var videoTrack = Video.LocalVideoTrack(this.screen_track,{name: trackName});
	  this.room.localParticipant.publishTrack(videoTrack);
	  document.getElementById('btn-share-screen').style.display = 'none';
	  document.getElementById('btn-unshare-screen').style.display = 'inline';
	  }); 
	}

	unshare_screen(room,screen_track) {
	  room.localParticipant.unpublishTrack(screen_track);
	  this.screen_track = null;
	  document.getElementById('btn-share-screen').style.display = 'inline';
	  document.getElementById('btn-unshare-screen').style.display = 'none';
	};
}

export { ScreenShare }