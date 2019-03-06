const express = require("express");
const mongoose = require('mongoose')

const envt = process.env.NODE_ENV || 'developpment';
const config = require('./config.json')[envt];

const controls = require('./lib/controls');
const db = require('./lib/db');

let app = express();

app.get('/register', async function(req, res) {
    try {
        let registered = await controls.register("192.168.50.100:49160");
        res.status(200);
        res.send({ result : registered });
    } catch(error) {
        res.status(500);
        res.send({ error })
    }
})

app.get('/unregister/:name', async function(req, res) {
    try {
        let result = await controls.unregister(req.params.name);
        res.status(200);
        res.send(result);
    } catch(error) {
        res.status(500);
        res.send({ error });
    }
})

app.get('/patient/:name', async function(req, res) {
    try {
        let patient = await controls.find(req.params.name);
        res.status(200);
        res.send(patient);
    } catch(error) {
        console.log(error)
        res.status(500);
        res.send({ error });
    }
})

setInterval(async () => {
    try {
        let patients = await controls.findAll();
        for(let i=0; i<patients.length; i++){
            let result = await controls.updateFromGenerator(patients[i].name);
        }
    } catch(err) {
        console.log("Error occured in cron")
    }
}, 200)

const start = () => {
    app.listen(config.node_port, () => {
        console.log("Server running on port ", config.node_port);
    });
}

mongoose.connect(config.database_uri, db.config)
    .then(() => {
        console.log(`Succesfully connected to database at uri ${config.database_uri}`);
        start();
    })
    .catch((err) => {
        console.log(err);
        console.log(`Could not reach database at uri ${config.database_uri}`);
    });