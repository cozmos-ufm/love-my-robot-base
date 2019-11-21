const express = require('express');
const redis = require('redis');
const pug = require('pug');
var bodyParser = require('body-parser');
const app = express();
const port = 8080
const channel = 'do'
const publisher = redis.createClient({
    host: 'redis',
    port: 6379
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));

var j={
    "name":"Andrea"
};

var _code={
    "request_timestamp":"2019-08-11T12:99",
    "lmr":["SAY NICE"]
}

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
            JSONpub(_code);
        }
    }, 5000);
}

stateChange(-1)

app.set('view engine', 'pug')
app.use(express.static('public'))

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

let names = ['SAY HI', 'SAY HELLO']

app.get('/', (req, res) => res.sendFile('index.html', {names}))
app.get('/pug', (req, res) => res.render('pugIndex', {names}))
app.get('/c', (req, res) => res.render('cozmo', {names}))

app.get('/send', (req, res) => {
    var js ={
        "request_timestamp":"2019-08-11T12:99",
        "lmr":names
    } 
    JSONpub(js)
})

app.post('/save-user', function(req, res) {
    console.log(req.body);
    names.push(req.body.name);
    res.json({message:"New name added"})
})
app.post('/delete-user', function(req, res) {
    console.log(req.body);
    let found = 0
    for( var i = 0; i < names.length; i++){ 
        if ( names[i] === req.body.name) {
          names.splice(i, 1); 
          found = 1
        }
     }
    // names.delete(req.body.name);
    if(found == 1){
        res.json({message:"User deleted"})
    }
    res.json({message:"User not found"})
})

