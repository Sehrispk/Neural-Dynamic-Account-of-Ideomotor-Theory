"""ObjectController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from Object import Object
import sys
import json
# create the Robot instance.
f = open('../../worlds/world-config.json')
config = json.load(f)
object = Object(config['Contingencies'][sys.argv[4]])

# get the time step of the current world.
timestep = int(object.getBasicTimeStep())
object.set_color([int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])], 1.)
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while object.step(timestep) != -1:
    object.update()
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
