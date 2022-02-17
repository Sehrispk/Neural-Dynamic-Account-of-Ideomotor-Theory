"""SupervisorController controller."""

#Webots todo!!!!
#goal selection phase after N(each) action episodes -> requires goal reset
#handcrafted sequence of action episodes

#DFT Tuning/todos
#tuning of memory traces
#plan recoring and plotting of data
#exploring when no strategy


import datetime, yaml, os, time
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
path = "../../data/Simulation/Simulation_" + datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
if not os.path.isdir("../../data/"):
    os.mkdir("../../data/")
if not os.path.isdir("../../data/Simulation/"):
    os.mkdir("../../data/Simulation/")
if not os.path.isdir(path):
    os.mkdir(path)  

f_traj = open(path + "/trajectory.dat", 'w')
f_ev = open(path + "/events.dat", 'w')
f_count = open(path + "/actionCount.dat", 'w')

f_traj.write("{}\t{}\t{}\t{}\t{}\t{}\n".format("Time", "SimulationTime", "e-puck", supervisor.robotIDs[0], supervisor.robotIDs[1], supervisor.robotIDs[2]))
f_ev.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("Time", "phase", "phaseEpisode", "actionEpisode", "goal", "action", "target", "sound"))

# Main loop:
init = 0
tic = time.time()
count = supervisor.currentState.phase['actionCounter'].copy()
f_count.write("T:\t{}\n{}\n".format(supervisor.clock.reading, supervisor.currentState.phase['actionCounter']))
while supervisor.step(timestep) != -1:
    supervisor.updateState()
    supervisor.updatePhase()

    # write data
    positions = "{} {} {}".format(supervisor.currentState.epuck['position'], supervisor.currentState.epuck['orientation'], supervisor.currentState.epuck['led'])
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            positions += "\t{}".format(supervisor.currentState.objects[ID]['position'])
        else:
            positions += "\t"

    toc = time.time()
    f_traj.write("{}\t{}\t{}\n".format(toc-tic, supervisor.clock.reading, positions))
    f_traj.flush()

    sound = np.zeros(10)
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            if any(supervisor.currentState.objects[ID]['sound']):
                sound = supervisor.currentState.objects[ID]['sound']

    f_ev.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(supervisor.clock.reading,supervisor.currentState.phase['phase'],
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
