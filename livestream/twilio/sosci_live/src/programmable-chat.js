'use strict';

class ProgrammableChat{


    constructor(identity,token){
        this.identity = identity;
        this.token = token;
        // Get handle to the chat div
        this.chat_window = document.getElementById('messages');


        this.create_chat_client();

        
        this.input = document.getElementById('chat-input');



        this.input.addEventListener('keydown', this.key_logger);

        
        // Our interface to the Chat service
        this.chatClient = null;
        // A handle to the "general" chat channel - the one and only channel we
        // will have in this sample app     
        this.generalChannel = null;
        // The server will assign the client a random username - store that value
        // here     
        this.username = null;

        // Alert the user they have been assigned a random username
        this.print('Logging in...');
    }

  // Helper function to print info messages to the chat window
  print(infoMessage, asHtml) {
    var msg = document.createElement("DIV"); 
    msg.setAttribute("class","info");


    if (asHtml) {
      msg.appendChild(infoMessage);
    } else {
      var txt = document.createTextNode(infoMessage);
      msg.appendChild(txt);
    }
    this.chat_window.append(msg);
  }

  // Helper function to print chat message to the chat window
  printMessage(fromUser, message) {
    var user = document.createElement("SPAN"); 
    user.setAttribute("class","username");
    var user_txt = document.createTextNode(fromUser + ':');
    user.appendChild(user_txt);

    if (fromUser === this.username) {
      user.classList.add("me");
    }
    var $message = $('<span class="message">').text(message);

    var msg = document.createElement("SPAN"); 
    msg.setAttribute("class","message");
    var msg_txt = document.createTextNode(message);
    msg.appendChild(msg_txt);


    var container = document.createElement("DIV"); 
    container.setAttribute("class","message-container");

    container.appendChild(user).appendChild(msg);
    this.chat_window.appendChild(container);
    this.chat_window.scrollTop = this.chat_window.scrollHeight;
  }



  // Get an access token for the current user, passing a username (identity)
  // and a device ID - for browser-based apps, we'll always just use the
  // value "browser"
 create_chat_client(){

        // Initialize the Chat client
    Twilio.Chat.Client.create(this.token).then(client => {
      console.log('Created chat client');
      this.chatClient = client;
      this.chatClient.getSubscribedChannels().then(this.createOrJoinGeneralChannel);

    // Alert the user they have been assigned a random username
    this.username = this.identity;
    print('You have been assigned a random username of: '
    + '<span class="me">' + this.username + '</span>', true);

    }).catch(error => {
      console.error(error);
      print('There was an error creating the chat client:<br/>' + error, true);
      print('Please check your .env file.', false);
    });
 }

  createOrJoinGeneralChannel() {
    // Get the general chat channel, which is where all the messages are
    // sent in this simple application
    print('Attempting to join "general" chat channel...');
    this.chatClient.getChannelByUniqueName('general')
    .then(function(channel) {
      this.generalChannel = channel;
      console.log('Found general channel:');
      console.log(this.generalChannel);
      setupChannel();
    }).catch(function() {
      // If it doesn't exist, let's create it
      console.log('Creating general channel');
      this.chatClient.createChannel({
        uniqueName: 'general',
        friendlyName: 'General Chat Channel'
      }).then(function(channel) {
        console.log('Created general channel:');
        console.log(channel);
        this.generalChannel = channel;
        setupChannel();
      }).catch(function(channel) {
        console.log('Channel could not be created:');
        console.log(channel);
      });
    });
  }

  // Set up channel after it has been found
  setupChannel() {
    // Join the general channel
    this.generalChannel.join().then(function(channel) {
      print('Joined channel as '
      + '<span class="me">' + this.username + '</span>.', true);
    });

    // Listen for new messages sent to the channel
    this.generalChannel.on('messageAdded', function(message) {
      printMessage(message.author, message.body);
    });
  }

  // Send a new message to the general channel
  key_logger(e) {

    if (e.keyCode == 13) {
      if (this.generalChannel === undefined) {
        this.print('The Chat Service is not configured. Please check your .env file.', false);
        return;
      }
      this.generalChannel.sendMessage(this.input.val())
      this.input.val('');
    }
   }
}

export { ProgrammableChat }