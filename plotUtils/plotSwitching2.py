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
plotInterval = [3141,3180]
cutInterval  = [3148, 3156]
snapShots = [3141.2, 3142, 3147, 3158, 3165]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

GoalSelectionFormat = baseFormat.copy()
GoalSelectionFormat.name = 'Goal Selection Nodes'
GoalSelectionFormat.xyLabel = {'x':None, 'y':'Goal\nSelection'}
GoalSelectionFormat.colors = {'low-pitch':'red', 'medium-pitch':'magenta', 'high-pitch':'blue'}
GoalSelectionFormat.xyLimits = {'x':plotInterval, 'y':[-2.5,2.8]}
GoalSelectionFormat.pltPosition = (3,1,2)
GoalSelectionFormat.snapShotMarkers = snapShots
GoalSelectionNodes = loadCedarData(path=pathParser('GoalSelection'), col_names=['T','low-pitch', 'medium-pitch', 'high-pitch'], dataType='node', plotFormat=GoalSelectionFormat)
GoalSelectionNodes.data.iloc[:,0] = GoalSelectionNodes.data.iloc[:,0].apply(correctTime)
GoalSelectionNodes.pruneData(plotInterval)
GoalSelectionNodes.cutTimeWidnow(cutInterval)

GoalCoSFormat = baseFormat.copy()
GoalCoSFormat.name = 'Goal-CoS Node'
GoalCoSFormat.xyLabel = {'x':None, 'y':'Neural\nNodes'}
GoalCoSFormat.colors = {'GoalCoS':'red', 'GoalInhibition': 'blue'}
GoalCoSFormat.xyLimits = {'x':plotInterval, 'y':[-2,0.5]}
GoalCoSFormat.pltPosition = (3,1,1)
GoalCoSFormat.snapShotMarkers = snapShots
GoalCoS = loadCedarData(path=pathParser('GoalCoS'), col_names=['T','GoalCoS'], dataType='node', plotFormat=GoalCoSFormat)
'''SelectionSignalFormat = baseFormat.copy()
SelectionSignalFormat.name = 'Selection Signal'
SelectionSignalFormat.xyLabel = {'x':None, 'y':'Selection Signal'}
SelectionSignalFormat.colors = {'Goal-CoS':'red', 'SelectionSignal': 'blue'}
SelectionSignalFormat.xyLimits = {'x':plotInterval, 'y':None}
SelectionSignal = loadCedarData(path=pathParser('SuperVisorCommands'), col_names=['T', 'Exp', 'P', 'T1', 'T2', 'T3', 'SelectionSignal', 'Sw', 'End'], dataType='node', plotFormat=SelectionSignalFormat)
SelectionSignal.data = SelectionSignal.data.drop(['Exp', 'T1', 'T2', 'T3', 'Sw', 'End', 'P'], axis=1)'''
GoalTimeoutFormat = baseFormat.copy()
GoalTimeoutFormat.name = 'Goal-CoS Node'
GoalTimeoutFormat.xyLabel = {'x':None, 'y':'Neural\nNodes'}
GoalTimeoutFormat.colors = {'GoalCoS':'red', 'GoalInhibition': 'blue'}
GoalTimeoutFormat.xyLimits = {'x':plotInterval, 'y':[-2,0.5]}
GoalTimeoutFormat.pltPosition = (3,1,1)
GoalTimeout = loadCedarData(path=pathParser('GoalInhibition'), col_names=['T', 'GoalInhibition'], dataType='node', plotFormat=GoalTimeoutFormat)
GoalCoS.appendData(GoalTimeout)
del GoalTimeout
GoalCoS.data.iloc[:,0] = GoalCoS.data.iloc[:,0].apply(correctTime)
GoalCoS.pruneData(plotInterval)
GoalCoS.cutTimeWidnow(cutInterval)

MemoryTracesFormat = baseFormat.copy()
MemoryTracesFormat.name = 'MemoryTraces'
MemoryTracesFormat.xyLabel = {'x':'T[s]', 'y':'Memory\nTraces'}
MemoryTracesFormat.colors = {'Exc-Mem-Low': 'red', 'Exc-Mem2': 'magenta', 'Exc-Mem-High': 'purple', 'Inh-Mem-Low': 'blue', 'Inh-Mem2': 'teal', 'Inh-Mem-High': 'turquoise'}
MemoryTracesFormat.xyLimits = {'x':plotInterval, 'y':[-0.2, 0.6]}
MemoryTracesFormat.pltPosition = (3,1,3)
MemoryTracesFormat.snapShotMarkers = snapShots
MemoryTraces = loadCedarData(path=pathParser('posMemTrace'), col_names=['T','Exc-Mem-Low', 'Exc-Mem2', 'Exc-Mem-High'], dataType='node', plotFormat=MemoryTracesFormat)
negMem = loadCedarData(path=pathParser('negMemTrace'), col_names=['T','Inh-Mem-Low', 'Inh-Mem2', 'Inh-Mem-High'], dataType='node', plotFormat=MemoryTracesFormat)
MemoryTraces.appendData(negMem)
del negMem
MemoryTraces.data.iloc[:,0] = MemoryTraces.data.iloc[:,0].apply(correctTime)
MemoryTraces.pruneData(plotInterval)
MemoryTraces.data = MemoryTraces.data.drop(['Exc-Mem2', 'Inh-Mem2'], axis=1)
MemoryTraces.data['Exc-Mem-Low'] = MemoryTraces.data['Exc-Mem-Low'].apply(lambda x: x*0.45)
MemoryTraces.data['Inh-Mem-Low'] = MemoryTraces.data['Inh-Mem-Low'].apply(lambda x: x*0.8)
MemoryTraces.data['Exc-Mem-High'] = MemoryTraces.data['Exc-Mem-High'].apply(lambda x: x*0.45)
MemoryTraces.data['Inh-Mem-High'] = MemoryTraces.data['Inh-Mem-High'].apply(lambda x: x*0.8)
MemoryTraces.cutTimeWidnow(cutInterval)

figure_Data = {'CoS': GoalCoS,
				'GoalSelection': GoalSelectionNodes,
                'Mem': MemoryTraces
				}
figure_size = [200,1.4*200]
figure_format = {'title': "Goal Switching", 
				 'lineWidth': 3}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
