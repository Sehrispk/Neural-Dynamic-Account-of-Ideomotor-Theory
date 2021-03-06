"""SupervisorController controller."""

#DFT Tuning/todos
#tuning of memory traces
#positive memory traces -> schnelleres ansteigen und absteigen
#timer für belief activation anpassen

#webots -> experiemnt sequenzen anpassen
# -> memory traces nach jeder sequenz rücksetzen
# -> nach test -> einzeln perseveration und habituation testen
# test für unterschiedliche strategien zum selben sound testen

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

f_traj.write("{},{},{},{},{},{}\n".format("Time", "SimulationTime", "e-puck", supervisor.robotIDs[0], supervisor.robotIDs[1], supervisor.robotIDs[2]))
f_ev.write("{},{},{},{},{},{},{},{}\n".format("Time", "phase", "phaseEpisode", "actionEpisode", "goal", "action", "target", "sound"))
#f_count.write("T, r1, g1, b1, y1, r2, g2, b2, y2, r3, g3, b3, y3\n")
f_count.write("T,counter\n")

# Main loop:
init = 0
tic = time.time()
count = supervisor.currentState.phase['actionCounter'].copy()
f_count.write("{},{}\n".format(supervisor.clock.reading, supervisor.currentState.phase['actionCounter'].to_numpy().flatten()))
print("start experiment...")
while supervisor.step(timestep) != -1:
    supervisor.updateState()
    supervisor.updatePhase()

    # write data
    positions = "[{}, {}, {}]".format(supervisor.currentState.epuck['position'], supervisor.currentState.epuck['orientation'], supervisor.currentState.epuck['led'])
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            positions += ",{}".format(supervisor.currentState.objects[ID]['position'])
        else:
            positions += ","

    toc = time.time()
    f_traj.write("{},{},{}\n".format(toc-tic, supervisor.clock.reading, positions))
    f_traj.flush()

    sound = np.zeros(10)
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            if any(supervisor.currentState.objects[ID]['sound']):
                sound = supervisor.currentState.objects[ID]['sound']

    f_ev.write("{},{},{},{},{},{},{},{}\n".format(supervisor.clock.reading,supervisor.currentState.phase['phase'],
                                           supervisor.phaseEpisode,
                                           supervisor.currentState.phase['actionEpisode'],
                                           list(supervisor.currentState.epuck['goal']),
                                           list(supervisor.currentState.epuck['action'][:,0]),
                                           supervisor.currentState.epuck['actionTarget'][0],
                                           list(sound)))
    f_ev.flush()
    
    if not count.equals(supervisor.currentState.phase['actionCounter']):
        count = supervisor.currentState.phase['actionCounter'].copy()
        f_count.write("{},{}\n".format(supervisor.clock.reading, supervisor.currentState.phase['actionCounter'].to_numpy().flatten()))
        f_count.flush()

f_traj.close()
f_ev.close()
f_count.close()
