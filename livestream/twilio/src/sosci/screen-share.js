'use strict';

import Video from 'twilio-video';

class ScreenShare {
	constructor(room, programmablevideo) {
		this.room = room;
		this.programmablevideo = programmablevideo;
		this.screen_track = null;

		this.btn_share_screen = document.getElementById('btn-share-screen');

		this.btn_share_screen.onclick = () => this.toggle_share_screen();
	}

	toggle_share_screen() {
		

		if (this.screen_track) {
			this.unshare_screen();


			this.programmablevideo.create_local_tracks();
		}

		var stream = navigator.mediaDevices.getDisplayMedia().then(stream => {
			this.screen_track = stream.getVideoTracks()[0];

			this.screen_track.oninactive = () => { console.log("hello");}; //this.programmablevideo.create_local_tracks(); };
			var trackName = this.room.localParticipant.identity + '/screen-share'
			var videoTrack = Video.LocalVideoTrack(this.screen_track, { name: trackName });
			var i_elements_array = this.btn_share_screen.getElementsByTagName("i");
			

			if (i_elements_array != undefined && i_elements_array.length != 0) {

				i_elements_array[0].className = "fas fa-eye-slash";

			}
			this.room.localParticipant.publishTrack(videoTrack);
		});
	}

	unshare_screen() {
		var i_elements_array = this.btn_share_screen.getElementsByTagName("i");
		if (this.screen_track) {
			this.room.localParticipant.unpublishTrack(this.screen_track);
			this.screen_track = null;

			if (i_elements_array != undefined && i_elements_array.length != 0) {

				i_elements_array[0].className = "fas fa-eye";

			}
		}
	}
}

export { ScreenShare }