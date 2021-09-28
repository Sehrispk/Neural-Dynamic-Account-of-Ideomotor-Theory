"""ObjectController controller."""
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

# Main loop:
while object.step(timestep) != -1:
    object.update()
    pass
