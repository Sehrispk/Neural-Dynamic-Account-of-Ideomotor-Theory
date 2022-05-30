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
plotInterval = [139.5,144]
#cutInterval  = [111.5, 121.5]
snapShots = [139.6, 140.3, 140.7, 143]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

BeliefFormat = baseFormat.copy()
BeliefFormat.name = 'Belief Node'
BeliefFormat.pltType = 'timecourse'
BeliefFormat.pltPosition = (6,1,2)
BeliefFormat.xyLimits = {'x':plotInterval, 'y':[-15,3]}
BeliefFormat.xyLabel = {'x':'T[s]', 'y':'Belief\nNodes'}
BeliefFormat.xyTicks = {'x':None,'y':None}
BeliefFormat.snapShotMarkers = snapShots # [t0, t2, ...]
BeliefFormat.colors = {'B1': 'red', 'B2': 'magenta', 'B3': 'purple', 'B4': 'blue', 'B5': 'teal', 'B6': 'turquoise'} # {'col1': '-r', ...}
BeliefNodes = loadCedarData(path=pathParser('B1'), col_names=['T', 'B1'], dataType='node', plotFormat=BeliefFormat)
Be2 = loadCedarData(path=pathParser('B2'), col_names=['T', 'B2'], dataType='node', plotFormat=BeliefFormat)
Be3 = loadCedarData(path=pathParser('B3'), col_names=['T', 'B3'], dataType='node', plotFormat=BeliefFormat)
Be4 = loadCedarData(path=pathParser('B4'), col_names=['T', 'B4'], dataType='node', plotFormat=BeliefFormat)
Be5 = loadCedarData(path=pathParser('B5'), col_names=['T', 'B5'], dataType='node', plotFormat=BeliefFormat)
Be6 = loadCedarData(path=pathParser('B6'), col_names=['T', 'B6'], dataType='node', plotFormat=BeliefFormat)
BeliefNodes.appendData(Be2)
BeliefNodes.appendData(Be3)
BeliefNodes.appendData(Be4)
BeliefNodes.appendData(Be5)
BeliefNodes.appendData(Be6)
del Be2
del Be3
del Be4
del Be5
del Be6
BeliefNodes.data.iloc[:,0] = BeliefNodes.data.iloc[:,0].apply(correctTime)
BeliefNodes.pruneData(plotInterval)
#BeliefNodes.cutTimeWidnow(cutInterval)

RecallFormat = baseFormat.copy()
RecallFormat.name = 'Neural Nodes'
RecallFormat.pltType = 'timecourse'
RecallFormat.pltPosition = (6,1,1)
RecallFormat.xyLimits = {'x':plotInterval, 'y':[-2,0.5]}
RecallFormat.xyLabel = {'x':' ', 'y':'Contingency\nRecall Nodes'}
RecallFormat.xyTicks = {'x':None,'y':None}
RecallFormat.snapShotMarkers = snapShots # [t0, t2, ...]
RecallFormat.colors = {'ColorRecallIntention': 'red', 'ColorRecallCoS': 'magenta', 'ColorRecallCoD': 'purple', 'BeliefActive': 'blue'}
ColorRecallNodes = loadCedarData(path=pathParser('ColorRecall'), col_names=['T', 'ColorRecallIntention'], dataType='node', plotFormat=RecallFormat)
ColorRecallCoS = loadCedarData(path=pathParser('ColorRecallCoS'), col_names=['T', 'ColorRecallCoS'], dataType='node', plotFormat=RecallFormat)
ColorRecallCoD = loadCedarData(path=pathParser('ColorRecallCoD'), col_names=['T', 'ColorRecallCoD'], dataType='node', plotFormat=RecallFormat)
BeliefActiveNode = loadCedarData(path=pathParser('BeliefActiveNode'), col_names=['T', 'BeliefActive'], dataType='node', plotFormat=RecallFormat)
ColorRecallNodes.appendData(ColorRecallCoS)
ColorRecallNodes.appendData(ColorRecallCoD)
#ColorRecallNodes.appendData(BeliefActiveNode)
del ColorRecallCoS
del ColorRecallCoD
del BeliefActiveNode
ColorRecallNodes.data.iloc[:,0] = ColorRecallNodes.data.iloc[:,0].apply(correctTime)
ColorRecallNodes.pruneData(timeWindow=plotInterval)
#LearningNodes.cutTimeWidnow(cutInterval)

ColorRoleFormat = baseFormat.copy()
ColorRoleFormat.name = 'Color Role Nodes'
ColorRoleFormat.pltType = 'timecourse'
ColorRoleFormat.pltPosition = (7,1,3)
ColorRoleFormat.xyLimits = {'x':plotInterval, 'y':[-2.5,3.25]}
ColorRoleFormat.xyLabel = {'x':None, 'y':'Object\nRole'}
ColorRoleFormat.xyTicks = {'x':None,'y':None}
ColorRoleFormat.snapShotMarkers = snapShots
ColorRoleFormat.colors = {'r':'red', 'o':'orange', 'y':'yellow', 'g':'green', 'b':'blue', 'v':'violet'}
ColorRoleNodes = loadCedarData(path=pathParser('RoleColor'), col_names=['T','r', 'o', 'y', 'g', 'b', 'v'], dataType='node', plotFormat=ColorRoleFormat)
ColorRoleNodes.data.iloc[:,0] = ColorRoleNodes.data.iloc[:,0].apply(correctTime)
ColorRoleNodes.pruneData(plotInterval)
ColorRoleSnaps = generateSnapShotSeries(ColorRoleNodes, snapShots)

ActionRoleFormat = ColorRoleFormat.copy()
ActionRoleFormat.name = 'Action Role Nodes'
ActionRoleFormat.xyLabel = {'x':None, 'y':'Action\nRole'}
ActionRoleFormat.colors = {'A1':'blue', 'A2':'blue', 'A3':'blue'}
ActionRoleNodes = loadCedarData(path=pathParser('RoleAction'), col_names=['T','A1', 'A2', 'A3'], dataType='node', plotFormat=ActionRoleFormat)
ActionRoleNodes.data.iloc[:,0] = ActionRoleNodes.data.iloc[:,0].apply(correctTime)
ActionRoleNodes.pruneData(plotInterval)
ActionRoleSnaps = generateSnapShotSeries(ActionRoleNodes, snapShots)

OutcomeRoleFormat = ColorRoleFormat.copy()
OutcomeRoleFormat.name = 'Outcome Role Nodes'
OutcomeRoleFormat.xyLabel = {'x':None, 'y':'Outcome\nRole'}
OutcomeRoleFormat.colors = {'low':'blue', 'medium':'blue', 'high':'blue'}
OutcomeRoleNodes = loadCedarData(path=pathParser('RoleOutcome'), col_names=['T','low', 'medium', 'high'], dataType='node', plotFormat=OutcomeRoleFormat)
OutcomeRoleNodes.data.iloc[:,0] = OutcomeRoleNodes.data.iloc[:,0].apply(correctTime)
OutcomeRoleNodes.pruneData(plotInterval)
OutcomeRoleSnaps = generateSnapShotSeries(OutcomeRoleNodes, snapShots)

GoalSelectionFormat = ColorRoleFormat.copy()
GoalSelectionFormat.name = 'Goal Selection Nodes'
GoalSelectionFormat.xyLabel = {'x':None, 'y':'Goal\nSelection'}
GoalSelectionFormat.colors = {'low':'blue', 'medium':'blue', 'high':'blue'}
GoalSelectionNodes = loadCedarData(path=pathParser('GoalSelection'), col_names=['T','low', 'medium', 'high'], dataType='node', plotFormat=GoalSelectionFormat)
GoalSelectionNodes.data.iloc[:,0] = GoalSelectionNodes.data.iloc[:,0].apply(correctTime)
GoalSelectionNodes.pruneData(plotInterval)
GoalSelectionSnaps = generateSnapShotSeries(GoalSelectionNodes, snapShots)

i=0
while i<len(snapShots):
	ColorRoleSnaps[i].pltPosition = (6,4,17+i)
	ActionRoleSnaps[i].pltPosition = (6,4,13+i)
	OutcomeRoleSnaps[i].pltPosition = (6,4,9+i)
	GoalSelectionSnaps[i].pltPosition = (6,4,21+i)

	if i == 0:
		print("")
	else:
		ColorRoleSnaps[i].xyLabel['y'] = ''
		ActionRoleSnaps[i].xyLabel['y'] = ''
		OutcomeRoleSnaps[i].xyLabel['y'] = ''
		GoalSelectionSnaps[i].xyLabel['y'] = ''
	i+=1

figure_Data = {'BeliefNodes': BeliefNodes,
                'ColorRecall': ColorRecallNodes,
				'O1': OutcomeRoleSnaps[0],
				'O2': OutcomeRoleSnaps[1],
				'O3': OutcomeRoleSnaps[2],
				'O4': OutcomeRoleSnaps[3],
				'A1': ActionRoleSnaps[0],
				'A2': ActionRoleSnaps[1],
				'A3': ActionRoleSnaps[2],
				'A4': ActionRoleSnaps[3],
				'C1': ColorRoleSnaps[0],
				'C2': ColorRoleSnaps[1],
				'C3': ColorRoleSnaps[2],
				'C4': ColorRoleSnaps[3],
				'G1': GoalSelectionSnaps[0],
				'G2': GoalSelectionSnaps[1],
				'G3': GoalSelectionSnaps[2],
				'G4': GoalSelectionSnaps[3]}
figure_size = [200,1.4*200]
figure_format = {'title': "Opportunistic Activation", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
