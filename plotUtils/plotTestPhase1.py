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
plotInterval = [2000,2145]
#cutInterval  = [111.5, 121.5]
snapShots = [2080, 2085, 2142.6, 2144]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

cameraFormat = baseFormat.copy()
cameraFormat.name = 'Camera' # name
cameraFormat.pltType = 'timecourse' # timecourse, snapshot
cameraFormat.pltPosition = (6, 1, 4) # (n_rows, n_cols, index)
cameraFormat.xyLimits = {'x':plotInterval,'y':None} # {'x': xlim, 'y': ylim}
cameraFormat.xyLabel = {'x':None,'y':None,'size':None} # {'x': 'x', 'y': 'y', 'size': size}
cameraFormat.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
cameraFormat.snapShotMarkers = None # [t0, t2, ...]
cameraFormat.colors = None # {'col1': '-r', ...}
camera = loadCedarData(path=pathParser('CameraImage'), col_names=None, dataType='image', plotFormat=cameraFormat)
camera.data.iloc[:,0] = camera.data.iloc[:,0].apply(correctTime)
camera.pruneData(plotInterval)
images = generateSnapShotSeries(camera, snapShots)
images[0].xyLabel['y'] = 'Camera'

GoalSelectionFormat = baseFormat.copy()
GoalSelectionFormat.name = 'Goal Selection Nodes'
GoalSelectionFormat.xyLabel = {'x':None, 'y':'Goal\nSelection'}
GoalSelectionFormat.colors = {'low':'blue', 'medium':'blue', 'high':'blue'}
GoalSelectionFormat.xyLimits = {'x':plotInterval, 'y':[-3,2.75]}
GoalSelectionNodes = loadCedarData(path=pathParser('GoalSelection'), col_names=['T','low', 'medium', 'high'], dataType='node', plotFormat=GoalSelectionFormat)
GoalSelectionNodes.data.iloc[:,0] = GoalSelectionNodes.data.iloc[:,0].apply(correctTime)
GoalSelectionNodes.pruneData(plotInterval)
GoalSelectionSnaps = generateSnapShotSeries(GoalSelectionNodes, snapShots)

actionSelectionFormat = baseFormat.copy()
actionSelectionFormat.xyLabel = {'x':'', 'y':'Action\nSelection', 'size': 12}
actionSelectionFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
actionSelection = loadCedarData(path=pathParser('ActionSelection'), col_names=None, dataType='2dfield', plotFormat=actionSelectionFormat)
actionSelection.data.iloc[:,0] = actionSelection.data.iloc[:,0].apply(correctTime)
actionSelection._field_size = [3,6]
actionSelection.pruneData(timeWindow=plotInterval)
actionSelSn = generateSnapShotSeries(actionSelection, snapShots)

colorAttentionF = baseFormat.copy()
colorAttentionF.name = 'Color Attention' # name
colorAttentionF.pltType = 'timecourse' # timecourse, snapshot
colorAttentionF.pltPosition = (6, 1, 3) # (n_rows, n_cols, index)
colorAttentionF.xyLimits = {'x':plotInterval,'y':[-3.25,1.0]} # {'x': xlim, 'y': ylim}
colorAttentionF.xyLabel = {'x':'Color','y':'Color\nAttention','size':12} # {'x': 'x', 'y': 'y', 'size': size}
colorAttentionF.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
colorAttentionF.snapShotMarkers = None # [t0, t2, ...]
colorAttentionF.colors = None # {'col1': '-r', ...}
colorAttention = loadCedarData(path=pathParser('ColorAttention'), col_names=None, dataType='1dfield', plotFormat=colorAttentionF)
colorAttention.data.iloc[:,0] = colorAttention.data.iloc[:,0].apply(correctTime)
colorAttention._field_size = [0,20]
colorAttention._field_dim = [0,20]
colorAttention.pruneData(timeWindow=plotInterval)
colorAttentionSnaps = generateSnapShotSeries(colorAttention, snapShots)

strategyFormat = baseFormat.copy()
strategyFormat.xyLabel = {'x':'', 'y':'Strategy', 'size': 12}
strategyFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
strategy = loadCedarData(path=pathParser('Strategy'), col_names=None, dataType='2dfield', plotFormat=strategyFormat)
strategy.data.iloc[:,0] = strategy.data.iloc[:,0].apply(correctTime)
strategy._field_size = [3,6]
strategySnaps = generateSnapShotSeries(strategy, snapShots)

i=0
while i<len(snapShots):
	GoalSelectionSnaps[i].pltPosition = (5,4,1+i)
	strategySnaps[i].pltPosition = (5,4,5+i)
	actionSelSn[i].pltPosition = (5,4,9+i)
	images[i].pltPosition = (5,4,17+i)
	colorAttentionSnaps[i].pltPosition = (5,4,13+i)

	if i == 0:
		actionSelSn[i]._label_pad = 15
		images[i]._label_pad = 23
	else:
		actionSelSn[i].xyLabel['y'] = ''
		actionSelSn[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
		colorAttentionSnaps[i].xyLabel['y'] = ''
		colorAttentionSnaps[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
		strategySnaps[i].xyLabel['y'] = ''
		strategySnaps[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
		GoalSelectionSnaps[i].xyLabel['y'] = ''
	i+=1

figure_Data = {'Intention1': actionSelSn[0],
				'Intention2': actionSelSn[1],
				'Intention3': actionSelSn[2],
				'Intention4': actionSelSn[3],
				'GoalSelection1': GoalSelectionSnaps[0],
				'GoalSelection2': GoalSelectionSnaps[1],
				'GoalSelection3': GoalSelectionSnaps[2],
				'GoalSelection4': GoalSelectionSnaps[3],
				'camera1': images[0],
				'camera2': images[1],
				'camera3': images[2],
				'camera4': images[3],
				'strategy1': strategySnaps[0],
				'strategy2': strategySnaps[1],
				'strategy3': strategySnaps[2],
				'strategy4': strategySnaps[3],
				'colorAttention1': colorAttentionSnaps[0],
				'colorAttention2': colorAttentionSnaps[1],
				'colorAttention3': colorAttentionSnaps[2],
				'colorAttention4': colorAttentionSnaps[3]
				}
figure_size = [200,200]
figure_format = {'title': "Feature Guiding", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
