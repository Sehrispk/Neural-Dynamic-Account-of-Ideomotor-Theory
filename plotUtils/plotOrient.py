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
images[0].xyLabel={'x':None, 'y':'Camera', 'size':12}

i=0
while i < len(snapShots):
	images[i].pltPosition = (6,3,16+i)
	if i == 0:
		images[i]._label_pad = 35
	i += 1

figure_Data = {'img1': images[0],
			   'img2': images[1],
			   'img3': images[2],
				}
figure_size = [200,180]
figure_format = {'title': "Visual Perception", 
				 'lineWidth': 2}
figure = PlotFigure(figure_Data, figure_size, figure_format)
figure.plot()
plt.show()
