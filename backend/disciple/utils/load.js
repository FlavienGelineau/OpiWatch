const csv = require('csvtojson');

module.exports = {
    load : (path) => {
        return new Promise((resolve, reject) => {
            try {
                csv().fromFile(path)
                .then(jsonObj => {
                    resolve(jsonObj);
                })
            } catch(err) {
                reject(err);
            }
        })
    }
}