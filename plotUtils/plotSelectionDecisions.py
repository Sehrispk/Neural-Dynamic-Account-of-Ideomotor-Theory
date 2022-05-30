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
plotInterval = [2213,2967]
#cutInterval  = [1263, 1272]
#snapShots = [1259, 1260, 1275, 1280, 1289]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
#soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
#soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
#correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

ev = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
ev.pruneData(plotInterval)
events = ev.data

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
low_t = []
for i in range(len(low_dict)):
    if low_dict[i]-t0 > 1:
        low_t.append(low_dict[i])
    t0 = low_dict[i]

t0 = 0
med_t = []
for i in range(len(medium_dict)):
    if medium_dict[i]-t0 > 1:
        med_t.append(medium_dict[i])
    t0 = medium_dict[i]
    
t0 = 0
high_t = []
for i in range(len(high_dict)):
    if high_dict[i]-t0 > 1:
        high_t.append(high_dict[i])
    t0 = high_dict[i]

print(low_t)
print(med_t)
print(high_t)  

figure = plt.figure(figsize=(10, 10))
selectionPlot = figure.add_subplot(1, 1, 1)

selectionPlot.plot(low_t, [1 for i in range(len(low_t))], color='red', marker='s', linestyle='None', markersize=15)
selectionPlot.plot(med_t, [2 for i in range(len(med_t))], color='green', marker='s', linestyle='None', markersize=15)
selectionPlot.plot(high_t, [3 for i in range(len(high_t))], color='blue', marker='s', linestyle='None', markersize=15)
selectionPlot.set_xlim([plotInterval[0]-20, plotInterval[1]+20])
selectionPlot.set_ylim([0.9,3.1])
selectionPlot.set_xlabel('T [s]', fontsize=20)
selectionPlot.set_ylabel('Goals', fontsize=20)
selectionPlot.set_yticks([1,2,3], labels=['low-pitch', 'medium-pitch', 'high-pitch'], minor=False, fontsize=16)
selectionPlot.tick_params('both', direction='in', top=True, right=True, labelsize=16)
selectionPlot.title.set_text('Goal Selection Decisions')
selectionPlot.title.set_size(20)
plt.show()