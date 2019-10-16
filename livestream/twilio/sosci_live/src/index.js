'use strict';

var Video = require('twilio-video');

var activeRoom;
var previewTracks;
var roomName;

// Attach the Tracks to the DOM.
function attachTracks(tracks, container) {
  tracks.forEach(function(track) {
    container.appendChild(track.attach());
  });
}

// Attach the Participant's Tracks to the DOM.
function attachParticipantTracks(participant, container) {
  var tracks = Array.from(participant.tracks.values());
  attachTracks(tracks, container);
}

// Detach the Tracks from the DOM.
function detachTracks(tracks) {
  tracks.forEach(function(track) {
    track.detach().forEach(function(detachedElement) {
      detachedElement.remove();
    });
  });
}

// Detach the Participant's Tracks from the DOM.
function detachParticipantTracks(participant) {
  var tracks = Array.from(participant.tracks.values());
  detachTracks(tracks);
}

function create_local_tracks() {
  var localTracksPromise = previewTracks
    ? Promise.resolve(previewTracks)
    : Video.createLocalTracks();

  localTracksPromise.then(function(tracks) {
    window.previewTracks = previewTracks = tracks;
    var previewContainer = document.getElementById('local-media');
    if (!previewContainer.querySelector('video')) {
      attachTracks(tracks, previewContainer);
    }
  }, function(error) {
    console.error('Unable to access local media', error);
    console.log('Unable to access Camera and Microphone');
  });
}


function share_screen(){
  var stream = navigator.mediaDevices.getDisplayMedia().then(stream => {
  var screenTrack = stream.getVideoTracks()[0];
  var trackName = window.room.localParticipant.identity +'-screen-share'
  var videoTrack = Video.LocalVideoTrack(screenTrack,{name: trackName});
  window.room.localParticipant.publishTrack(videoTrack);
  }); 
}

function create_participants_list_item(participant){
    var participants_list = document.getElementById('participants');
    var participants_list_item = document.createElement("LI"); 
    var participants_list_item_content;
    var participant_identity;
    var paricipant_full_name;

    participants_list_item.setAttribute("id",participant.SID);

    participant_identity = participant.identity.split("/");

    paricipant_full_name = 1 in participant_identity ? participant_identity[1] : "";

    participants_list_item_content = '<div class="participant">'+ paricipant_full_name +'</div><i class="fas fa-circle"></i>';

    participants_list_item.innerHTML = participants_list_item_content;

    participants_list.appendChild(participants_list_item);     
}

function delete_participants_list_item(participant){
  var participants_list_item = document.getElementById(participant.SID);
  participants_list_item.parentNode.removeChild(elem);
}

function populate_participant_list(room){


     room.participants.forEach(function(participant) {

      create_participants_list_item(participant);
    });
}

// Successfully connected!
function roomJoined(room) {
  window.room = activeRoom = room;

  console.log("Joined Room");

  populate_participant_list(room);

  // create_local_tracks();


  // Attach LocalParticipant's Tracks, if not already attached.
  var previewContainer = document.getElementById('local-media');
  if (!previewContainer.querySelector('video')) {
    attachParticipantTracks(room.localParticipant, previewContainer);
  }

  // Attach the Tracks of the Room's Participants.
  room.participants.forEach(function(participant) {
    console.log("Already in Room: '" + participant.identity + "'");
    var previewContainer = document.getElementById('remote-media');
    attachParticipantTracks(participant, previewContainer);
  });

  // When a Participant joins the Room, log the event.
  room.on('participantConnected', function(participant) {
    console.log("Joining: '" + participant.identity + "'");
    create_participants_list_item(participant);
  });

  // When a Participant adds a Track, attach it to the DOM.
  room.on('trackSubscribed', function(track, participant) {
    console.log(participant.identity + " added track: " + track.kind);
    var previewContainer = document.getElementById('remote-media');
    attachTracks([track], previewContainer);
  });

  // When a Participant removes a Track, detach it from the DOM.
  room.on('trackUnsubscribed', function(track, participant) {
    console.log(participant.identity + " removed track: " + track.kind);
    detachTracks([track]);
  });

  // When a Participant leaves the Room, detach its Tracks.
  room.on('participantDisconnected', function(participant) {
    console.log("Participant '" + participant.identity + "' left the room");
    delete_participants_list_item(participant);
    detachParticipantTracks(participant);
  });

  // Once the LocalParticipant leaves the room, detach the Tracks
  // of all Participants, including that of the LocalParticipant.
  room.on('disconnected', function() {
    console.log('Left');
    if (previewTracks) {
      previewTracks.forEach(function(track) {
        track.stop();
      });
      previewTracks = null;
    }
    detachParticipantTracks(room.localParticipant);
    room.participants.forEach(detachParticipantTracks);
    activeRoom = null;
  });
}

// Leave Room.
function leaveRoomIfJoined() {
  if (activeRoom) {
    activeRoom.disconnect();
  }
}


function join(token){

// Obtain a token from the server in order to connect to the Room.
  var connectOptions = {
    name: 'default',
    video: {width: 1920, height: 1080,aspectRatio: 1.7777777778},
    audio: true,
    logLevel: 'debug'
  };

  if (previewTracks) {
    connectOptions.tracks = previewTracks;
  }

  // Join the Room with the token from the server and the
  // LocalParticipant's Tracks.
  Video.connect(token, connectOptions).then(roomJoined, function(error) {
    console.log('Could not connect to Twilio: ' + error.message);
  });
 

  // Bind button to leave Room.
  document.getElementById('button-leave').onclick = function() {
    console.log('Leaving room...');
    activeRoom.disconnect();
  };

}


// When we are about to transition away from this page, disconnect
// from the room, if joined.
window.addEventListener('beforeunload', leaveRoomIfJoined);

document.getElementById('btn-share-screen').onclick = share_screen;

module.exports = {join: join};