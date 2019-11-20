from flask import Flask
import redis, json, threading, time, asyncio

app = Flask(__name__)
r = redis.StrictRedis(host="localhost", port=6379, db=0)
#cmmnt here
p = r.pubsub(ignore_subscribe_messages=True)


channel = 'do'

global_json = None

@app.route("/")
def index():
    return "Hello from Flask!"


def message_handler(message):
    """Converts message string to JSON.

    Once invoked through asyncSUB() it handles
    the message by converting it from string
    to JSON and assigns it to 'global_json'
    """
    print(f"MY HANDLER: '{message.get('data')}")
    json_message = None
    message_data = message.get('data')

    if message_data:
        json_message = json.loads(message_data) # converts to JSON type
        _testPrint(json_message)
        global_json = json_message
        

def _testPrint(JSON):
    """Temporary func. CHANGE LATER

    As the underscore implies, this is just
    a temporary function. Its purpose is to
    prove that 'message_handler()' is able to
    process the JSON and send it to any custom
    method. That custom mentioned for now is 
    '_testPrint(JSON)' for now, however it NEEDS
    to be changed to a function that parses the JSON
    and understands code from it; this is not yet 
    implemented.
    """
    print(f"\nCUSTOM: {JSON}")

def asyncSUB():
    """Subscribes to channel and sends message 
    to handler.

    When in need of reading messages this is the 
    function to call. Once called it will subscribe 
    asynchronously to channel (where channel = 'CHANNEL_NAME' 
    defined on the first lines of this file).

    p.run_in_thread(): Behind the scenes, this is
    simply a wrapper around get_message() that runs 
    in a separate thread, and use asyncio.run_coroutine_threadsafe() 
    to run coroutines.

    Coroutine: Coroutines are generalization of subroutines. 
    They are used for cooperative multitasking where a process 
    voluntarily yields (give away) control periodically or when 
    idle in order to enable multiple applications to be run 
    simultaneously.
    """
    p.subscribe(**{channel: message_handler})
    thread = p.run_in_thread(sleep_time=0.1, daemon=True)
    message = p.get_message()
    print(f"asyncSUB: message: {message}")



if __name__ == "__main__":
    """We start asyncSUB() and Flask.

    We call the main function 'asyncSUB()' to subscribe asynchronously to 
    the channel; 
    this is were the fun begins.
    """
    asyncSUB()
    app.run(host="0.0.0.0")
    
    




