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
plotInterval = [500,600]
cutInterval  = [505, 575]
snapShots = [576, 587, 595]

soundConceptsFormat = baseFormat.copy()
soundConceptsFormat.name = 'Sound Concepts'
soundConceptsFormat.pltPosition = (5,1,2)
soundConceptsFormat.xyLabel = {'x': 'T[s]', 'y': soundConceptsFormat.name, 'size': 12}
soundConceptsFormat.xyLimits = {'x': plotInterval, 'y': [-1,1]}
soundConceptsFormat.colors = {'S1': 'r', 'S2': 'g', 'S3': 'b'}
soundConcepts = loadCedarData(path=pathParser('SoundConcepts'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=soundConceptsFormat)
soundConcepts.snapShotMarkers = snapShots

colorConceptsFormat = baseFormat.copy()
colorConceptsFormat.name = 'Color Concepts'
colorConceptsFormat.pltPosition = (5,3,7)
colorConceptsFormat.xyLabel = {'x':'Color', 'y':'Color Concepts', 'size':12}
colorConceptsFormat.xyLimits = {'x': [0,5], 'y':[-1,1]}
colorConceptsFormat.xyTicks['x'] = {'ticks': [0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}
colorConceptsFormat.colors = 'red'
colorConcepts = loadCedarData(path=pathParser('ColorConcepts'), col_names=None, dataType='1dfield', plotFormat=colorConceptsFormat)

goalSelectionFormat = baseFormat.copy()
goalSelectionFormat.name = 'Goal Selection'
goalSelectionFormat.xyLabel = {'x': ' ', 'y': 'Goal Selection', 'size': 12}
goalSelectionFormat.xyLimits = {'x': plotInterval, 'y': [-3,2]}
goalSelectionFormat.colors = {'G1': 'red', 'G2': 'green', 'G3': 'blue'}
goalSelection = loadCedarData(path=pathParser('GoalSelection'), col_names=['T', 'G1', 'G2', 'G3'], dataType='node', plotFormat=goalSelectionFormat)

goalCoSFormat = baseFormat.copy()
goalCoSFormat.name = 'Goal CoS'
goalCoSFormat.pltPosition = (5,1,1)
goalCoSFormat.xyLabel = {'x': ' ', 'y': 'Goal CoS/CoD', 'size': 12}
goalCoSFormat.xyLimits = {'x': plotInterval, 'y': [-3,2]}
goalCoSFormat.colors = {'CoS': 'red'}
goalCoS = loadCedarData(path=pathParser('GoalCoS'), col_names=['T', 'CoS'], dataType='node', plotFormat=goalCoSFormat)
goalCoS.snapShotMarkers = snapShots

goalCoDFormat = goalCoSFormat.copy()
goalCoDFormat.name = 'Goal CoD'
goalCoDFormat.colors = {'CoD': 'blue'}
goalCoD = loadCedarData(path=pathParser('GoalCoD'), col_names=['T', 'CoD'], dataType='node', plotFormat=goalCoDFormat)

goalCoS.appendData(goalCoD)
goalCoS.colors = {'CoS': 'red', 'CoD': 'blue'}
goalCoS.name = 'Goal CoS/CoD'
del goalCoD

actionSelectionFormat = baseFormat.copy()
actionSelectionFormat.xyLabel = {'x':'Color', 'y':'Action Selection', 'size': 12}
actionSelectionFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
actionSelection = loadCedarData(path=pathParser('ActionSelection'), col_names=None, dataType='2dfield', plotFormat=actionSelectionFormat)
actionSelection._field_size = [6,3]

webotsEventFormat = baseFormat.copy()
webotsEvents = loadWebotsData(path=pathParser('events'), col_names=['T', 'phase', 'phaseEpisode', 'actEpisode','goal', 'action', 'target', 'sound'], dataType='webots', plotFormat=webotsEventFormat)

correctTime = correctTimeOffSet(soundConcepts.data, webotsEvents.data[['T', 'sound']])
soundConcepts.data.iloc[:,0] = soundConcepts.data.iloc[:,0].apply(correctTime)
goalSelection.data.iloc[:,0] = goalSelection.data.iloc[:,0].apply(correctTime)
goalCoS.data.iloc[:,0] = goalCoS.data.iloc[:,0].apply(correctTime)
actionSelection.data.iloc[:,0] = actionSelection.data.iloc[:,0].apply(correctTime)
colorConcepts.data.iloc[:,0] = colorConcepts.data.iloc[:,0].apply(correctTime)

soundConcepts.pruneData(timeWindow=plotInterval)
goalSelection.pruneData(timeWindow=plotInterval)
goalCoS.pruneData(timeWindow=plotInterval)
goalCoS.pruneData(timeWindow=plotInterval)
actionSelection.pruneData(timeWindow=plotInterval)
colorConcepts.pruneData(timeWindow=plotInterval)

goalCoS.cutTimeWidnow(timeWindow=cutInterval)
soundConcepts.cutTimeWidnow(timeWindow=cutInterval)

actionSelectionSnapshots = generateSnapShotSeries(actionSelection, snapShots)
goalSnapshots = generateSnapShotSeries(goalSelection, snapShots)
colorSnapshots = generateSnapShotSeries(colorConcepts, snapShots)

i=0
while i < len(snapShots):
	colorSnapshots[i].pltPosition = (5,3,10+i)
	colorSnapshots[i]._field_dim = [0,6]
	goalSnapshots[i].pltPosition = (5,3,7+i)
	actionSelectionSnapshots[i].pltPosition = (5,3,13+i)
	if i > 0:
		goalSnapshots[i].xyLabel['y']=''
		goalSnapshots[i].xyTicks['y']={'ticks':None, 'label':[]}
		actionSelectionSnapshots[i].xyLabel['y']=''
		actionSelectionSnapshots[i].xyTicks['y']={'ticks':[0,1,2], 'label':[]}
		colorSnapshots[i].xyLabel['y']=''
		colorSnapshots[i].xyTicks['y']={'ticks':None, 'label':[]}
	elif i == 0:
		colorSnapshots[i]._label_pad = 10
		goalSnapshots[i]._label_pad = -0.05
		actionSelectionSnapshots[i]._label_pad = 25
	i += 1

figure_Data = {'sounds':soundConcepts, 
			   'goalCoS': goalCoS,
			   'goal1': goalSnapshots[0],
			   'goal2': goalSnapshots[1],
			   'goal3': goalSnapshots[2],
			   'actSel1': actionSelectionSnapshots[0],
			   'actSel2': actionSelectionSnapshots[1],
			   'actSel3': actionSelectionSnapshots[2],
			   'img1': colorSnapshots[0],
			   'img2': colorSnapshots[1],
			   'img3': colorSnapshots[2]}
figure_size = [200,180]
figure_format = {'title': 'GoalReachingAttempts', 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
