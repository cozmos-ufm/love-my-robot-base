import cozmo, time
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import blue_light, Color, green_light, Light, red_light, white_light, off_light
from cozmo.util import degrees, distance_mm, radians, speed_mmps
def cozmo_program(robot: cozmo.robot.Robot):
    robot.say_text('Hello').wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabYes).wait_for_completed()
    robot.play_audio(cozmo.audio.AudioEvents.SfxGameWin)
    time.sleep(1.0)
    robot.drive_off_charger_contacts().wait_for_completed()
    robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
    robot.move_lift(-3)
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.set_head_angle(degrees(0)).wait_for_completed()
    time.sleep(0.5)
    robot.drive_straight(distance_mm(-60), speed_mmps(50)).wait_for_completed()

    robot.drive_straight(distance_mm(150.0), speed_mmps(50.0)).wait_for_completed()
    robot.turn_in_place(degrees(360)).wait_for_completed()
    robot.move_lift(1)
    for i in range(10):
        robot.set_all_backpack_lights(cozmo.lights.red_light)
        time.sleep(0.1)
        robot.set_all_backpack_lights(cozmo.lights.green_light)
        time.sleep(0.1)
        robot.set_all_backpack_lights(cozmo.lights.blue_light)
        time.sleep(0.1)
        robot.set_center_backpack_lights(cozmo.lights.white_light)
        time.sleep(0.1)
        robot.set_all_backpack_lights(cozmo.lights.off_light)
        time.sleep(0.1)

    robot.set_all_backpack_lights(cozmo.lights.blue_light)
    time.sleep(1)
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabWin).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHiccup).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSurprise).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabExcited).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSneeze).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabScaredCozmo).wait_for_completed()

    cube1 = robot.world.get_light_cube(LightCube1Id)
    if cube1 is not None:
        cube1.set_lights(cozmo.lights.red_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")
        time.sleep(10)

    
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    targ = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()
    robot.pickup_object(targ[0], num_retries=5).wait_for_completed()

cozmo.run_program(cozmo_program)
