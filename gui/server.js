const express = require('express');
const redis = require('redis');
const channel = 'do'
const publisher = redis.createClient({
    host: 'redis',
    port: 6379
});
const app = express();
const port = 8080;

app.get('/', (req, res) => res.send('Hello From Express'));

app.listen(port, () => console.log(`Example app listening on port ${port}!`));

var j={
    "name":"Andrea"
};

function JSONpub(json) {
    /**
     * Receives JSON and publishes it as a string.
     * 
     * This function receives a JSON, then it converts
     * it to a string (to make it compatible with redis pubsub)
     * (pubsub: Publish: Send message, Subscribe: Enters a 
     * channel to receive messages)
     * and finally it publishes it (as a string) to redis' channel
     * (where channel is a constant with the channel as value).
     * 
     */
    json_string = JSON.stringify(json)
    publisher.publish(channel, json_string);
    console.log("JSON sent!")
}

function stateChange(newState) {
    /**
     * Waits 5 seconds before sending JSON
     * 
     * This function is only temporary, it 
     */
    setTimeout(function () {
        if (newState == -1) {
            console.log("Printing stuff")
            JSONpub(j);
        }
    }, 5000);
}

stateChange(-1)

