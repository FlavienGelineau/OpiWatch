var mongoose = require('mongoose');

const envt = process.env.NODE_ENV || 'developpment';
const config = require('../config.json')[envt];

const mongoConfig = { 
    useNewUrlParser : true,
    useCreateIndex : true,
    autoReconnect : true,
    reconnectTries: Number.MAX_VALUE,
    reconnectInterval: 500,
    connectTimeoutMS: 10000,
}

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
    config : mongoConfig,
    models : {
        patient : Patient
    }
}