const loader = require('./load');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '../public')

const format = async (filename) => {
  return new Promise(async (resolve, reject) => {
    try {
      let data = await loader.load(path.join(PUBLIC_DIR, filename));
      for(let i=0; i<data.length; i++){
        for (var key in data[i]) {
          if (data[i].hasOwnProperty(key)) {
              data[i][key] = parseFloat(data[i][key]);
          }
        }
      }
      resolve(data)
    } catch(err) {
      reject(err)
    }
  })
}

module.exports = {
    format : format
}