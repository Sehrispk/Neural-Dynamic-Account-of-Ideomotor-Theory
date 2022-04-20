from ast import Constant
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
plotInterval = [778.75,780.1]
#cutInterval  = [505, 575]
snapShots = [779,779.5,780.0]

"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""
soundPerception = loadCedarData(path=pathParser('SoundPerception'), col_names=['T', 'S1', 'S2', 'S3'], dataType='nodes', plotFormat=baseFormat.copy())
soundWebots = loadWebotsData(path=pathParser('events'), col_names=None, dataType='webots', plotFormat=baseFormat.copy())
correctTime = correctTimeOffSet(soundPerception.data, soundWebots.data[['T', 'sound']])
"""-----------------------------------------timeCorrection---------------------------------------------------------------------------------"""

colorConceptFormat = baseFormat.copy()
colorConceptFormat.name = 'ColorConcepts' # name
colorConceptFormat.pltType = 'timecourse' # timecourse, snapshot
colorConceptFormat.pltPosition = (6, 1, 1) # (n_rows, n_cols, index)
colorConceptFormat.xyLimits = {'x':plotInterval,'y':[-1,1]} # {'x': xlim, 'y': ylim}
colorConceptFormat.xyLabel = {'x':'Time [s]','y':'Color Concepts','size':12} # {'x': 'x', 'y': 'y', 'size': size}
colorConceptFormat.snapShotMarkers = snapShots
colorConceptFormat.colors = {'red':'red', 'orange': 'orange', 'yellow':'yellow', 'green': 'green', 'blue': 'blue', 'violet': 'violet'} # {'col1': '-r', ...}

spaceAttentionFormat = baseFormat.copy()
spaceAttentionFormat.name = 'Space Attention' # name
spaceAttentionFormat.pltType = 'timecourse' # timecourse, snapshot
spaceAttentionFormat.pltPosition = (6, 1, 2) # (n_rows, n_cols, index)
spaceAttentionFormat.xyLimits = {'x':plotInterval,'y':[-1,1]} # {'x': xlim, 'y': ylim}
spaceAttentionFormat.xyLabel = {'x':'Horizontal Position','y':'Space Attention','size':12} # {'x': 'x', 'y': 'y', 'size': size}
spaceAttentionFormat.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
spaceAttentionFormat.snapShotMarkers = None # [t0, t2, ...]
spaceAttentionFormat.colors = 'red' # {'col1': '-r', ...}

colorSpaceAttentionF = baseFormat.copy()
colorSpaceAttentionF.name = 'Color Space Attention' # name
colorSpaceAttentionF.pltType = 'timecourse' # timecourse, snapshot
colorSpaceAttentionF.pltPosition = (6, 1, 3) # (n_rows, n_cols, index)
colorSpaceAttentionF.xyLimits = {'x':plotInterval,'y':[-1.75,0.25]} # {'x': xlim, 'y': ylim}
colorSpaceAttentionF.xyLabel = {'x':'Horizontal Position','y':'Color/Space\nAttention','size':12} # {'x': 'x', 'y': 'y', 'size': size}
colorSpaceAttentionF.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
colorSpaceAttentionF.snapShotMarkers = None # [t0, t2, ...]
colorSpaceAttentionF.colors = None # {'col1': '-r', ...}

colorAttentionFormat = baseFormat.copy()
colorAttentionFormat.name = 'Color Space Attention' # name
colorAttentionFormat.pltType = 'timecourse' # timecourse, snapshot
colorAttentionFormat.pltPosition = (6, 1, 3) # (n_rows, n_cols, index)
colorAttentionFormat.xyLimits = {'x':plotInterval,'y':[-4,1]} # {'x': xlim, 'y': ylim}
colorAttentionFormat.xyLabel = {'x':'Color','y':'Color Attention','size':12} # {'x': 'x', 'y': 'y', 'size': size}
colorAttentionFormat.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
colorAttentionFormat.snapShotMarkers = None # [t0, t2, ...]
colorAttentionFormat.colors = None # {'col1': '-r', ...}

ColorSpacePerceptionF = baseFormat.copy()
ColorSpacePerceptionF.name = 'Color Space Perception' # name
ColorSpacePerceptionF.pltType = 'timecourse' # timecourse, snapshot
ColorSpacePerceptionF.pltPosition = (6, 1, 4) # (n_rows, n_cols, index)
ColorSpacePerceptionF.xyLimits = {'x':plotInterval,'y':[-5,0.25]} # {'x': xlim, 'y': ylim}
ColorSpacePerceptionF.xyLabel = {'x':'Horizontal Position','y':'Color/Space\nPerception','size':12} # {'x': 'x', 'y': 'y', 'size': size}
ColorSpacePerceptionF.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
ColorSpacePerceptionF.snapShotMarkers = None # [t0, t2, ...]
ColorSpacePerceptionF.colors = None # {'col1': '-r', ...}

cameraFormat = baseFormat.copy()
cameraFormat.name = 'Camera' # name
cameraFormat.pltType = 'timecourse' # timecourse, snapshot
cameraFormat.pltPosition = (6, 1, 4) # (n_rows, n_cols, index)
cameraFormat.xyLimits = {'x':plotInterval,'y':None} # {'x': xlim, 'y': ylim}
cameraFormat.xyLabel = {'x':None,'y':None,'size':None} # {'x': 'x', 'y': 'y', 'size': size}
cameraFormat.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
cameraFormat.snapShotMarkers = None # [t0, t2, ...]
cameraFormat.colors = None # {'col1': '-r', ...}

colorConcept = loadCedarData(path=pathParser('ColorConcepts'), col_names=['T', 'red', 'orange', 'yellow', 'green', 'blue', 'violet'], dataType='node', plotFormat=colorConceptFormat)
spaceAttention = loadCedarData(path=pathParser('SpaceAttention'), col_names=None, dataType='1dfield', plotFormat=spaceAttentionFormat)
colorSpaceAttention = loadCedarData(path=pathParser('ColorSpaceAttention'), col_names=None, dataType='2dfield', plotFormat=colorSpaceAttentionF)
colorAttention = loadCedarData(path=pathParser('ColorAttention'), col_names=None, dataType='1dfield', plotFormat=colorAttentionFormat)
ColorSpacePerception = loadCedarData(path=pathParser('ColorSpacePerception'), col_names=None, dataType='2dfield', plotFormat=ColorSpacePerceptionF)
camera = loadCedarData(path=pathParser('CameraImage'), col_names=None, dataType='image', plotFormat=cameraFormat)

ColorSpacePerception._field_size=[52,20]
colorSpaceAttention._field_size=[52,20]
spaceAttention._field_dim = [0,52]
colorAttention._field_dim = [0,20]

colorConcept.data.iloc[:,0] = colorConcept.data.iloc[:,0].apply(correctTime)
spaceAttention.data.iloc[:,0] = spaceAttention.data.iloc[:,0].apply(correctTime)
colorSpaceAttention.data.iloc[:,0] = colorSpaceAttention.data.iloc[:,0].apply(correctTime)
colorAttention.data.iloc[:,0] = colorAttention.data.iloc[:,0].apply(correctTime)
ColorSpacePerception.data.iloc[:,0] = ColorSpacePerception.data.iloc[:,0].apply(correctTime)
camera.data.iloc[:,0] = camera.data.iloc[:,0].apply(correctTime)

colorConcept.pruneData(plotInterval)
spaceAttention.pruneData(plotInterval)
colorSpaceAttention.pruneData(plotInterval)
colorAttention.pruneData(plotInterval)
ColorSpacePerception.pruneData(plotInterval)
camera.pruneData(plotInterval)

images = generateSnapShotSeries(camera, snapShots)
images[0].xyLabel={'x':None, 'y':'Camera', 'size':12}
ColSpPercSn = generateSnapShotSeries(ColorSpacePerception, snapShots)
ColSpAtSn = generateSnapShotSeries(colorSpaceAttention, snapShots)
SpAtSn = generateSnapShotSeries(spaceAttention, snapShots)
CoAtSn = generateSnapShotSeries(colorAttention, snapShots)

i=0
while i < len(snapShots):
	SpAtSn[i].pltPosition = (6,3,7+i)
	ColSpAtSn[i].pltPosition = (6,3,10+i)
	CoAtSn[i].pltPosition = (6,3,4+i)
	ColSpPercSn[i].pltPosition = (6,3,13+i)
	images[i].pltPosition = (6,3,16+i)
	if i > 0:
		ColSpPercSn[i].xyLabel['y'] = ''
		ColSpPercSn[i].xyTicks['y'] = {'ticks':None, 'label':[]}
		ColSpAtSn[i].xyLabel['y'] = ''
		ColSpAtSn[i].xyTicks['y'] = {'ticks':None, 'label':[]}
		CoAtSn[i].xyLabel['y'] = ''
		CoAtSn[i].xyTicks['y'] = {'ticks':None, 'label':[]}
		SpAtSn[i].xyLabel['y'] = ''
		SpAtSn[i].xyTicks['y'] = {'ticks':None, 'label':[]}
	elif i == 0:
		images[i]._label_pad = 35
		CoAtSn[i]._label_pad = 15
		#goalSnapshots[i]._label_pad = -0.05
		#actionSelectionSnapshots[i]._label_pad = 25
	i += 1

figure_Data = {'ColorConcepts': colorConcept,
			   'img1': images[0],
			   'img2': images[1],
			   'img3': images[2],
			   'CoP1': ColSpPercSn[0],
			   'CoP2': ColSpPercSn[1],
			   'CoP3': ColSpPercSn[2],
			   'CAS1': CoAtSn[0],
			   'CAS2': CoAtSn[1],
			   'CAS3': CoAtSn[2],
			   'SAS1': SpAtSn[0],
			   'SAS2': SpAtSn[1],
			   'SAS3': SpAtSn[2],
			   'CSAS1': ColSpAtSn[0],
			   'CSAS2': ColSpAtSn[1],
			   'CSAS3': ColSpAtSn[2],
			   }
figure_size = [200,180]
figure_format = {'title': "Visual Perception", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
