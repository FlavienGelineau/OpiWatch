/*

The functions of this file are used to retrieve data from the different
generators, and to store them into the mongo database.

*/
const axios = require('axios');
const db = require('./db');

let controls = {};

// Register a patient from the uri of it's generator
// No data is saved at this point
controls.registerPatient = async (uri) => {
    return new Promise(async (resolve, reject) => {
        try {
            let res = await axios.get('http://' + uri+'/history')
                .then(result => result.data)
                .catch(err => {reject(err)});
            delete res.data;
            res.local_uri = 'http://' + uri+'/history';
            let patient = new db.models.patient(res);
            let result = await patient.save();
            resolve(result);
        } catch(err) {
            reject(err);
        }
    })
}

// Update data of a patient from it's generator
controls.updateFromGenerator = async (name) => {
    return new Promise(async (resolve, reject) => {
        try {
            let patient = await db.models.patient.findOne({name : name});
            let res = await axios.get(patient.local_uri)
                .then(result => result.data)
                .catch(err => {reject(err)});
            patient.history = res.data;
            let result = await patient.save();
            resolve(result)
        } catch(err) {
            reject(err)
        }
    })
}

controls.findAll = () => {
    return new Promise(async (resolve, reject) => {
        try {
            let results = await db.models.patient.find({});
            resolve(results);
        } catch(err) {
            reject(err);
        }
    });
}

controls.find = (name) => {
    return new Promise(async (resolve, reject) => {
        try {
            let result = await db.models.patient.findOne({name : name});
            delete result._id
            delete result.local_id
            resolve(result);
        } catch(err) {
            reject(err);
        }
    })
}

module.exports = controls;