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
plotInterval = [121,129]
#cutInterval  = [111.5, 121.5]
snapShots = [121.2, 122.35, 124.5, 128.5]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=['T', 'ph', 'ph2', 'acE', 'g', 'a', 't','sound'], dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

BeliefFormat = baseFormat.copy()
BeliefFormat.name = 'Belief Node'
BeliefFormat.pltType = 'timecourse'
BeliefFormat.pltPosition = (6,1,2)
BeliefFormat.xyLimits = {'x':plotInterval, 'y':[-16,8]}
BeliefFormat.xyLabel = {'x':' ', 'y':'Belief\nNodes'}
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

CommitFormat = baseFormat.copy()
CommitFormat.name = 'Commit Node'
CommitFormat.pltType = 'timecourse'
CommitFormat.pltPosition = (6,1,3)
CommitFormat.xyLimits = {'x':plotInterval, 'y':[-2,2]}
CommitFormat.xyLabel = {'x':'T[s]', 'y':'Commit\nNodes'}
CommitFormat.xyTicks = {'x':None,'y':None}
CommitFormat.snapShotMarkers = snapShots # [t0, t2, ...]
CommitFormat.colors = {'C1': 'red', 'C2': 'magenta', 'C3': 'purple', 'C4': 'blue', 'C5': 'teal', 'C6': 'turquoise'} # {'col1': '-r', ...}
CommitNodes = loadCedarData(path=pathParser('C1'), col_names=['T', 'C1'], dataType='node', plotFormat=CommitFormat)
Co2 = loadCedarData(path=pathParser('C2'), col_names=['T', 'C2'], dataType='node', plotFormat=CommitFormat)
Co3 = loadCedarData(path=pathParser('C3'), col_names=['T', 'C3'], dataType='node', plotFormat=CommitFormat)
Co4 = loadCedarData(path=pathParser('C4'), col_names=['T', 'C4'], dataType='node', plotFormat=CommitFormat)
Co5 = loadCedarData(path=pathParser('C5'), col_names=['T', 'C5'], dataType='node', plotFormat=CommitFormat)
Co6 = loadCedarData(path=pathParser('C6'), col_names=['T', 'C6'], dataType='node', plotFormat=CommitFormat)
CommitNodes.appendData(Co2)
CommitNodes.appendData(Co3)
CommitNodes.appendData(Co4)
CommitNodes.appendData(Co5)
CommitNodes.appendData(Co6)
del Co2
del Co3
del Co4
del Co5
del Co6
CommitNodes.data.iloc[:,0] = CommitNodes.data.iloc[:,0].apply(correctTime)
CommitNodes.pruneData(plotInterval)
#BeliefNodes.cutTimeWidnow(cutInterval)

LearningFormat = baseFormat.copy()
LearningFormat.name = 'Neural Nodes'
LearningFormat.pltType = 'timecourse'
LearningFormat.pltPosition = (6,1,1)
LearningFormat.xyLimits = {'x':plotInterval, 'y':[-2,0.5]}
LearningFormat.xyLabel = {'x':' ', 'y':'Neural\nNodes'}
LearningFormat.xyTicks = {'x':None,'y':None}
LearningFormat.snapShotMarkers = snapShots # [t0, t2, ...]
LearningFormat.colors = {'LearnNode': 'magenta', 'CommitBoost': 'purple', 'RecruitNode': 'blue', 'BeliefActive': 'teal', 'RewardNode': 'turquoise', 'OutcomeDetection':'red'}
LearningNodes = loadCedarData(path=pathParser('LearningNode'), col_names=['T', 'LearnNode'], dataType='node', plotFormat=LearningFormat)
OutcomeDetection = loadCedarData(path=pathParser('OutcomeDetection'), col_names=['T', 'OutcomeDetection'], dataType='node', plotFormat=LearningFormat)
CommitBoostNode = loadCedarData(path=pathParser('CommitBoostNode'), col_names=['T', 'CommitBoost'], dataType='node', plotFormat=LearningFormat)
RecruitNode = loadCedarData(path=pathParser('RecruitNode'), col_names=['T', 'RecruitNode'], dataType='node', plotFormat=LearningFormat)
BeliefActive = loadCedarData(path=pathParser('BeliefActiveNode'), col_names=['T', 'BeliefActive'], dataType='node', plotFormat=LearningFormat)
RewardNode = loadCedarData(path=pathParser('RewardNode'), col_names=['T', 'RewardNode'], dataType='node', plotFormat=LearningFormat)
LearningNodes.appendData(CommitBoostNode)
LearningNodes.appendData(RecruitNode)
LearningNodes.appendData(BeliefActive)
LearningNodes.appendData(RewardNode)
LearningNodes.appendData(OutcomeDetection)
del CommitBoostNode
del RecruitNode
del BeliefActive
del RewardNode
del OutcomeDetection
LearningNodes.data.iloc[:,0] = LearningNodes.data.iloc[:,0].apply(correctTime)
LearningNodes.pruneData(timeWindow=plotInterval)
#LearningNodes.cutTimeWidnow(cutInterval)

'''RecallIntentionsFormat = baseFormat.copy()
RecallIntentionsFormat.name = 'Neural Nodes'
RecallIntentionsFormat.pltType = 'timecourse'
RecallIntentionsFormat.pltPosition = (6,1,3)
RecallIntentionsFormat.xyLimits = {'x':plotInterval, 'y':[-2,0.5]}
RecallIntentionsFormat.xyLabel = {'x':' ', 'y':'Neural\nNodes'}
RecallIntentionsFormat.xyTicks = {'x':None,'y':None}
RecallIntentionsFormat.snapShotMarkers = snapShots # [t0, t2, ...]
RecallIntentionsFormat.colors = {'OutcomeDetection': 'red', 'ColorRecall': 'blue', 'StrategyRecall': 'green'}
RecallIntentions = loadCedarData(path=pathParser('OutcomeDetection'), col_names=['T', 'OutcomeDetection'], dataType='node', plotFormat=RecallIntentionsFormat)
ColorRecall = loadCedarData(path=pathParser('ColorRecall'), col_names=['T', 'ColorRecall'], dataType='node', plotFormat=RecallIntentionsFormat)
StrategyRecall = loadCedarData(path=pathParser('StrategyRecall'), col_names=['T', 'StrategyRecall'], dataType='node', plotFormat=RecallIntentionsFormat)
RecallIntentions.appendData(ColorRecall)
RecallIntentions.appendData(StrategyRecall)
del ColorRecall
del StrategyRecall
RecallIntentions.data.iloc[:,0] = RecallIntentions.data.iloc[:,0].apply(correctTime)
RecallIntentions.pruneData(timeWindow=plotInterval)'''
#RecallIntentions.cutTimeWidnow(cutInterval)

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

i=0
while i<len(snapShots):
	ColorRoleSnaps[i].pltPosition = (6,4,21+i)
	ActionRoleSnaps[i].pltPosition = (6,4,17+i)
	OutcomeRoleSnaps[i].pltPosition = (6,4,13+i)

	if i == 0:
		print("")
	else:
		ColorRoleSnaps[i].xyLabel['y'] = ''
		ActionRoleSnaps[i].xyLabel['y'] = ''
		OutcomeRoleSnaps[i].xyLabel['y'] = ''
	i+=1


figure_Data = {'BeliefNodes': BeliefNodes,
                'LearningNodes': LearningNodes,
				'CommitNodes': CommitNodes,
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
				'C4': ColorRoleSnaps[3]}
figure_size = [200,1.4*200]
figure_format = {'title': "Belief Formation", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()