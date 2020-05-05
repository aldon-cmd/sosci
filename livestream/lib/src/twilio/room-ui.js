'use strict';

class RoomUI {

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

export { RoomUI }