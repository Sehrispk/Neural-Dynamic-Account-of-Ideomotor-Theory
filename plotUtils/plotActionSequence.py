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
plotInterval = [1258,1290]
cutInterval  = [1263, 1272]
snapShots = [1259, 1260, 1275, 1280, 1289]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

IntentionFormat = baseFormat.copy()
IntentionFormat.name = 'Neural Nodes'
IntentionFormat.pltType = 'timecourse'
IntentionFormat.pltPosition = (3,1,1)
IntentionFormat.xyLimits = {'x':plotInterval, 'y':[-2,1.1]}
IntentionFormat.xyLabel = {'x':'T[s]', 'y':'Intnetion/CoS\nNodes'}
IntentionFormat.xyTicks = {'x':None,'y':None}
IntentionFormat.snapShotMarkers = snapShots # [t0, t2, ...]
IntentionFormat.colors = {'priorInt': 'red', 'OrientInt': 'magenta', 'BrakeInt': 'purple', 'LEDInt': 'blue'}
IntentionNodes = loadCedarData(path=pathParser('PriorI'), col_names=['T', 'priorInt'], dataType='node', plotFormat=IntentionFormat)
OrientInt = loadCedarData(path=pathParser('OrientIiA'), col_names=['T', 'OrientInt'], dataType='node', plotFormat=IntentionFormat)
DriveInt = loadCedarData(path=pathParser('DriveIiA'), col_names=['T', 'BrakeInt'], dataType='node', plotFormat=IntentionFormat)
LEDInt = loadCedarData(path=pathParser('LEDIiA'), col_names=['T', 'LEDInt'], dataType='node', plotFormat=IntentionFormat)
#priorCoS = loadCedarData(path=pathParser('PriorCoS'), col_names=['T', 'priorCoS'], dataType='node', plotFormat=IntentionFormat)
#OrientCoS = loadCedarData(path=pathParser('OrientCoS'), col_names=['T', 'OrientCoS'], dataType='node', plotFormat=IntentionFormat)
#DriveCoS = loadCedarData(path=pathParser('DriveCoS'), col_names=['T', 'DriveCoS'], dataType='node', plotFormat=IntentionFormat)
#LEDCoS = loadCedarData(path=pathParser('LEDCoS'), col_names=['T', 'LEDCoS'], dataType='node', plotFormat=IntentionFormat)
#IntentionNodes.appendData(priorCoS)
IntentionNodes.appendData(OrientInt)
#IntentionNodes.appendData(OrientCoS)
IntentionNodes.appendData(DriveInt)
#IntentionNodes.appendData(DriveCoS)
IntentionNodes.appendData(LEDInt)
#IntentionNodes.appendData(LEDCoS)
#del priorCoS
del OrientInt
#del OrientCoS
del DriveInt
#del DriveCoS
del LEDInt
#del LEDCoS
IntentionNodes.data.iloc[:,0] = IntentionNodes.data.iloc[:,0].apply(correctTime)
IntentionNodes.pruneData(timeWindow=plotInterval)
IntentionNodes.cutTimeWidnow(cutInterval)

space2RateFormat = baseFormat.copy()
space2RateFormat.name = 'Space To Rate Code'
space2RateFormat.pltType = 'timecourse'
space2RateFormat.pltPosition = (6,1,4)
space2RateFormat.xyLimits = {'x':plotInterval, 'y':[0,52]}
space2RateFormat.xyLabel = {'x':'', 'y':'Target\nOrientation'}
space2RateFormat.xyTicks = {'x':None,'y':{'ticks':[0,13,26,39,50], 'label':None}}
space2RateFormat.snapShotMarkers = snapShots # [t0, t2, ...]
space2RateFormat.colors = None # {'col1': '-r', ...}
space2rate = loadCedarData(path=pathParser('Space2Rate'), col_names=['T', 'Sp2Rt'], dataType='node', plotFormat=space2RateFormat)
space2rate.data.iloc[:,0] = space2rate.data.iloc[:,0].apply(correctTime)
space2rate.pruneData(plotInterval)
space2rate.cutTimeWidnow(cutInterval)

breakFormat = baseFormat.copy()
breakFormat.name = 'Brake Node'
breakFormat.pltType = 'timecourse'
breakFormat.pltPosition = (6,1,5)
breakFormat.xyLimits = {'x':plotInterval, 'y':[-1,0.5]}
breakFormat.xyLabel = {'x':'', 'y':'Brake\nNode'}
breakFormat.xyTicks = {'x':None,'y':None}
breakFormat.snapShotMarkers = snapShots # [t0, t2, ...]
breakFormat.colors = None # {'col1': '-r', ...}
breakNode = loadCedarData(path=pathParser('BrakeNode'), col_names=['T', 'Brake'], dataType='node', plotFormat=breakFormat)
breakNode.data.iloc[:,0] = breakNode.data.iloc[:,0].apply(correctTime)
breakNode.pruneData(plotInterval)
breakNode.cutTimeWidnow(cutInterval)

LEDFormat = baseFormat.copy()
LEDFormat.name = 'Neural Nodes'
LEDFormat.pltType = 'timecourse'
LEDFormat.pltPosition = (6,1,6)
LEDFormat.xyLimits = {'x':plotInterval, 'y':[0,1.7]}
LEDFormat.xyLabel = {'x':'T[s]', 'y':'LED\nNodes'}
LEDFormat.xyTicks = {'x':None,'y':None}
LEDFormat.snapShotMarkers = snapShots # [t0, t2, ...]
LEDFormat.colors = {'LED1': 'red', 'LED2': 'magenta', 'LED3': 'purple', 'LED4': 'blue', 'LED5': 'teal', 'LED6': 'turquoise', 'LED7': 'lime', 'LED8': 'green', 'LED9': 'yellow'}
LEDsNodes = loadCedarData(path=pathParser('LEDs'), col_names=['T', 'LED1', 'LED2', 'LED3', 'LED4', 'LED5', 'LED6', 'LED7', 'LED8', 'LED9' ], dataType='node', plotFormat=LEDFormat)
LEDsNodes.data.iloc[:,0] = LEDsNodes.data.iloc[:,0].apply(correctTime)
LEDsNodes.pruneData(timeWindow=plotInterval)
LEDsNodes.cutTimeWidnow(cutInterval)

actionSelectionFormat = baseFormat.copy()
actionSelectionFormat.xyLabel = {'x':'', 'y':'Action\nSelection', 'size': 12}
actionSelectionFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
actionSelection = loadCedarData(path=pathParser('ActionSelection'), col_names=None, dataType='2dfield', plotFormat=actionSelectionFormat)
actionSelection.data.iloc[:,0] = actionSelection.data.iloc[:,0].apply(correctTime)
actionSelection._field_size = [3,6]
actionSelection.pruneData(timeWindow=plotInterval)
actionSelSn = generateSnapShotSeries(actionSelection, snapShots)

i=0
while i<len(snapShots):
	actionSelSn[i].pltPosition = (6,5,11+i)

	if i == 0:
		actionSelSn[i]._label_pad = 30
	else:
		actionSelSn[i].xyLabel['y'] = ''
		actionSelSn[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
	i+=1

figure_Data = {'Intention': IntentionNodes,
				'Space2Rate': space2rate,
                'Brake': breakNode,
                'LEDs': LEDsNodes,
				'acSel1': actionSelSn[0],
				'acSel2': actionSelSn[1],
				'acSel3': actionSelSn[2],
				'acSel4': actionSelSn[3],
                'acSel5': actionSelSn[4]
				}
figure_size = [2*200,1.4*200]
figure_format = {'title': "Action Sequence", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
