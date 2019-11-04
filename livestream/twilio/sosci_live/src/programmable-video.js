'use strict';
import Video from 'twilio-video';

class ProgrammableVideo {

	constructor(){
		this.room = null;
		this.previewTracks = null;
	}

	// Attach the Tracks to the DOM.
	attachTracks(tracks, container) {
	  tracks.forEach(function(track) {
	    container.appendChild(track.attach());
	  });
	}

	// Attach the Participant's Tracks to the DOM.
	attachParticipantTracks(participant, container) {
	  var tracks = Array.from(participant.tracks.values());
	  this.attachTracks(tracks, container);
	}

	// Detach the Tracks from the DOM.
	detachTracks(tracks) {
	  tracks.forEach(function(track) {
	    track.detach().forEach(function(detachedElement) {
	      detachedElement.remove();
	    });
	  });
	}

	// Detach the Participant's Tracks from the DOM.
	detachParticipantTracks(participant) {
	  var tracks = Array.from(participant.tracks.values());
	  this.detachTracks(tracks);
	}

	create_participants_list_item(participant){
	    var participants_list = document.getElementById('participants-list');
	    var participants_list_item = document.createElement("LI"); 
	    var participants_list_item_content;
	    var participant_identity;
	    var paricipant_full_name;

	    participants_list_item.setAttribute("id",participant.sid);

	    participant_identity = participant.identity.split("/");

	    paricipant_full_name = 1 in participant_identity ? participant_identity[1] : "";

	    participants_list_item_content = '<div class="participant">'+ paricipant_full_name +'</div><i class="fas fa-circle"></i>';

	    participants_list_item.innerHTML = participants_list_item_content;

	    participants_list.appendChild(participants_list_item);     
	}

	delete_participants_list_item(participant){
	  var participants_list_item = document.getElementById(participant.sid);
	  participants_list_item.parentNode.removeChild(participants_list_item);
	}

	populate_participant_list(room){


	     room.participants.forEach((participant) => {this.create_participants_list_item(participant);});
	}

	// Successfully connected!
	roomJoined(room) {
	  this.room = room;

	  console.log("Joined Room");

	  this.populate_participant_list(room);

	  // Attach LocalParticipant's Tracks, if not already attached.
	  var previewContainer = document.getElementById('local-media');
	  if (!previewContainer.querySelector('video')) {
	    this.attachParticipantTracks(room.localParticipant, previewContainer);
	  }

	  // Attach the Tracks of the Room's Participants.
	  room.participants.forEach((participant) => {
	    console.log("Already in Room: '" + participant.identity + "'");
	    var previewContainer = document.getElementById('remote-media');
	    this.attachParticipantTracks(participant, previewContainer);
	  });

	  // When a Participant joins the Room, log the event.
	  room.on('participantConnected', (participant) => {
	    console.log("Joining: '" + participant.identity + "'");
	    this.create_participants_list_item(participant);
	  });

	  // When a Participant adds a Track, attach it to the DOM.
	  room.on('trackSubscribed', (track, participant) => {
	    console.log(participant.identity + " added track: " + track.kind);

	    var previewContainer = document.getElementById('remote-media');

	    this.attachTracks([track], previewContainer);
	  });

	  // When a Participant removes a Track, detach it from the DOM.
	  room.on('trackUnsubscribed', (track, participant) => {
	    console.log(participant.identity + " removed track: " + track.kind);
	    this.detachTracks([track]);
	  });

	  // When a Participant leaves the Room, detach its Tracks.
	  room.on('participantDisconnected', (participant) => {
	    console.log("Participant '" + participant.identity + "' left the room");
	    this.delete_participants_list_item(participant);
	    this.detachParticipantTracks(participant);
	  });

	  // Once the LocalParticipant leaves the room, detach the Tracks
	  // of all Participants, including that of the LocalParticipant.
	  room.on('disconnected', () => {
	    console.log('Left');
	    if (this.previewTracks) {
	      this.previewTracks.forEach((track) => {
	        track.stop();
	      });
	      this.previewTracks = null;
	    }
	    this.detachParticipantTracks(room.localParticipant);
	    room.participants.forEach(this.detachParticipantTracks);
	    this.room = null;
	  });


	  // Bind button to leave Room.
	  document.getElementById('button-leave').onclick = () => {
	    console.log('Leaving room...');
	    this.room.disconnect();
	  };
	  return new Promise(function(resolve, reject) {
		    /* missing implementation */
		    resolve(room);
  			}); 
	}

	// Leave Room.
	leaveRoomIfJoined() {
	  if (activeRoom) {
	    this.room.disconnect();
	  }
	}


	join(token){

	// Obtain a token from the server in order to connect to the Room.
	  var connectOptions = {
	    name: 'default',
	    video: {width: 1920, height: 1080,aspectRatio: 1.7777777778},
	    audio: true,
	    logLevel: 'debug'
	  };

	  if (this.previewTracks) {
	    connectOptions.tracks = this.previewTracks;
	  }

	  // Join the Room with the token from the server and the
	  // LocalParticipant's Tracks.
	  return Video.connect(token, connectOptions).then((room) => this.roomJoined(room), function(error) {
	    console.log('Could not connect to Twilio: ' + error.message);
	  });
	 



	}
}

export { ProgrammableVideo }