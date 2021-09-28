"""SupervisorController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
import json
from controller import Robot
from controller import Supervisor
# create the Robot instance.
#robot = Robot()

# get the time step of the current world.
supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())
children = supervisor.getRoot().getField('children')

f = open('../../worlds/world-config.json')
config = json.load(f)

for robot in config['Robots']:
    controllerArgs = '['
    args = ''
    for key,value in robot['controllerArgs'].items():
        controllerArgs += '\"{}\", '.format(value)
    controllerArgs += ']'
    for key,value in robot.items():
        if key != 'controllerArgs' and key != 'type':
            args += key + ' ' + value + ', '
    args += 'controllerArgs ' + str(controllerArgs)
    
    robotString = '{0} {{{1}}}'.format(robot['type'], args)
    children.importMFNodeFromString(-1, robotString)
    
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
#while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    #pass

# Enter here exit cleanup code.
