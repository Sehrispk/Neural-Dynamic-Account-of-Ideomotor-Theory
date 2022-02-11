"""SupervisorController controller."""

# Webots todo!!!!
# (TUNING OF TIMERS)
# goal selection phase after each action episode? -> maybe only if goal decays?
# implement multiple contingencies for 1 sound

#DFT Tuning/todos
# TUNING OF BELIEF STRUCTURE
#tuning of memory traces
# desire in DFT architecture? -> probably not
# connect new tasks
# implement dft exp to reset architecture
# plan recoring
# exploring when no strategy?


import time, yaml
import numpy as np
from controller import Supervisor
from SupervisorRobot import SupervisorRobot

def isActive(ID, supervisor):
    try:
        supervisor.activeRobots[ID]
        return 1
    except:
        return 0

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
supervisor.currentState.epuck['action'] = np.zeros((3,2))
supervisor.currentState.epuck['actionTarget'] = ['','']
supervisor.currentState.epuck['position'] = np.zeros(3)

# prepare Data
f_traj = open("../../data/trajectory2.dat", 'w')
f_ev = open("../../data/events2.dat", 'w')
f_count = open("../../data/actionCount2.dat", 'w')

f_traj.write("{}\t{}\t{}\t{}\t{}\n".format("Time", "e-puck", supervisor.robotIDs[0], supervisor.robotIDs[1], supervisor.robotIDs[2]))
f_ev.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("Time", "phase", "phaseEpisode", "actionEpisode", "goal", "action", "target", "sound"))

# Main loop:
tic = time.time()
init = 0
count = supervisor.currentState.phase['actionCounter'].copy()
f_count.write("T:\t{}\n{}\n".format(supervisor.clock.reading, supervisor.currentState.phase['actionCounter']))
while supervisor.step(timestep) != -1:
    supervisor.updateState()
    supervisor.updatePhase()

    #toc = time.time()
    #if toc - tic > 3 and supervisor.currentState.phase['phase'] == 0 and not init:
    #    tic = toc
    #    init=1
    #    supervisor.initPhase()
    
    #if toc - tic > 30 and supervisor.currentState.phase['phase'] == 0:
    #    tic = toc
    #   supervisor.currentState.phase['phase'] = 1
    #   supervisor.initPhase()
        
    #if toc - tic > 60 and supervisor.currentState.phase['phase'] == 1:
    #    tic = toc
    #    supervisor.currentState.phase['phase'] = 2
    #    supervisor.initPhase()

    # write data
    positions = "{} {} {}".format(supervisor.currentState.epuck['position'], supervisor.currentState.epuck['orientation'], supervisor.currentState.epuck['led'])
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            positions += "\t{}".format(supervisor.currentState.objects[ID]['position'])
        else:
            positions += "\t"

    f_traj.write("{}\t{}\n".format(supervisor.clock.reading, positions))
    f_traj.flush()

    sound = np.zeros(10)
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            if any(supervisor.currentState.objects[ID]['sound']):
                sound = supervisor.currentState.objects[ID]['sound']

    f_ev.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(supervisor.clock.reading, supervisor.currentState.phase['phase'],
                                           supervisor.phaseEpisode,
                                           supervisor.currentState.phase['actionEpisode'],
                                           supervisor.currentState.epuck['goal'],
                                           supervisor.currentState.epuck['action'][:,0],
                                           supervisor.currentState.epuck['actionTarget'][0],
                                           sound))
    f_ev.flush()
    
    if not count.equals(supervisor.currentState.phase['actionCounter']):
        count = supervisor.currentState.phase['actionCounter'].copy()
        f_count.write("{}\n{}\n".format(supervisor.clock.reading, supervisor.currentState.phase['actionCounter']))
        f_count.flush()

f_traj.close()
f_ev.close()
f_count.close()
