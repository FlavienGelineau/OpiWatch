const mqtt = require('mqtt');
const random = require('./utils/random');
const generator = require('./utils/generator');
const colors = require('./utils/colors');

const envt = process.env.NODE_ENV || 'development';
const config = require('./config.json')[envt];

const mockFilename = process.argv[3] || 'bidmc_05_Signals.csv';
const broker_uri = process.argv[2]

console.log(mockFilename)
console.log(broker_uri)

var id = random.string(10);
var client  = mqtt.connect(broker_uri);

// Client logs and event handlers
client.on('connect', function () {
  console.log(colors.connected(`Succesfully connected to ${colors.bold(broker_uri)}`));
  console.log(colors.termination(`Data will be published on topic ${colors.bold(id)}`))
})

// Loading data
const data = generator.format(mockFilename)
  .then(data => {
    index = 0;
    setInterval(() => {
      index = (index + 1) % data.length;
      client.publish(id, JSON.stringify({
        "time" : data[index]["time"],
        "avg" : data[index]["AVR"]
      }))
    }, 8);
  })
  .catch( err => {
    console.log(`Error when loading mock data with file ${mockFilename}`);
    return null;
  });