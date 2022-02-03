"""ObjectController controller."""
from Object import Object
import sys, ast

# create the Robot instance.
color = ast.literal_eval(sys.argv[1])
contingencies = ast.literal_eval(sys.argv[2])
rewardDelay = ast.literal_eval(sys.argv[3])
rewardRate = ast.literal_eval(sys.argv[4])
object = Object(color, contingencies, rewardDelay, rewardRate)

# get the time step of the current world.
timestep = int(object.getBasicTimeStep())
object.set_color([int(color['R']), int(color['G']), int(color['B'])], 1.)

# Main loop:
while object.step(timestep) != -1:
    object.update()
    pass
