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
plotInterval = [955,1110]
cutInterval  = [979, 1097]
snapShots = [962.5, 1105, 971, 976.5]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

GoalSelectionFormat = baseFormat.copy()
GoalSelectionFormat.name = 'Goal Selection Nodes'
GoalSelectionFormat.xyLabel = {'x':None, 'y':'Goal\nSelection'}
GoalSelectionFormat.colors = {'low-pitch':'red', 'medium-pitch':'magenta', 'high-pitch':'blue'}
GoalSelectionFormat.xyLimits = {'x':plotInterval, 'y':[-1,1]}
GoalSelectionFormat.pltPosition = (6,1,2)
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
GoalCoSFormat.pltPosition = (6,1,1)
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
GoalTimeoutFormat.pltPosition = (6,1,1)
GoalTimeout = loadCedarData(path=pathParser('GoalInhibition'), col_names=['T', 'GoalInhibition'], dataType='node', plotFormat=GoalTimeoutFormat)
GoalCoS.appendData(GoalTimeout)
del GoalTimeout
GoalCoS.data.iloc[:,0] = GoalCoS.data.iloc[:,0].apply(correctTime)
GoalCoS.pruneData(plotInterval)
GoalCoS.cutTimeWidnow(cutInterval)

MemoryTracesFormat = baseFormat.copy()
MemoryTracesFormat.name = 'MemoryTraces'
MemoryTracesFormat.xyLabel = {'x':'T[s]', 'y':'Memory\nTraces'}
MemoryTracesFormat.colors = {'Exc-Mem-Low': 'red', 'Exc-Mem-Med': 'magenta', 'Exc-Mem-High': 'purple', 'Inh-Mem-Low': 'blue', 'Inh-Mem-Med': 'teal', 'Inh-Mem-High': 'turquoise'}
MemoryTracesFormat.xyLimits = {'x':plotInterval, 'y':[0.4, 0.7]}
MemoryTracesFormat.pltPosition = (6,1,3)
MemoryTracesFormat.snapShotMarkers = snapShots
MemoryTraces = loadCedarData(path=pathParser('posMemTrace'), col_names=['T','Exc-Mem-Low', 'Exc-Mem-Med', 'Exc-Mem-High'], dataType='node', plotFormat=MemoryTracesFormat)
negMem = loadCedarData(path=pathParser('negMemTrace'), col_names=['T','Inh-Mem-Low', 'Inh-Mem-Med', 'Inh-Mem-High'], dataType='node', plotFormat=MemoryTracesFormat)
MemoryTraces.appendData(negMem)
del negMem
MemoryTraces.data.iloc[:,0] = MemoryTraces.data.iloc[:,0].apply(correctTime)
MemoryTraces.pruneData(plotInterval)
MemoryTraces.data = MemoryTraces.data.drop(['Exc-Mem-Low', 'Inh-Mem-Low', 'Exc-Mem-High', 'Inh-Mem-High'], axis=1)
#MemoryTraces.data['Exc-Mem-Low'] = MemoryTraces.data['Exc-Mem-Low'].apply(lambda x: x*0.45)
#MemoryTraces.data['Inh-Mem-Low'] = MemoryTraces.data['Inh-Mem-Low'].apply(lambda x: x*0.8)
#MemoryTraces.data['Exc-Mem-High'] = MemoryTraces.data['Exc-Mem-High'].apply(lambda x: x*0.45)
#MemoryTraces.data['Inh-Mem-High'] = MemoryTraces.data['Inh-Mem-High'].apply(lambda x: x*0.8)
MemoryTraces.data['Exc-Mem-Med'] = MemoryTraces.data['Exc-Mem-Med'].apply(lambda x: x*0.45)
MemoryTraces.data['Inh-Mem-Med'] = MemoryTraces.data['Inh-Mem-Med'].apply(lambda x: x*0.8)
MemoryTraces.cutTimeWidnow(cutInterval)

cameraFormat = baseFormat.copy()
cameraFormat.name = 'Camera' # name
cameraFormat.pltType = 'timecourse' # timecourse, snapshot
cameraFormat.pltPosition = (4, 1, 4) # (n_rows, n_cols, index)
cameraFormat.xyLimits = {'x':plotInterval,'y':None} # {'x': xlim, 'y': ylim}
cameraFormat.xyLabel = {'x':None,'y':None,'size':None} # {'x': 'x', 'y': 'y', 'size': size}
cameraFormat.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
cameraFormat.snapShotMarkers = None # [t0, t2, ...]
cameraFormat.colors = None # {'col1': '-r', ...}
camera = loadCedarData(path=pathParser('CameraImage'), col_names=None, dataType='image', plotFormat=cameraFormat)
camera.data.iloc[:,0] = camera.data.iloc[:,0].apply(correctTime)
camera.pruneData(plotInterval)
images = generateSnapShotSeries(camera, snapShots)
images[0].pltPosition = (6,2,11)
images[1].pltPosition = (6,2,12)

actionSelectionFormat = baseFormat.copy()
actionSelectionFormat.xyLabel = {'x':'', 'y':'Action\nSelection', 'size': 12}
actionSelectionFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
actionSelection = loadCedarData(path=pathParser('ActionSelection'), col_names=None, dataType='2dfield', plotFormat=actionSelectionFormat)
actionSelection.data.iloc[:,0] = actionSelection.data.iloc[:,0].apply(correctTime)
actionSelection._field_size = [3,6]
actionSelection.pruneData(timeWindow=plotInterval)
actionSelSn = generateSnapShotSeries(actionSelection, snapShots)
actionSelSn[0].pltPosition = (6,2,9)
actionSelSn[1].xyLabel['y'] = ''
actionSelSn[1].pltPosition = (6,2,10)

strategyFormat = baseFormat.copy()
strategyFormat.xyLabel = {'x':'', 'y':'Strategy', 'size': 12}
strategyFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
strategy = loadCedarData(path=pathParser('Strategy'), col_names=None, dataType='2dfield', plotFormat=strategyFormat)
strategy.data.iloc[:,0] = strategy.data.iloc[:,0].apply(correctTime)
strategy._field_size = [3,6]
strategySnaps = generateSnapShotSeries(strategy, snapShots)
strategySnaps[0].pltPosition = (6,2,7)
strategySnaps[1].xyLabel['y'] = ''
strategySnaps[1].pltPosition = (6,2,8)


i = 0

figure_Data = {'CoS': GoalCoS,
				'GoalSelection': GoalSelectionNodes,
                'Mem': MemoryTraces,
                'img1': images[0],
                'img2': images[1],
                'str1': strategySnaps[0],
                'str2': strategySnaps[1],
                'act1': actionSelSn[0],
                'act2': actionSelSn[1]
				}
figure_size = [200,1.4*200]
figure_format = {'title': "Goal Habituation", 
				 'lineWidth': 3}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
