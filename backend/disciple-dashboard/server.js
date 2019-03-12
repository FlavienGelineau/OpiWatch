const express = require('express');
const opn = require('opn');
const envt = process.env.NODE_ENV || 'development';
const config = require('./config.json')[envt];


let app = express();


app.set('view engine', 'ejs');
app.use('/public', express.static('./public'));
app.use('/rickshaw', express.static('./node_modules/rickshaw'));

app.get('/dashboard', function(req, res) {
  res.status(200);
  res.render('dashboard.ejs');
})

app.listen(config.node_port, () => {
  console.log(`Server listening on port ${config.node_port}`)
  if(envt === "production"){
    opn(`http://localhost:${config.node_port}/dashboard`);
  }
})