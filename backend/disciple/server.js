const mqtt = require('mqtt');
const random = require('./utils/random');
const generator = require('./utils/generator');

const envt = process.env.NODE_ENV || 'development';
const config = require('./config.json')[envt];

const mockFilename = 'bidmc_05_Signals.csv';

var id = random.string(10);
var client  = mqtt.connect(config.broker_uri);

// Client logs and event handlers
client.on('connect', function () {
  console.log(`Succesfully connected to ${config.broker_uri}`);
  console.log(`Data will be published on topic ${id}`)
})

// Loading data
const data = generator.format(mockFilename)
  .then(data => {
      index = 0;
      setInterval(() => {
          index = (index + 1) % data.length;
          client.publish(id, JSON.stringify(data[index]))
      }, 8);
  })
  .catch( err => {
      console.log(`Error when loading mock data with file ${mockFilename}`);
      return null;
  })