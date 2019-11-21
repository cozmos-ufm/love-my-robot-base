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

let code = ['SAY HI', 'SAY HELLO']

app.get('/', (req, res) => res.sendFile('index.html', {code}))
app.get('/pug', (req, res) => res.render('pugIndex', {code}))
app.get('/cozmo', (req, res) => res.render('cozmo', {code}))

app.get('/send', (req, res) => {
    var dateobj = new Date(Date.now()); 
  
    // Contents of above date object is converted 
    // into a string using toISOString() function. 
    var date = dateobj.toISOString(); 
    console.log(date)
    var js ={
        "request_timestamp":date,
        "lmr":code
    } 
    JSONpub(js)
})

app.get('/clear', (req, res) => {
    code = []
    res.json({message:"Cleared"})
})

app.post('/save-code', function(req, res) {
    console.log(req.body);
    code.push(req.body.name);
    res.json({message:"New code added"})
})
app.post('/delete-code', function(req, res) {
    console.log(req.body);
    let found = 0
    for( var i = 0; i < code.length; i++){ 
        if ( i == req.body.id) {
          code.splice(i, 1)
          found = 1
        }
     }
    // names.delete(req.body.name);
    if(found == 1){
        res.json({message:"Code deleted"})
    }
    res.json({message:"Code not found"})
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

