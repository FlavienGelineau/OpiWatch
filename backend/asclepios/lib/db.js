const mongoose = require('mongoose');
const colors = require('./colors');

module.exports = config => {
  const url = config.database_uri;
  mongoose.connect(url, config.options);

  mongoose.connection.on('connected', function(){
    console.log(colors.connected("Mongoose default connection is open to ", colors.bold(url)));
  });

  mongoose.connection.on('error', function(err){
    console.log(colors.error("Mongoose default connection has occured "+colors.bold(err)+" error"));
  });

  mongoose.connection.on('disconnected', function(){
    console.log(colors.disconnected("Mongoose default connection is disconnected"));
  });
}