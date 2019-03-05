const express = require("express");
const bodyParser = require('body-parser');
const cron = require('node-cron');

const envt = process.env.NODE_ENV || 'developpment';
const config = require('./config.json')[envt];

const controls = require('./lib/controls');

let app = express();

app.get('/register', async function(req, res) {
    try {
        let registered = await controls.registerPatient("192.168.50.100:8080");
        res.status(200);
        res.send({ result : registered});
    } catch(error) {
        res.status(500);
        res.send({ error })
    }
})

app.get('/patient/:name', async function(req, res) {
    try {
        let patient = await controls.find(req.params.name);
        res.status(200);
        res.send(patient);
    } catch(error) {
        res.status(500);
        res.send({ error });
    }
})

cron.schedule('0-59 * * * * *', async () => {
    try {
        let patients = await controls.findAll();
        for(let i=0; i<patients.length; i++){
            let result = await controls.updateFromGenerator(patients[i].name);
        }
    } catch(err) {
        console.log(err)
    }
})

app.listen(config.node_port, () => {
    console.log("Server running on port ", config.node_port);
});