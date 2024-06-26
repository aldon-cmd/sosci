'use strict';

import $ from 'jquery';
import { JitsiMeetJS } from 'lib-jitsi-meet.min'

class VideoConference {

	constructor(){
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

            this.connection = null;
            this.isJoined = false;
            this.room = null;

            this.localTracks = [];
            this.remoteTracks = {};

			this.isVideo = true;

			$(window).bind('beforeunload', this.unload);
			$(window).bind('unload', this.unload);

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
			    onConnectionSuccess);
			this.connection.addEventListener(
			    JitsiMeetJS.events.connection.CONNECTION_FAILED,
			    onConnectionFailed);
			this.connection.addEventListener(
			    JitsiMeetJS.events.connection.CONNECTION_DISCONNECTED,
			    disconnect);

			JitsiMeetJS.mediaDevices.addEventListener(
			    JitsiMeetJS.events.mediaDevices.DEVICE_LIST_CHANGED,
			    onDeviceListChanged);

			this.connection.connect();

			JitsiMeetJS.createLocalTracks({ devices: [ 'audio', 'video' ] })
			    .then(onLocalTracks)
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
	            () => console.log('local track muted'));
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
	}

	/**
	 *
	 * @param id
	 */
	onUserLeft(id) {
	    console.log('user left');
	    if (!this.remoteTracks[id]) {
	        return;
	    }
	    const tracks = this.remoteTracks[id];

	    for (let i = 0; i < tracks.length; i++) {
	        tracks[i].detach($(`#${id}${tracks[i].getType()}`));
	    }
	}

	/**
	 * That function is called when connection is established successfully
	 */
	onConnectionSuccess() {
	    this.room = this.connection.initJitsiConference('conference', this.confOptions);
	    this.room.on(JitsiMeetJS.events.conference.TRACK_ADDED, onRemoteTrack);
	    this.room.on(JitsiMeetJS.events.conference.TRACK_REMOVED, track => {
	        console.log(`track removed!!!${track}`);
	    });
	    this.room.on(
	        JitsiMeetJS.events.conference.CONFERENCE_JOINED,
	        onConferenceJoined);
	    this.room.on(JitsiMeetJS.events.conference.USER_JOINED, id => {
	        console.log('user join');
	        this.remoteTracks[id] = [];
	    });
	    this.room.on(JitsiMeetJS.events.conference.USER_LEFT, onUserLeft);
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
	        onConnectionSuccess);
	    this.connection.removeEventListener(
	        JitsiMeetJS.events.connection.CONNECTION_FAILED,
	        onConnectionFailed);
	    this.connection.removeEventListener(
	        JitsiMeetJS.events.connection.CONNECTION_DISCONNECTED,
	        disconnect);
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
	switchVideo() { // eslint-disable-line no-unused-vars
	    this.isVideo = !this.isVideo;
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
	                () => console.log('local track muted'));
	            this.localTracks[1].addEventListener(
	                JitsiMeetJS.events.track.LOCAL_TRACK_STOPPED,
	                () => console.log('local track stoped'));
	            this.localTracks[1].attach($('#localVideo1')[0]);
	            this.room.addTrack(this.localTracks[1]);
	        })
	        .catch(error => console.log(error));
	}

	/**
	 *
	 * @param selected
	 */
	changeAudioOutput(selected) { // eslint-disable-line no-unused-vars
	    JitsiMeetJS.mediaDevices.setAudioOutputDevice(selected.value);
	}

}

export { VideoConference }