const mqtt = require('mqtt');
const express = require("express");
const mongoose = require('mongoose');
const dbConnection = require('./lib/db');
const mqttConnection = require('./lib/mqtt_client');

const colors = require('./lib/colors');

// const controls = require('./lib/controls');
// const db = require('./lib/db');

const envt = process.env.NODE_ENV || 'developpment';
const config = require('./config')[envt];

/* ===========================================
============= Handle connections =============
=========================================== */

var app = express();

dbConnection(config.db_config);
var client = mqttConnection(config.broker_uri)

/* ===========================================
=================== Routes ===================
=========================================== */

app.get('/register/:id', function(req, res) {
  client.subscribe(req.params.id)
})

/* ===========================================
=============== Launch server  ===============
=========================================== */

var server = app.listen(config.node_port, () => {
  console.log(colors.connected(`Server is listenning on port ${colors.bold(config.node_port)}`))
})

/* ===========================================
============ Process Termination  ============
=========================================== */

process.on('SIGINT', function(){
  client.end(function() {
    console.log(colors.termination("Client connection is closed due to application termination"));
    mongoose.connection.close(function(){
      console.log(colors.termination("Mongoose default connection is disconnected due to application termination"));
      server.close(() => process.exit(0))
    });
  })
});

