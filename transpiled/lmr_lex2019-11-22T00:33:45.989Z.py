import cozmo, time
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import blue_light, Color, green_light, Light, red_light, white_light, off_light
from cozmo.util import degrees, distance_mm, radians, speed_mmps
def cozmo_program(robot: cozmo.robot.Robot):

    cube1 = robot.world.get_light_cube(LightCube1Id)
    if cube1 is not None:
        cube1.set_lights(cozmo.lights.red_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube1Id cube - check the battery.")
        time.sleep(10)

    

    cube2 = robot.world.get_light_cube(LightCube2Id)
    if cube2 is not None:
        cube2.set_lights(cozmo.lights.green_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube2Id cube - check the battery.")
        time.sleep(10)

    

    cube3 = robot.world.get_light_cube(LightCube3Id)
    if cube3 is not None:
        cube3.set_lights(cozmo.lights.blue_light)
    else:
        cozmo.logger.warning("Cozmo is not connected to a LightCube3Id cube - check the battery.")
        time.sleep(10)

    
    robot.move_lift(1)
    if targ[0]:
        robot.place_object_on_ground_here(targ[0]).wait_for_completed()
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    targ = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()
    robot.pickup_object(targ[0], num_retries=5).wait_for_completed()

    if targ[0]:
        robot.place_object_on_ground_here(targ[0]).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabDuck).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabElephant).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSheep).wait_for_completed()
cozmo.run_program(cozmo_program)
