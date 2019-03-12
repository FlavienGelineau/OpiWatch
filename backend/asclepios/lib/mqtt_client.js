const mqtt = require('mqtt');
const colors = require('./colors');

/* ===========================================
==================== MQTT ====================
=========================================== */

module.exports = uri => {
  let client = mqtt.connect(uri);

  // Client logs and event handlers
  client.on('connect', function () {
    console.log(colors.connected(`Succesfully connected to ${colors.bold(uri)}`));
  });
  
  client.on('message', function(topic, message) {
    let data = JSON.parse(message.toString());
    console.log(data)
  });

  return client
}