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
plotInterval = [1181,1185]
#cutInterval  = [505, 575]
snapShots = [1181.5,1183,1183.5,1184.5]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=None, dataType='webots', plotFormat=baseFormat.copy())
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

intentionFormat = baseFormat.copy()
intentionFormat.name = 'Intention'
intentionFormat.pltType = 'timecourse'
intentionFormat.pltPosition = (5,1,1)
intentionFormat.xyLimits = {'x':plotInterval, 'y':[-2,1]}
intentionFormat.xyLabel = {'x':' ', 'y':'Intention/CoS\nNode'}
intentionFormat.xyTicks = {'x':None,'y':None}
intentionFormat.snapShotMarkers = snapShots # [t0, t2, ...]
intentionFormat.colors = None # {'col1': '-r', ...}
intentionNode = loadCedarData(path=pathParser('OrientIiA'), col_names=['T', 'IiA'], dataType='node', plotFormat=intentionFormat)
intentionNode.data.iloc[:,0] = intentionNode.data.iloc[:,0].apply(correctTime)
intentionNode.pruneData(plotInterval)

CoSFormat = baseFormat.copy()
CoSFormat.name = 'CoS'
CoSFormat.pltType = 'timecourse'
CoSFormat.pltPosition = (5,1,1)
CoSFormat.xyLimits = {'x':plotInterval, 'y':[-2,1]}
CoSFormat.xyLabel = {'x':' ', 'y':'Intention/CoS\nNode'}
CoSFormat.xyTicks = {'x':None,'y':None}
CoSFormat.snapShotMarkers = snapShots # [t0, t2, ...]
CoSFormat.colors = None # {'col1': '-r', ...}
CoSNode = loadCedarData(path=pathParser('OrientCoS'), col_names=['T', 'CoS'], dataType='node', plotFormat=CoSFormat)
CoSNode.data.iloc[:,0] = CoSNode.data.iloc[:,0].apply(correctTime)
CoSNode.pruneData(plotInterval)
intentionNode.appendData(CoSNode)
intentionNode.colors = {'IiA':'blue', 'CoS':'red'}

space2RateFormat = baseFormat.copy()
space2RateFormat.name = 'Space To Rate Code'
space2RateFormat.pltType = 'timecourse'
space2RateFormat.pltPosition = (5,1,2)
space2RateFormat.xyLimits = {'x':plotInterval, 'y':[0,52]}
space2RateFormat.xyLabel = {'x':'Time [s]', 'y':'Target\nOrientation'}
space2RateFormat.xyTicks = {'x':None,'y':{'ticks':[0,13,26,39,50], 'label':None}}
space2RateFormat.snapShotMarkers = snapShots # [t0, t2, ...]
space2RateFormat.colors = None # {'col1': '-r', ...}
space2rate = loadCedarData(path=pathParser('Space2Rate'), col_names=['T', 'Sp2Rt'], dataType='node', plotFormat=space2RateFormat)
space2rate.data.iloc[:,0] = space2rate.data.iloc[:,0].apply(correctTime)
space2rate.pruneData(plotInterval)

colorMatchingFormat = baseFormat.copy()
colorMatchingFormat.name = 'Color Matching'
colorMatchingFormat.pltType = 'timecourse'
colorMatchingFormat.pltPosition = (6,1,3)
colorMatchingFormat.xyLimits = {'x':plotInterval, 'y':[-2,0.5]}
colorMatchingFormat.xyLabel = {'x':None, 'y':'Color Match'}
colorMatchingFormat.xyTicks = {'x':None,'y':None}
colorMatchingFormat.snapShotMarkers = snapShots
colorMatchingFormat.colors = {'r':'red', 'o':'orange', 'y':'yellow', 'g':'green', 'b':'blue', 'v':'violet'}
colorMatching = loadCedarData(path=pathParser('ColorMatching'), col_names=['T','r', 'o', 'y', 'g', 'b', 'v'], dataType='node', plotFormat=colorMatchingFormat)
colorMatching.data.iloc[:,0] = colorMatching.data.iloc[:,0].apply(correctTime)
colorMatching.pruneData(plotInterval)
cMatchSnaps = generateSnapShotSeries(colorMatching, snapShots)

spaceMatchingFormat = baseFormat.copy()
spaceMatchingFormat.name = 'Space Matching'
spaceMatchingFormat.pltType = 'timecourse'
spaceMatchingFormat.pltPosition = (6,1,3)
spaceMatchingFormat.xyLimits = {'x':plotInterval, 'y':[-1.8,0.5]}
spaceMatchingFormat.xyLabel = {'x':'Horizontal Position', 'y':'Space Match'}
spaceMatchingFormat.xyTicks = {'x':None,'y':None}
spaceMatchingFormat.snapShotMarkers = snapShots
spaceMatchingFormat.colors = None
spaceMatching = loadCedarData(path=pathParser('SpaceMatching'), col_names=None, dataType='1dfield', plotFormat=spaceMatchingFormat)
spaceMatching._field_dim =[0,52]
spaceMatching.data.iloc[:,0] = spaceMatching.data.iloc[:,0].apply(correctTime)
spaceMatching.pruneData(plotInterval)
spMatchSnaps = generateSnapShotSeries(spaceMatching, snapShots)

actionSelectionFormat = baseFormat.copy()
actionSelectionFormat.xyLabel = {'x':'Color', 'y':'Action Selection', 'size': 12}
actionSelectionFormat.xyTicks = {'y':{'ticks':[0,1,2,3,4,5], 'label': ['r', 'o', 'y', 'g', 'b', 'p']}, 'x':{'ticks': [0,1,2], 'label': None}}
actionSelection = loadCedarData(path=pathParser('ActionSelection'), col_names=None, dataType='2dfield', plotFormat=actionSelectionFormat)
actionSelection.data.iloc[:,0] = actionSelection.data.iloc[:,0].apply(correctTime)
actionSelection._field_size = [3,6]
actionSelSn = generateSnapShotSeries(actionSelection, snapShots)
#actionSelection._field_size = [6,3]

i=0
while i < len(snapShots):
	spMatchSnaps[i].pltPosition = (5,4,9+i)
	cMatchSnaps[i].pltPosition = (5,4,13+i)
	#actionSelSn[i].pltPosition = (5,4,13+i)
	images[i].pltPosition = (5,4,17+i)
	if i == 0:
		images[i].xyLabel={'x':None, 'y':'Camera', 'size':12}
		images[i]._label_pad = 15
	if i!= 0:
		spMatchSnaps[i].xyLabel={'x':'Horizontal Position', 'y':''}
		#actionSelSn[i].xyLabel={'x':None, 'y':''}
		cMatchSnaps[i].xyLabel={'x':None, 'y': ''}

	i += 1

figure_Data = {'int': intentionNode,
			   'sp2R': space2rate,
			   'spMatch1': spMatchSnaps[0],
			   'spMatch2': spMatchSnaps[1],
			   'spMatch3': spMatchSnaps[2],
			   'spMatch4': spMatchSnaps[3],
			   'img1': images[0],
			   'img2': images[1],
			   'img3': images[2],
			   'img4': images[3],
			   'actionSel1': cMatchSnaps[0],
			   'actionSel2': cMatchSnaps[1],
			   'actionSel3': cMatchSnaps[2],
			   'actionSel4': cMatchSnaps[3]
				}
figure_size = [200,180]
figure_format = {'title': "", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
