module.exports = {
    developpment : {
        node_port : 8080,
        broker_uri : "mqtt://localhost:1883",
        db_config : {
            database_uri : "mongodb://localhost:27017/asclepios",
            options : {
                useNewUrlParser : true,
                useCreateIndex : true,
                autoReconnect : true,
                reconnectInterval: 500,
                reconnectTries: Number.MAX_VALUE,
                connectTimeoutMS: 10000
            }
        }
    },
    production : {
        node_port : 8080,
        database_uri : "mongodb://mongo:27017/asclepios",
        generator_port : 49160,
        db : {
            useNewUrlParser : true,
            useCreateIndex : true,
            autoReconnect : true,
            reconnectInterval: 500,
            reconnectTries: Number.MAX_VALUE,
            connectTimeoutMS: 10000
        }
    }
}