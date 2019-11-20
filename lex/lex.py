import asyncio
import sys
import cozmo
import time
from flask import Flask
import redis, json, threading, time, asyncio

from cozmo.lights import blue_light, Color, green_light, Light, red_light, white_light, off_light
from cozmo.util import degrees, distance_mm, radians, speed_mmps

app = Flask(__name__)
r = redis.StrictRedis(host="localhost", port=6379, db=0)
#cmmnt here
p = r.pubsub(ignore_subscribe_messages=True)
channel = 'do'
global_json = None

#Cozmo functions
async def sayhello(robot: cozmo.robot.Robot):
    async with robot.perform_off_charger():
        action = robot.say_text("Hello World")
        await action.wait_for_completed()

def move(robot: cozmo.robot.Robot):
    # Drive forwards for 150 millimeters at 50 millimeters-per-second.
    robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()

def moveback(robot: cozmo.robot.Robot):
    # Drive backwards for 150 millimeters at 50 millimeters-per-second.
    robot.drive_straight(distance_mm(-150), speed_mmps(50)).wait_for_completed()

def turn(robot: cozmo.robot.Robot):
    # Turn 90 degrees to the left.
    # Note: To turn to the right, just use a negative number.
    robot.turn_in_place(degrees(90)).wait_for_completed()

def lift(robot: cozmo.robot.Robot):
    # Tell the head motor to start lowering the head (at 5 radians per second)
    #robot.move_head(-5)
    # Tell the lift motor to start lowering the lift (at 5 radians per second)
    robot.move_lift(-5)
    # Tell Cozmo to drive the left wheel at 25 mmps (millimeters per second),
    # and the right wheel at 50 mmps (so Cozmo will drive Forwards while also
    # turning to the left
    #robot.drive_wheels(25, 50)

#Animations
def celebration(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabWin).wait_for_completed()  

#Animals
def duck(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabDuck).wait_for_completed()    

def frog(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabDuck).wait_for_completed()  

@app.route("/e")

def index():
    return "Hello from Python!"

@app.route('/')
def hello_world():
    cozmo.run_program(happy)

    return 'Hello, World!'


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
    
    




