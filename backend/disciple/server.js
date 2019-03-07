const express = require('express');
const fs = require('fs');
const ip = require('ip');

const envt = process.env.NODE_ENV || 'development';
const config = require('./config.json')[envt];

const random = require('./utils/random');
const generator = require('./utils/generator');

let app = express();

const MAX_HISTORY_LENGTH = 100;
const ID = 'bidmc_05';

const mockFilename = 'bidmc_05_Signals.csv';

let history = []
const data = generator.format(mockFilename)
    .then(data => {
        index = 0;
        setInterval(() => {
            let generated = data[index];
            index = (index + 1) % data.length;
            history.push(generated);
            if(history.length > MAX_HISTORY_LENGTH){
                history.shift();
            }
        }, 8);
    })
    .catch( err => {
        console.log(`Error when loading mock data with file ${mockFilename}`);
        return null;
    })

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
    if(envt == "development") {
        res.header("Access-Control-Allow-Origin", "http://localhost:8081");
    } else {
        res.header("Access-Control-Allow-Origin", "http://localhost:49161");
    }
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

app.listen(config.node_port, async () => {
    console.log(`Server listening on port ${config.node_port}`)
    console.log(`Server local uri : ${ip.address()}:${config.node_port}`)
})