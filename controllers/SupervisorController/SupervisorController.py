"""SupervisorController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Supervisor
# create the Robot instance.
#robot = Robot()

# get the time step of the current world.
#timestep = int(robot.getBasicTimeStep())
supervisor = Supervisor()
children = supervisor.getRoot().getField('children')

position = '0.16 0.05 -0.34'
name = "\"box1\""
controllerArgs = '["255", "0", "0", "contingency 1"]'
args = 'translation {}, name {}, controllerArgs {}'.format(position, name, controllerArgs)
RobotString1 = 'ColoredBoxRobot {{{}}}'.format(args)
children.importMFNodeFromString(-1, RobotString1)

position = '0.1 0.05 -0.34'
name = "\"box2\""
controllerArgs = '["0", "255", "0", "contingency 1"]'
args = 'translation {}, name {}, controllerArgs {}'.format(position, name, controllerArgs)
RobotString2 = 'ColoredBoxRobot {{{}}}'.format(args)
children.importMFNodeFromString(-1, RobotString2)
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
