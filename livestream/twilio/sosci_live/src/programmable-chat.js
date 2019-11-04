'use strict';
import {Client} from 'twilio-chat';

class ProgrammableChat{


    constructor(identity,token){
        this.identity_arr = identity.split("/");
        this.identity = 1 in this.identity_arr ? this.identity_arr[1] : "";
        
        this.token = token;

        // Our interface to the Chat service
        this.chatClient = null;
        // A handle to the "general" chat channel - the one and only channel we
        // will have in this sample app     
        this.generalChannel = null;
        // The server will assign the client a random username - store that value
        // here     
        this.username = null;

        // Get handle to the chat div
        this.chat_panel = document.getElementById('chat-panel');

        this.input = document.getElementById('chat-input');



        this.input.addEventListener('keydown', (e) => this.key_logger(e));

        // Alert the user they have been assigned a random username
        this.print('Logging in...');




        this.create_chat_client();

        


        

    }

  // Helper function to print info messages to the chat window
  print(infoMessage, asHtml) {
    var msg = document.createElement("DIV"); 
    msg.setAttribute("class","info");
    var infoMessage_txt = document.createTextNode(infoMessage);

    if (asHtml) {
      msg.appendChild(infoMessage_txt);
    } else {
      
      msg.appendChild(infoMessage_txt);
    }
    this.chat_panel.appendChild(msg);
  }

  // Helper function to print chat message to the chat window
  printMessage(fromUser, message) {
    var message_container = document.createElement("DIV"); 
    message_container.setAttribute("class","live-chat");

    //avoid xss with textContent
    var message_txt = document.createTextNode(message);
    var message_span = document.createElement("SPAN");
    message_span.appendChild(message_txt);



    var chat_list_item = '<div class="">'+
                '<span class="chat-badge">'+
                  '<i class="fas fa-user-circle"></i>'+
                '</span>'+
                '<span class="chat-line-username">'+
                  '<span>'+this.identity+'<span>:</span></span>'+
                '</span>'+
                '<span>'+
                  '<span>'+message_span.textContent+'</span>'+
                '</span>'+
             '</div>';
    message_container.innerHTML = chat_list_item;


    this.chat_panel.appendChild(message_container);
    // this.chat_panel.scrollTop = this.chat_panel.scrollHeight;
  }



  // Get an access token for the current user, passing a username (identity)
  // and a device ID - for browser-based apps, we'll always just use the
  // value "browser"
 create_chat_client(){

        // Initialize the Chat client
    Client.create(this.token).then(client => {
      console.log('Created chat client');
      this.chatClient = client;
      this.chatClient.getSubscribedChannels().then(() => this.createOrJoinGeneralChannel());

    // Alert the user they have been assigned a random username
    this.username = this.identity;
    this.print('You have been assigned the username: '
    + this.username, true);

    }).catch(error => {
      console.error(error);
      this.print('There was an error creating the chat client:<br/>' + error, true);
      this.print('Please check your .env file.', false);
    });
 }

  getChannelByUniqueNamelHandler(channel){
      this.generalChannel = channel;
      console.log('Found general channel:');
      console.log(this.generalChannel);
      this.setupChannel(channel);
  }

  createChannelCatch(channel){

        console.log('Channel could not be created:');
        console.log(channel);
  }

  createChannel(channel) {
        console.log('Created general channel:');
        console.log(channel);
        this.generalChannel = channel;
        this.setupChannel(channel);
      }

  getChannelByUniqueNamelHandlerCatch() {
      // If it doesn't exist, let's create it
      console.log('Creating general channel');
      this.chatClient.createChannel({
        uniqueName: 'general',
        friendlyName: 'General Chat Channel'
      }).then((channel) => this.createChannel(channel)).catch((channel) => this.createChannelCatch(channel));
    }

  createOrJoinGeneralChannel() {
    // Get the general chat channel, which is where all the messages are
    // sent in this simple application
    this.print('Attempting to join "general" chat channel...');
    this.chatClient.getChannelByUniqueName('general')
    .then((channel) => this.getChannelByUniqueNamelHandler(channel)).catch(
      () => this.getChannelByUniqueNamelHandlerCatch()
      );
  }

joinedChannel(channel){
      this.print('Joined channel as '+this.username , true);
}
  // Set up channel after it has been found
  setupChannel(channel) {
    // Join the general channel
    if(channel.state.status !== "joined"){
      this.generalChannel.join().then((channel) => this.joinedChannel(channel));
    }else{
      this.joinedChannel(channel);
    }
    

    // Listen for new messages sent to the channel
    this.generalChannel.on('messageAdded', (message) =>
      this.printMessage(message.author, message.body)
    );
  }

  // Send a new message to the general channel
  key_logger(e) {

    if (e.keyCode == 13) {
      if (this.generalChannel === undefined) {
        this.print('The Chat Service is not configured. Please check your .env file.', false);
        return;
      }
      this.generalChannel.sendMessage(this.input.value)
      this.input.value = '';
    }
   }
}

export { ProgrammableChat }