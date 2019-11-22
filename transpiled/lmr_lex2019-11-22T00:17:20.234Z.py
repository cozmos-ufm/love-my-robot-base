import cozmo, time
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import blue_light, Color, green_light, Light, red_light, white_light, off_light
from cozmo.util import degrees, distance_mm, radians, speed_mmps
def cozmo_program(robot: cozmo.robot.Robot):
    robot.play_audio(cozmo.audio.AudioEvents.SfxGameWin)
    time.sleep(1.0)
cozmo.run_program(cozmo_program)
