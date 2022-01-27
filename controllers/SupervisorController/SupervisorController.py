"""SupervisorController controller."""
import time, yaml
import numpy as np
from controller import Supervisor
from SupervisorRobot import SupervisorRobot

# load config
f = open('../../worlds/world-setup.yml')
config = yaml.load(f, yaml.FullLoader)
f.close()

# load supervisor
scenario = "voluntaryGoalSwitching"
supervisor = SupervisorRobot(config, scenario)
timestep = int(supervisor.getBasicTimeStep())

# load E-Puck
supervisor.loadRobot(kind='epuck', ID='e-puck')

# prepare Data
f_traj = open("../../Data/trajectory.dat", 'w')
f_ev = open("../../Data/events.dat", 'w')

f_traj.write("{}\t{}\t{}\t{}".format("e-puck", supervisor.robotIDs[0], supervisor.robotIDs[1], supervisor.robotIDs[2]))
f_ev.wirte("{}\t{}\t{}\t{}\t{}".format("phase", "actionEpisode", "goal", "action", "target", "sound"))

# Main loop:
tic = time.time()
while supervisor.step(timestep) != -1:
    supervisor.updateState()
    supervisor.updatePhase()

    toc = time.time()
    if toc - tic > 100:
        tic = toc
        supervisor.currentState.phase['phase'] = 1
        supervisor.initPhase()
        
    if toc - tic > 100 and supervisor.phase == 1:
        tic = toc
        supervisor.currentState.phase['phase'] = 2
        supervisor.initPhase()

    # write data
    positions = "{} {}".format(supervisor.currentState.epuck.position, supervisor.currentState.epuck.orientation)
    for ID in supervisor.robotIDs:
        if isactive(ID):
            positions += "\t{}".format(supervisor.currentState.objects.ID.position)
        else:
            positions += "\t"

    f_traj.write("{}".format(positions))
    f_traj.flush()

    sound = 0
    for ID in supervisor.robotIDs:
        if isactive(ID):
            if supervisor.currentState.objects.ID.sound != 0:
                sound = supervisor.currentState.objects.ID.sound

    f_ev.write("{}\t{}\t{}\t{}\t{}".format(supervisor.currentState.phase.phase,
                                           supervisor.currentState.phase.actionEpisode,
                                           supervisor.currentState.epuck.goal,
                                           supervisor.currentState.epuck.action[:,0],
                                           supervisor.currentState.epuck.target[0],
                                           sound))
    f_ev.flush()

f_traj.close()
f_ev.close()
