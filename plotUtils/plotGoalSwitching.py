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
plotInterval = [2969,3586]
#cutInterval  = [1263, 1272]
#snapShots = [1259, 1260, 1275, 1280, 1289]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
#soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
#soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
#correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

ev = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
actionC = loadWebotsData(path=pathParser('Histograms'), col_names=['T', 'counter'], dataType='webots', plotFormat=baseFormat.copy())
ev.pruneData(plotInterval)
actionC.pruneData(plotInterval)
events = ev.data
actionCount = actionC.data

playedSounds = {'500Hz': [], '1000Hz': [], '1500Hz': []}
for t in actionCount['T'].values:
    soundInterval = events.loc[(events['T']>=t-3) & (events['T']<=t)]
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

threshold = 0.8
low_dict = []
medium_dict = []
high_dict = []

for t in events['T'].values:
    g = events.loc[events['T']==t, 'g'].values[0]
    if g[0] > threshold:
        low_dict.append(t)
    elif g[1] > threshold:
        medium_dict.append(t)
    elif g[2] > threshold:
        high_dict.append(t)

t0 = 0
i0 = 0
low_t = []
for i in range(len(low_dict)):
    if low_dict[i]-t0 > 1:
        low_t += [low_dict[i0:i]]
        i0 = i
    t0 = low_dict[i]
low_t += [low_dict[i0:]]

t0 = 0
i0 = 0
med_t = []
for i in range(len(medium_dict)):
    if medium_dict[i]-t0 > 1:
        med_t += [medium_dict[i0:i]]
        i0 = i
    t0 = medium_dict[i]
med_t += [medium_dict[i0:]]
    
t0 = 0
i0 = 0
high_t = []
for i in range(len(high_dict)):
    if high_dict[i]-t0 > 1:
        high_t += [high_dict[i0:i]]
        i0 = i
    t0 = high_dict[i]
high_t += [high_dict[i0:]]

print(low_t)
print(med_t)
print(high_t)  

figure = plt.figure(figsize=(10, 10))
soundPlot = figure.add_subplot(2,1,1)
selectionPlot = figure.add_subplot(2, 1, 2)

for timewindow in low_t[1:]:
    selectionPlot.plot(timewindow, [1 for i in range(len(timewindow))], color='red', linewidth=20)

for timewindow in med_t[1:]:
    selectionPlot.plot(timewindow, [2 for i in range(len(timewindow))], color='green', linewidth=20)

for timewindow in high_t[1:]:
    selectionPlot.plot(timewindow, [3 for i in range(len(timewindow))], color='blue', linewidth=20)

soundPlot.plot(playedSounds['500Hz'], [1 for i in playedSounds['500Hz']], color='red', marker='s', linestyle='None', markersize=10)
soundPlot.plot(playedSounds['1000Hz'], [2 for i in playedSounds['1000Hz']], color='green', marker='s', linestyle='None', markersize=10)
soundPlot.plot(playedSounds['1500Hz'], [3 for i in playedSounds['1500Hz']], color='blue', marker='s', linestyle='None', markersize=10)
soundPlot.set_xlim([plotInterval[0]-20, plotInterval[1]+20])
soundPlot.set_ylim([0.9,3.1])
soundPlot.tick_params('both', direction='in', top=True, right=True, labelsize=16)
soundPlot.set_xlabel('T [s]', fontsize=20)
soundPlot.set_yticks([1,2,3], labels=['500Hz', '1000Hz', '1500Hz'], minor=False, fontsize=16)
soundPlot.title.set_text('Played Sounds')
soundPlot.title.set_size(20)
soundPlot.set_ylabel('Sound [Hz]', fontsize=20)

"""selectionPlot.plot(low_t, [1 for i in range(len(low_t))], color='red', marker='s', linestyle='None', markersize=10)
selectionPlot.plot(med_t, [2 for i in range(len(med_t))], color='green', marker='s', linestyle='None', markersize=10)
selectionPlot.plot(high_t, [3 for i in range(len(high_t))], color='blue', marker='s', linestyle='None', markersize=10)"""
selectionPlot.set_xlim([plotInterval[0]-20, plotInterval[1]+20])
selectionPlot.set_ylim([0.9,3.1])
selectionPlot.set_xlabel('T [s]', fontsize=20)
selectionPlot.set_ylabel('Goals', fontsize=20)
selectionPlot.set_yticks([1,2,3], labels=['low-pitch', 'medium-pitch', 'high-pitch'], minor=False, fontsize=16)
selectionPlot.tick_params('both', direction='in', top=True, right=True, labelsize=16)
selectionPlot.title.set_text('Current Goal')
selectionPlot.title.set_size(20)
plt.show()