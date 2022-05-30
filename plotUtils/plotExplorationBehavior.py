from ast import Constant
from email.headerregistry import ContentTransferEncodingHeader
from email.mime import base
import numpy as np
import matplotlib.pyplot as plt
import yaml
import pandas as pd

from loadData import *
from correctTimeOffSet import *
from PlotFigure import PlotFigure

with open("config.yml", "r") as f:
	config = yaml.load(f, yaml.FullLoader)
pathParser = lambda fileKey: r"{}\{}".format(config['BasePath'], config['FileNames'][fileKey])

baseFormat = plotFormat()
plotInterval = [20,1800]

ev = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
actionC = loadWebotsData(path=pathParser('Histograms'), col_names=['T', 'counter'], dataType='webots', plotFormat=baseFormat.copy())
ev.pruneData(plotInterval)
actionC.pruneData(plotInterval)
events = ev.data
actionCount = actionC.data

playedSounds = {'500Hz': [], '1000Hz': [], '1500Hz': []}
actions = {'A1':{'red': [],'yellow': [],'green': [],'blue': []}, 'A2':{'red': [],'yellow': [],'green': [],'blue': []}, 'A3':{'red': [],'yellow': [],'green': [],'blue': []}}
performed_action = np.zeros(12)
previous_action = np.zeros(12)
for t in actionCount['T'].values:
    soundInterval = events.loc[(events['T']>=t-3) & (events['T']<=t)]
    performed_action = [actionCount.loc[actionCount['T']==t]['counter'].values[0][i] - previous_action[i] for i in range(len(performed_action))]
    previous_action = actionCount.loc[actionCount['T']==t]['counter'].values[0]
    act_idx = tuple(zip(*np.where(np.reshape(performed_action, (3,4))==1)))[0]

    if act_idx[0]==0:
        if act_idx[1]==0:
            actions['A1']['red'].append(t)
        if act_idx[1]==1:
            actions['A1']['green'].append(t)
        if act_idx[1]==2:
            actions['A1']['blue'].append(t)
        if act_idx[1]==3:
            actions['A1']['yellow'].append(t)

    if act_idx[0]==1:
        if act_idx[1]==0:
            actions['A2']['red'].append(t)
        if act_idx[1]==1:
            actions['A2']['green'].append(t)
        if act_idx[1]==2:
            actions['A2']['blue'].append(t)
        if act_idx[1]==3:
            actions['A2']['yellow'].append(t)

    if act_idx[0]==2:
        if act_idx[1]==0:
            actions['A3']['red'].append(t)
        if act_idx[1]==1:
            actions['A3']['green'].append(t)
        if act_idx[1]==2:
            actions['A3']['blue'].append(t)
        if act_idx[1]==3:
            actions['A3']['yellow'].append(t)

    playedSound = 0
    for value in list(soundInterval['sound'].values):
        try:
            idx = value.index(1.0)
        except:
            idx = None
        if idx == 9:
            playedSound = '1500Hz'
        elif idx == 6:
            playedSound = '1000Hz'
        elif idx == 2:
            playedSound = '500Hz'
        

    if playedSound:
        playedSounds[playedSound].append(t)
    playedSound = 0

print(playedSounds)
print(actions)

figure = plt.figure(figsize=(10, 10))
actionPlot = figure.add_subplot(2, 1, 1)
soundPlot = figure.add_subplot(2,1,2)

actionPlot.plot(actions['A1']['red'], [1 for i in actions['A1']['red']], color='red', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A1']['green'], [1 for i in actions['A1']['green']], color='green', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A1']['blue'], [1 for i in actions['A1']['blue']], color='blue', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A1']['yellow'], [1 for i in actions['A1']['yellow']], color='yellow', marker='s', linestyle='None', markersize=10)

actionPlot.plot(actions['A2']['red'], [2 for i in actions['A2']['red']], color='red', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A2']['green'], [2 for i in actions['A2']['green']], color='green', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A2']['blue'], [2 for i in actions['A2']['blue']], color='blue', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A2']['yellow'], [2 for i in actions['A2']['yellow']], color='yellow', marker='s', linestyle='None', markersize=10)

actionPlot.plot(actions['A3']['red'], [3 for i in actions['A3']['red']], color='red', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A3']['green'], [3 for i in actions['A3']['green']], color='green', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A3']['blue'], [3 for i in actions['A3']['blue']], color='blue', marker='s', linestyle='None', markersize=10)
actionPlot.plot(actions['A3']['yellow'], [3 for i in actions['A3']['yellow']], color='yellow', marker='s', linestyle='None', markersize=10)
actionPlot.set_xlim([0,1800])
actionPlot.set_ylim([0.9,3.1])
actionPlot.set_xlabel('T [s]', fontsize=20)
actionPlot.set_ylabel('Actions', fontsize=20)
actionPlot.set_yticks([1,2,3], labels=['A1', 'A2', 'A3'], minor=False, fontsize=16)
actionPlot.tick_params('both', direction='in', top=True, right=True)
actionPlot.title.set_text('Performed Actions')
actionPlot.title.set_size(20)

soundPlot.plot(playedSounds['500Hz'], [1 for i in playedSounds['500Hz']], color='red', marker='s', linestyle='None', markersize=10)
soundPlot.plot(playedSounds['1000Hz'], [2 for i in playedSounds['1000Hz']], color='green', marker='s', linestyle='None', markersize=10)
soundPlot.plot(playedSounds['1500Hz'], [3 for i in playedSounds['1500Hz']], color='blue', marker='s', linestyle='None', markersize=10)
soundPlot.plot(actions['A3']['yellow'], [1 for i in actions['A3']['yellow']], color='yellow', marker='s', linestyle='None', markersize=10)
soundPlot.set_xlim([0,1800])
soundPlot.set_ylim([0.9,3.1])
soundPlot.tick_params('both', direction='in', top=True, right=True)
soundPlot.set_xlabel('T [s]', fontsize=20)
soundPlot.set_yticks([1,2,3], labels=['500Hz', '1000Hz', '1500Hz'], minor=False, fontsize=16)
soundPlot.title.set_text('Played Sounds')
soundPlot.title.set_size(20)
soundPlot.set_ylabel('Sound [Hz]', fontsize=20)
plt.show()
# load action counts
# load events
# prune tmiewindow to exploration phase
# for each action event
    # take timepont and search corresponding point in events
    # if sound is played in the nexts three seconds
        # mark down sound event

# then combine both action events and sound events
    # 2 plots (subplots)
    # played sound
    # poduced action
    # histogram in inkscape