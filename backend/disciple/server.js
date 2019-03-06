const express = require('express');
const envt = process.env.NODE_ENV || 'development';
const config = require('./config.json')[envt];
const fs = require('fs');
const cron = require('node-cron');
const ip = require('ip');

const random = require('./utils/random');

let app = express();

const MIN_RAND = 0;
const MAX_RAND = 100;
const MAX_HISTORY_LENGTH = 100
const ID = random.string(10);

let history = []

/* ========================================
Cron jobs for generating data every second
The generated data is appened to the file logs/history.txt
======================================== */
// cron.schedule('0-59 * * * * *', () => {
//     let generated = random.number(MIN_RAND, MAX_RAND);
//     // fs.appendFile('./logs/history.txt', generated.toString() + '\n', (err) => {
//     //     if (err) throw err;
//     //     console.log(`The data ${generated} was appened to history file`);
//     // });
//     history.push(generated);
//     if(history.length > MAX_HISTORY_LENGTH){
//         history.shift();
//     }
// })

setInterval(() => {
    let generated = random.number(MIN_RAND, MAX_RAND);
    history.push(generated);
    if(history.length > MAX_HISTORY_LENGTH){
        history.shift();
    }
}, 1000)

/* ========================================
Sending the current history to the requester
======================================== */
app.get('/history', function(req, res) {
    // This road returns the last MAX_HISTORY_LENGTH generated values
    // fs.readFile('./logs/history.txt', (err, data) => {
    //     if(!err) {
    //         res.status(200);
    //         res.contentType("text/plain");
    //         res.send(data);
    //     } else {
    //         res.status(500);
    //         res.contentType("text/plain");
    //         res.send("Internal server error");
    //         throw err;
    //     }
    // })
    res.header("Access-Control-Allow-Origin", "http://localhost:49161");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.status(200);
    res.contentType("text/plain");
    res.send(JSON.stringify({"data" : history, "name" : ID}));
})

/* ========================================
Cleaning every data stored in history.txt
======================================== */
app.get('/clear', function(req, res) {
    fs.writeFile('./logs/history.txt', '', err => {
        if(!err) {
            res.status(200);
            res.contentType("text/plain");
            res.send("succesfully cleaned history");
        } else {
            res.status(500);
            res.contentType("text/plain");
            res.send("Internal server error");
            throw err;
        }
    })
})

app.listen(config.node_port, () => {
    // clean history when launching new instance
    console.log("Cleaning history...")
    fs.writeFile('./logs/history.txt', '', err => {
        if(!err) {
            console.log("Succesfully cleaned history");
        } else {
            throw err;
        }
    })
    console.log(`Server listening on port ${config.node_port}`)
    console.log(`Server local uri : ${ip.address()}:${config.node_port}`)
})