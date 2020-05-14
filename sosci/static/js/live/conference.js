class VideoConference {

	constructor(local_participant_name){
            /* global $, JitsiMeetJS */

            this.options = {
                hosts: {
                    domain: 'sosci.tv',
                    muc: 'conference.sosci.tv' // FIXME: use XEP-0030
                },
                bosh: 'https://sosci.tv/http-bind', // FIXME: use xep-0156 for that

                // The name of client node advertised in XEP-0115 'c' stanza
                clientNode: 'http://jitsi.org/jitsimeet'
            };

            this.confOptions = {
                openBridgeChannel: true
            };

            this.local_participant_name = local_participant_name;

            this.connection = null;
            this.isJoined = false;
            this.room = null;
            this.policy = {audio: false, video:false}

            this.localTracks = [];
            this.remoteTracks = {};

			this.isVideo = true;


			this.btn_toggle_audio = document.getElementById('btn-toggle-audio');
			this.btn_toggle_video = document.getElementById('btn-toggle-video');

			this.btn_toggle_audio.onclick = () => this.toggle_audio();
			this.btn_toggle_video.onclick = () => this.toggle_video();

			this.btn_share_screen = document.getElementById('btn-share-screen');

		    this.btn_share_screen.onclick = () => this.toggle_share_screen();

		    // When we are about to transition away from this page, disconnect
		    // from the room, if joined.
		    $(window).bind('beforeunload', () => this.unload());
			$(window).bind('unload', () => this.unload());

	        // Get handle to the chat div
	        this.chat_panel = document.getElementById('chat-panel');

	        this.input = document.getElementById('chat-input');



	        this.input.addEventListener('keydown', (e) => this.key_logger(e));			

			// JitsiMeetJS.setLogLevel(JitsiMeetJS.logLevels.ERROR);
			this.initOptions = {
			    disableAudioLevels: true,

			    // The ID of the jidesha extension for Chrome.
			    desktopSharingChromeExtId: 'mbocklcggfhnbahlnepmldehdhpjfcjp',

			    // Whether desktop sharing should be disabled on Chrome.
			    desktopSharingChromeDisabled: false,

			    // The media sources to use when using screen sharing with the Chrome
			    // extension.
			    desktopSharingChromeSources: [ 'screen', 'window' ],

			    // Required version of Chrome extension
			    desktopSharingChromeMinExtVersion: '0.1',

			    // Whether desktop sharing should be disabled on Firefox.
			    desktopSharingFirefoxDisabled: true
			};

			JitsiMeetJS.init(this.initOptions);

			this.connection = new JitsiMeetJS.JitsiConnection(null, null, this.options);

			this.connection.addEventListener(
			    JitsiMeetJS.events.connection.CONNECTION_ESTABLISHED,
			    () => this.onConnectionSuccess());
			this.connection.addEventListener(
			    JitsiMeetJS.events.connection.CONNECTION_FAILED,
			    () => this.onConnectionFailed());
			this.connection.addEventListener(
			    JitsiMeetJS.events.connection.CONNECTION_DISCONNECTED,
			    () => this.disconnect());

			JitsiMeetJS.mediaDevices.addEventListener(
			    JitsiMeetJS.events.mediaDevices.DEVICE_LIST_CHANGED,
			    () => this.onDeviceListChanged());

			this.connection.connect();

			JitsiMeetJS.createLocalTracks({ devices: [ 'audio', 'video' ] })
			    .then((tracks) => this.onLocalTracks(tracks))
			    .catch(error => {
			        throw error;
			    });

			if (JitsiMeetJS.mediaDevices.isDeviceChangeAvailable('output')) {
			    JitsiMeetJS.mediaDevices.enumerateDevices(devices => {
			        const audioOutputDevices
			            = devices.filter(d => d.kind === 'audiooutput');

			        if (audioOutputDevices.length > 1) {
			            $('#audioOutputSelect').html(
			                audioOutputDevices
			                    .map(
			                        d =>
			                            `<option value="${d.deviceId}">${d.label}</option>`)
			                    .join('\n'));

			            $('#audioOutputSelectWrapper').show();
			        }
			    });
			}						
	}

	create_participants_list_item(id){
		let participant = this.room.getParticipantById(id);
	    let participants_list = document.getElementById('participants-list');
	    let participants_list_item = document.createElement("LI"); 
	    let participants_list_item_content;
	    let paricipant_full_name;

	    participants_list_item.setAttribute("id",participant.getId());

	    paricipant_full_name = participant.getDisplayName();

	    participants_list_item_content = '<div class="participant">'+ paricipant_full_name +'</div><i class="fas fa-circle"></i>';

	    participants_list_item.innerHTML = participants_list_item_content;

	    participants_list.appendChild(participants_list_item);     
	}

	delete_participants_list_item(participant){
	  var participants_list_item = document.getElementById(participant.getId());
	  participants_list_item.parentNode.removeChild(participants_list_item);
	}

	populate_participant_list(room){


	   this.room.getParticipants().forEach((participant) => {this.create_participants_list_item(participant.getId());});
	}	

	get_audio_track(){
		return this.room.getLocalTracks().find((track) => track.getType() === "audio");
	}

	get_video_track(){
		return this.room.getLocalTracks().find((track) => track.getType() === "video");
	}	

	toggle_mic_btn(){
		let i_elements_array = this.btn_toggle_audio.getElementsByTagName("i");

		if (i_elements_array != undefined && i_elements_array.length != 0) {
			if (i_elements_array[0].className === "fas fa-microphone"){
				i_elements_array[0].className  = "fas fa-microphone-slash";
			}else{
				i_elements_array[0].className  = "fas fa-microphone";
			}	
		}		
	}

	toggle_video_btn(){
		let i_elements_array = this.btn_toggle_video.getElementsByTagName("i");

		if (i_elements_array != undefined && i_elements_array.length != 0) {
			if (i_elements_array[0].className === "fas fa-video"){
				i_elements_array[0].className  = "fas fa-video-slash";
			}else{
				i_elements_array[0].className  = "fas fa-video";
			}	
		}		
	}

	toggle_audio(){
	   let audio_track = this.get_audio_track();

      if (audio_track.isMuted()) {
        audio_track.unmute();
      } else {
        audio_track.mute();
      }
	}

	toggle_video(){
	   let video_track = this.get_video_track();

      if (video_track.isMuted()) {
        video_track.unmute();
      } else {
        video_track.mute();
      }	
	}

	toggle_device_btn(track){
		let mediatype = track.getType();
		console.log('local track mute toggled');

		if (mediatype === "audio"){
			 this.toggle_mic_btn();
		}
		else if(mediatype === "video"){
			this.toggle_video_btn();
		}
	}		

	/**
	 * Handles local tracks.
	 * @param tracks Array with JitsiTrack objects
	 */
	onLocalTracks(tracks) {
	    this.localTracks = tracks;
	    for (let i = 0; i < this.localTracks.length; i++) {
	        this.localTracks[i].addEventListener(
	            JitsiMeetJS.events.track.TRACK_AUDIO_LEVEL_CHANGED,
	            audioLevel => console.log(`Audio Level local: ${audioLevel}`));
	        this.localTracks[i].addEventListener(
	            JitsiMeetJS.events.track.TRACK_MUTE_CHANGED,
	            (track) => this.toggle_device_btn(track));
	        this.localTracks[i].addEventListener(
	            JitsiMeetJS.events.track.LOCAL_TRACK_STOPPED,
	            () => console.log('local track stoped'));
	        this.localTracks[i].addEventListener(
	            JitsiMeetJS.events.track.TRACK_AUDIO_OUTPUT_CHANGED,
	            deviceId =>
	                console.log(
	                    `track audio output device was changed to ${deviceId}`));
	        if (this.localTracks[i].getType() === 'video') {
	            $('.video-player-container').append(`<video autoplay='1' id='localVideo${i}' />`);
	            this.localTracks[i].attach($(`#localVideo${i}`)[0]);
	        } else {
	            $('.video-player-container').append(
	                `<audio autoplay='1' muted='true' id='localAudio${i}' />`);
	            this.localTracks[i].attach($(`#localAudio${i}`)[0]);
	        }
	        if (this.isJoined) {
	            this.room.addTrack(this.localTracks[i]);
	        }
	    }
	}

	/**
	 * Handles remote tracks
	 * @param track JitsiTrack object
	 */
	onRemoteTrack(track) {
	    if (track.isLocal()) {
	        return;
	    }
	    const participant = track.getParticipantId();

	    if (!this.remoteTracks[participant]) {
	        this.remoteTracks[participant] = [];
	    }
	    const idx = this.remoteTracks[participant].push(track);

	    track.addEventListener(
	        JitsiMeetJS.events.track.TRACK_AUDIO_LEVEL_CHANGED,
	        audioLevel => console.log(`Audio Level remote: ${audioLevel}`));
	    track.addEventListener(
	        JitsiMeetJS.events.track.TRACK_MUTE_CHANGED,
	        () => console.log('remote track muted'));
	    track.addEventListener(
	        JitsiMeetJS.events.track.LOCAL_TRACK_STOPPED,
	        () => console.log('remote track stoped'));
	    track.addEventListener(JitsiMeetJS.events.track.TRACK_AUDIO_OUTPUT_CHANGED,
	        deviceId =>
	            console.log(
	                `track audio output device was changed to ${deviceId}`));
	    const id = participant + track.getType() + idx;

	    if (track.getType() === 'video') {
	        $('body').append(
	            `<video autoplay='1' id='${participant}video${idx}' />`);
	    } else {
	        $('body').append(
	            `<audio autoplay='1' id='${participant}audio${idx}' />`);
	    }
	    track.attach($(`#${id}`)[0]);
	    console.log(`track added!!!${track}`);
	}

	onRemoveRemoteTrackContainer(track) {
	    if (track.isLocal()) {
	        return;
	    }

	    const container = track.containers.find((container) => container !== undefined);

	    $(container).remove();
	}
	/**
	 * That function is executed when the conference is joined
	 */
	onConferenceJoined() {
	    console.log('conference joined!');
	    this.isJoined = true;
	    for (let i = 0; i < this.localTracks.length; i++) {
	        this.room.addTrack(this.localTracks[i]);
	    }
	    this.populate_participant_list();
	}

	/**
	 *
	 * @param id
	 */
	onUserLeft(id,participant) {
	    console.log('user left');
	    if (!this.remoteTracks[id]) {
	        return;
	    }
	    const tracks = this.remoteTracks[id];

	    for (let i = 0; i < tracks.length; i++) {
	        tracks[i].detach($(`#${id}${tracks[i].getType()}${i+1}`)[0]);
	        $(`#${id}${tracks[i].getType()}${i+1}`).remove();
	    }

	    this.delete_participants_list_item(participant);
	}

	/**
	 * That function is called when connection is established successfully
	 */
	onConnectionSuccess() {
	    this.room = this.connection.initJitsiConference('conference', this.confOptions);
	    this.room.setDisplayName(this.local_participant_name);
	    this.room.on(JitsiMeetJS.events.conference.MESSAGE_RECEIVED, (id, text, ts) => this.onMessageReceived(id, text, ts));
	    this.room.on(JitsiMeetJS.events.conference.TRACK_ADDED, (track) => this.onRemoteTrack(track));
	    this.room.on(JitsiMeetJS.events.conference.TRACK_REMOVED, track => {
	        console.log(`track removed!!!${track}`);
	        this.onRemoveRemoteTrackContainer(track);
	    });
	    this.room.on(
	        JitsiMeetJS.events.conference.CONFERENCE_JOINED,
	        () => this.onConferenceJoined());
	    this.room.on(JitsiMeetJS.events.conference.USER_JOINED, id => {
	        console.log('user join');
	        this.create_participants_list_item(id);
	        this.remoteTracks[id] = [];
	    });
	    this.room.on(JitsiMeetJS.events.conference.USER_LEFT, (id,participant) => this.onUserLeft(id,participant));
	    this.room.on(JitsiMeetJS.events.conference.TRACK_MUTE_CHANGED, track => {
	        console.log(`${track.getType()} - ${track.isMuted()}`);
	    });
	    this.room.on(
	        JitsiMeetJS.events.conference.DISPLAY_NAME_CHANGED,
	        (userID, displayName) => console.log(`${userID} - ${displayName}`));
	    this.room.on(
	        JitsiMeetJS.events.conference.TRACK_AUDIO_LEVEL_CHANGED,
	        (userID, audioLevel) => console.log(`${userID} - ${audioLevel}`));
	    this.room.on(
	        JitsiMeetJS.events.conference.PHONE_NUMBER_CHANGED,
	        () => console.log(`${this.room.getPhoneNumber()} - ${this.room.getPhonePin()}`));
	    this.room.join();
	    this.room.setStartMutedPolicy(this.policy);
	}

	onMessageReceived(id, text, ts){
	    let message_container = document.createElement("DIV"); 
	    message_container.setAttribute("class","live-chat");

	    //avoid xss with textContent
	    let message_txt = document.createTextNode(text);
	    let message_span = document.createElement("SPAN");
	    message_span.appendChild(message_txt);



	    let chat_list_item = '<div class="">'+
	                '<span class="chat-badge">'+
	                  '<i class="fas fa-user-circle"></i>'+
	                '</span>'+
	                '<span class="chat-line-username">'+
	                  '<span>'+this.local_participant_name+'<span>:</span></span>'+
	                '</span>'+
	                '<span>'+
	                  '<span>'+message_span.textContent+'</span>'+
	                '</span>'+
	             '</div>';
	    message_container.innerHTML = chat_list_item;


	    this.chat_panel.appendChild(message_container);
	}

    // Send a new message to the general channel
	key_logger(e) {

	    if (e.keyCode == 13) {
	      this.room.sendTextMessage(this.input.value);
	      this.input.value = '';
	    }
	}

	/**
	 * This function is called when the connection fail.
	 */
	onConnectionFailed() {
	    console.error('Connection Failed!');
	}

	/**
	 * This function is called when the connection fail.
	 */
	onDeviceListChanged(devices) {
	    console.info('current devices', devices);
	}

	/**
	 * This function is called when we disconnect.
	 */
	disconnect() {
	    console.log('disconnect!');
	    this.connection.removeEventListener(
	        JitsiMeetJS.events.connection.CONNECTION_ESTABLISHED,
	        () => this.onConnectionSuccess());
	    this.connection.removeEventListener(
	        JitsiMeetJS.events.connection.CONNECTION_FAILED,
	        () => this.onConnectionFailed());
	    this.connection.removeEventListener(
	        JitsiMeetJS.events.connection.CONNECTION_DISCONNECTED,
	        () => this.disconnect());
	}

	/**
	 *
	 */
	unload() {
	    for (let i = 0; i < this.localTracks.length; i++) {
	        this.localTracks[i].dispose();
	    }
	    this.room.leave();
	    this.connection.disconnect();
	}



	/**
	 *
	 */
	toggle_share_screen() { // eslint-disable-line no-unused-vars
	    this.isVideo = !this.isVideo;
	    let i_elements_array = this.btn_share_screen.getElementsByTagName("i");

	    if (this.localTracks[1]) {
	        this.localTracks[1].dispose();
	        this.localTracks.pop();
	    }
	    JitsiMeetJS.createLocalTracks({
	        devices: [ this.isVideo ? 'video' : 'desktop' ]
	    })
	        .then(tracks => {
	            this.localTracks.push(tracks[0]);
	            this.localTracks[1].addEventListener(
	                JitsiMeetJS.events.track.TRACK_MUTE_CHANGED,
	                () => console.log('TRACK_MUTE_CHANGED fired!!!'));
	            this.localTracks[1].addEventListener(
	                JitsiMeetJS.events.track.LOCAL_TRACK_STOPPED,
	                () => this.unshare_screen());
	            this.localTracks[1].attach($('#localVideo1')[0]);
	            this.room.addTrack(this.localTracks[1]);
	            this.toggle_screen_share_btn();
	        })
	        .catch(error => console.log(error));
	}

	toggle_screen_share_btn(){
		let i_elements_array = this.btn_share_screen.getElementsByTagName("i");
		if (i_elements_array != undefined && i_elements_array.length != 0) {

			if(this.isVideo){
				i_elements_array[0].className = "fas fa-eye";

			}else{

				i_elements_array[0].className = "fas fa-eye-slash";
			}
			

		}
	}

	unshare_screen(){

		this.toggle_share_screen();
		this.toggle_screen_share_btn();


	}

	/**
	 *
	 * @param selected
	 */
	changeAudioOutput(selected) { // eslint-disable-line no-unused-vars
	    JitsiMeetJS.mediaDevices.setAudioOutputDevice(selected.value);
	}

}

class ConferenceUI {

	constructor(){
		this.participants_panel = document.getElementById('participants-panel');
		this.video_controls_panel = document.getElementById('video-controls-panel');
		this.chat_panel = document.getElementById('chat-panel');

		document.getElementById('btn-toggle-participants-panel').onclick = () => this.toggle_participants_panel();
		document.getElementById('btn-toggle-chat-panel').onclick = () => this.toggle_chat_panel();
		document.getElementById('btn-toggle-video-controls-panel').onclick = () => this.toggle_video_controls_panel();
	}

	toggle_participants_panel(){
		this.participants_panel.style.cssText = 'display:block !important';
		this.video_controls_panel.style.cssText = 'display:none !important';
		this.chat_panel.style.cssText = 'display:none !important';
	}

	toggle_chat_panel(){
		this.participants_panel.style.cssText = 'display:none !important';
		this.video_controls_panel.style.cssText = 'display:none !important';
		this.chat_panel.style.cssText = 'display:block !important';
	}

	toggle_video_controls_panel(){
		this.participants_panel.style.cssText = 'display:none !important';
		this.video_controls_panel.style.cssText = 'display:block !important';
		this.chat_panel.style.cssText = 'display:none !important';
	}
			
}