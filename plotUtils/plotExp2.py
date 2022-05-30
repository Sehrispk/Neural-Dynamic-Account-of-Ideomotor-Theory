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
plotInterval = [105,130]
cutInterval  = [110, 120]
snapShots = [106, 109, 128]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

IntentionFormat = baseFormat.copy()
IntentionFormat.name = 'Neural Nodes'
IntentionFormat.pltType = 'timecourse'
IntentionFormat.pltPosition = (3,1,1)
IntentionFormat.xyLimits = {'x':plotInterval, 'y':[-2,1.8]}
IntentionFormat.xyLabel = {'x':'T[s]', 'y':'Intnetion/CoS\nNodes'}
IntentionFormat.xyTicks = {'x':None,'y':None}
IntentionFormat.snapShotMarkers = snapShots # [t0, t2, ...]
IntentionFormat.colors = {'priorInt': 'red', 'OrientInt': 'magenta', 'BreakInt': 'purple', 'LEDInt': 'blue'}
IntentionNodes = loadCedarData(path=pathParser('PriorI'), col_names=['T', 'priorInt'], dataType='node', plotFormat=IntentionFormat)
OrientInt = loadCedarData(path=pathParser('OrientIiA'), col_names=['T', 'OrientInt'], dataType='node', plotFormat=IntentionFormat)
DriveInt = loadCedarData(path=pathParser('DriveIiA'), col_names=['T', 'BreakInt'], dataType='node', plotFormat=IntentionFormat)
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

actionSelectionFormat = baseFormat.copy()
actionSelectionFormat.xyLabel = {'x':'', 'y':'Action\nSelection', 'size': 12}
actionSelectionFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
actionSelection = loadCedarData(path=pathParser('ActionSelection'), col_names=None, dataType='2dfield', plotFormat=actionSelectionFormat)
actionSelection.data.iloc[:,0] = actionSelection.data.iloc[:,0].apply(correctTime)
actionSelection._field_size = [3,6]
actionSelection.pruneData(timeWindow=plotInterval)
actionSelSn = generateSnapShotSeries(actionSelection, snapShots)

inhibitionOfReturunFormat = baseFormat.copy()
inhibitionOfReturunFormat.xyLabel = {'x':'', 'y':'Memory\nReturn', 'size': 12}
inhibitionOfReturunFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
inhibitionOfReturn = loadCedarData(path=pathParser('InhibitionOfReturn'), col_names=None, dataType='2dfield', plotFormat=inhibitionOfReturunFormat)
inhibitionOfReturn.data.iloc[:,0] = inhibitionOfReturn.data.iloc[:,0].apply(correctTime)
inhibitionOfReturn._field_size = [3,6]
inhibitionOfReturn.pruneData(timeWindow=plotInterval)
inhibitionOfReturnSnaps = generateSnapShotSeries(inhibitionOfReturn, snapShots)


i=0
while i<len(snapShots):
	actionSelSn[i].pltPosition = (3,3,4+i)
	inhibitionOfReturnSnaps[i].pltPosition = (3,3,7+i)

	if i == 0:
		actionSelSn[i]._label_pad = 15
		print("")
	else:
		actionSelSn[i].xyLabel['y'] = ''
		actionSelSn[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
		inhibitionOfReturnSnaps[i].xyLabel['y'] = ''
		inhibitionOfReturnSnaps[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
	i+=1

figure_Data = {'Intention': IntentionNodes,
				'acSel1': actionSelSn[0],
				'acSel2': actionSelSn[1],
				'acSel3': actionSelSn[2],
				'inh1': inhibitionOfReturnSnaps[0],
				'inh2': inhibitionOfReturnSnaps[1],
				'inh3': inhibitionOfReturnSnaps[2]
				}
figure_size = [200,100]
figure_format = {'title': "Exploration", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
