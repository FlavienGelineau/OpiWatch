const express = require("express");
const bodyParser = require('body-parser')

let app = express();
let port = parseInt(process.env.PORT, 10) || 8080;

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }))

// parse text
app.use(bodyParser.text())

// parse application/json
app.use(bodyParser.json())

app.post("/test", (req, res, next) => {
    console.log(req.body)
    res.status(200).send()
})

app.listen(port, () => {
    console.log("Server running on port ", port);
});