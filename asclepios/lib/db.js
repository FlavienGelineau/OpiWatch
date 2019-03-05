var mongoose = require('mongoose');

const envt = process.env.NODE_ENV || 'developpment';
const config = require('../config.json')[envt];


mongoose.connect(config.database_uri, { useNewUrlParser : true, useCreateIndex : true });
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log(`Succesfully connected to database at uri ${config.database_uri}`)
});

let patientSchema = new mongoose.Schema({
    name : {
        type : String,
        required : true,
        unique : true,
        index : true,
    },
    local_uri : {
        type : String,
        required : true
    },
    history : {
        type : Array,
        default : []
    }
})

let Patient = mongoose.model('Patient', patientSchema);

module.exports = {
    connection : db,
    models : {
        patient : Patient
    }
}