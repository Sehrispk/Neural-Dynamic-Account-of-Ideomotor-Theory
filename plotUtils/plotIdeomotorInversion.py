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
plotInterval = [2137,2145]
#cutInterval  = [111.5, 121.5]
snapShots = [2137.2, 2138, 2141, 2144]

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
RecallFormat.pltPosition = (4,1,1)
RecallFormat.xyLimits = {'x':plotInterval, 'y':[-2,0.5]}
RecallFormat.xyLabel = {'x':'T[s]', 'y':'Strategy Recall\nNodes'}
RecallFormat.xyTicks = {'x':None,'y':None}
RecallFormat.snapShotMarkers = snapShots # [t0, t2, ...]
RecallFormat.colors = {'StrategyRecallIntention': 'red', 'StrategyRecallCoS': 'magenta', 'StrategyRecallCoD': 'purple', 'BeliefActive': 'blue'}
StrategyRecallNodes = loadCedarData(path=pathParser('StrategyRecall'), col_names=['T', 'StrategyRecallIntention'], dataType='node', plotFormat=RecallFormat)
StrategyRecallCoS = loadCedarData(path=pathParser('StrategyRecallCoS'), col_names=['T', 'StrategyRecallCoS'], dataType='node', plotFormat=RecallFormat)
StrategyRecallCoD = loadCedarData(path=pathParser('StrategyRecallCoD'), col_names=['T', 'StrategyRecallCoD'], dataType='node', plotFormat=RecallFormat)
#BeliefActiveNode = loadCedarData(path=pathParser('BeliefActiveNode'), col_names=['T', 'BeliefActive'], dataType='node', plotFormat=RecallFormat)
StrategyRecallNodes.appendData(StrategyRecallCoS)
StrategyRecallNodes.appendData(StrategyRecallCoD)
#ColorRecallNodes.appendData(BeliefActiveNode)
del StrategyRecallCoS
del StrategyRecallCoD
#del BeliefActiveNode
StrategyRecallNodes.data.iloc[:,0] = StrategyRecallNodes.data.iloc[:,0].apply(correctTime)
StrategyRecallNodes.pruneData(timeWindow=plotInterval)
#LearningNodes.cutTimeWidnow(cutInterval)

ColorRoleFormat = baseFormat.copy()
ColorRoleFormat.name = 'Color Role Nodes'
ColorRoleFormat.pltType = 'timecourse'
ColorRoleFormat.pltPosition = (6,1,3)
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
GoalSelectionFormat.xyLimits = {'x':plotInterval, 'y':[-3,2.75]}
GoalSelectionNodes = loadCedarData(path=pathParser('GoalSelection'), col_names=['T','low', 'medium', 'high'], dataType='node', plotFormat=GoalSelectionFormat)
GoalSelectionNodes.data.iloc[:,0] = GoalSelectionNodes.data.iloc[:,0].apply(correctTime)
GoalSelectionNodes.pruneData(plotInterval)
GoalSelectionSnaps = generateSnapShotSeries(GoalSelectionNodes, snapShots)

actionSelectionFormat = baseFormat.copy()
actionSelectionFormat.xyLabel = {'x':'', 'y':'Action Selection', 'size': 12}
actionSelectionFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
actionSelection = loadCedarData(path=pathParser('ActionSelection'), col_names=None, dataType='2dfield', plotFormat=actionSelectionFormat)
actionSelection.data.iloc[:,0] = actionSelection.data.iloc[:,0].apply(correctTime)
actionSelection._field_size = [3,6]
actionSelSn = generateSnapShotSeries(actionSelection, snapShots)

strategyFormat = baseFormat.copy()
strategyFormat.xyLabel = {'x':'', 'y':'Strategy', 'size': 12}
strategyFormat.xyTicks = {'x':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'y':{'ticks': [0,1,2], 'label': None}}
strategy = loadCedarData(path=pathParser('Strategy'), col_names=None, dataType='2dfield', plotFormat=strategyFormat)
strategy.data.iloc[:,0] = strategy.data.iloc[:,0].apply(correctTime)
strategy._field_size = [3,6]
strategySnaps = generateSnapShotSeries(strategy, snapShots)

i=0
while i<len(snapShots):
	ColorRoleSnaps[i].pltPosition = (6,4,21+i)
	ActionRoleSnaps[i].pltPosition = (6,4,17+i)
	OutcomeRoleSnaps[i].pltPosition = (6,4,13+i)
	GoalSelectionSnaps[i].pltPosition = (4,4,5+i)
	strategySnaps[i].pltPosition = (4,4,9+i)
	actionSelSn[i].pltPosition = (4,4,13+i)

	if i == 0:
		print("")
	else:
		ColorRoleSnaps[i].xyLabel['y'] = ''
		ActionRoleSnaps[i].xyLabel['y'] = ''
		OutcomeRoleSnaps[i].xyLabel['y'] = ''
		GoalSelectionSnaps[i].xyLabel['y'] = ''
		actionSelSn[i].xyLabel['y'] = ''
		actionSelSn[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
		strategySnaps[i].xyLabel['y'] = ''
		strategySnaps[i].xyTicks['y'] = {'ticks':[0,1,2], 'label': ['', '', '']}
	i+=1

figure_Data = {#'BeliefNodes': BeliefNodes,
				'StrategyRecall': StrategyRecallNodes,
				#'O1': OutcomeRoleSnaps[0],
				#'O2': OutcomeRoleSnaps[1],
				#'O3': OutcomeRoleSnaps[2],
				#'O4': OutcomeRoleSnaps[3],
				#'A1': ActionRoleSnaps[0],
				#'A2': ActionRoleSnaps[1],
				#'A3': ActionRoleSnaps[2],
				#'A4': ActionRoleSnaps[3],
				#'C1': ColorRoleSnaps[0],
				#'C2': ColorRoleSnaps[1],
				#'C3': ColorRoleSnaps[2],
				#'C4': ColorRoleSnaps[3],
				'G1': GoalSelectionSnaps[0],
				'G2': GoalSelectionSnaps[1],
				'G3': GoalSelectionSnaps[2],
				'G4': GoalSelectionSnaps[3],
				'strat1': strategySnaps[0],
				'strat2': strategySnaps[1],
				'strat3': strategySnaps[2],
				'strat4': strategySnaps[3],
				'acSel1': actionSelSn[0],
				'acSel2': actionSelSn[1],
				'acSel3': actionSelSn[2],
				'acSel4': actionSelSn[3]
				}
figure_size = [400,1.4*200]
figure_format = {'title': "Strategy Recall", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()