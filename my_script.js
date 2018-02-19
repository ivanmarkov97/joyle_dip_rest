var websocket = new WebSocket("ws://127.0.0.1:8888/websocket");

document.forms.publish.onsubmit = function() {
  var outgoingMessage = this.message.value;
  msg = {
  	id: 123231412,
  	type: "message",
    text: this.message.value,
    name: this.person.value,
    date: Date.now()
  };
  websocket.send(JSON.stringify(msg));
  return false;
};

websocket.onopen = function() {
	alert("Connection opened");
};

websocket.onclose = function() {
	alert("Connection closed");
};

websocket.onmessage = function(event) {
	var incomingMessage = event.data;
  	showMessage(incomingMessage);
};

websocket.onerror = function(error) {
	alert("Error " + error.message);
};

function showMessage(message) {
  var messageElem = document.createElement('div');
  messageElem.appendChild(document.createTextNode(message));
  document.getElementById('subscribe').appendChild(messageElem);
}
