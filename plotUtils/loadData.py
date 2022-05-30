import time
from tracemalloc import Snapshot
from copy import deepcopy
import pandas as pd

class plotFormat:
    def __init__(self) -> None:
        """Wrapper for plotting options."""
        self.name = 'Plot' # name
        self.pltType = 'timecourse' # timecourse, snapshot
        self.pltPosition = (1, 1, 1) # (n_rows, n_cols, index)
        self.xyLimits = {'x':None,'y':None} # {'x': xlim, 'y': ylim}
        self.xyLabel = {'x':None,'y':None,'size':None} # {'x': 'x', 'y': 'y', 'size': size}
        self.xyTicks = {'x':None,'y':None} # {'x': [x1, x2, ...], 'y': [y1, y2, ...]}
        self.snapShotMarkers = None # [t0, t2, ...]
        self.colors = None # {'col1': '-r', ...}
    
    def copy(self):
        return deepcopy(self)

class Data:
    """Wrapper for cedar and webots data. For consistant formatting."""
    def __init__(self, data, dataType, plotFormat) -> None:
        self.plotFormat = plotFormat
        self.name = plotFormat.name
        self.pltType = plotFormat.pltType
        self.pltPosition = plotFormat.pltPosition
        self.xyLimits = plotFormat.xyLimits
        self.xyLabel = plotFormat.xyLabel
        self.xyTicks = plotFormat.xyTicks
        self.snapShotMarkers = plotFormat.snapShotMarkers
        self.colors = plotFormat.colors

        self.data = data
        self.dataType = dataType # nodes, field, image, webots

        self._data_gap = None
        self._field_dim = None
        self._field_size = None
        self._label_pad = None

    def _setPlotFormat(self):
        """Set plot format for data object.
            ::args:: 
                plotFormat: dictionary containing plotting options"""
        self.name = plotFormat.name
        self.pltType = plotFormat.pltType
        self.pltPosition = plotFormat.pltPosition
        self.xyLimits = plotFormat.xyLimits
        self.xyLabel = plotFormat.xyLabel
        self.xyTicks = plotFormat.xyTicks
        self.snapShotMarkers = plotFormat.snapShotMarkers
        self.colors = plotFormat.colors

    def appendData(self, DataObj):
        """Appends data from another Data Object. Old formatting 
        labels are ignored. Should be done before pruning etc.
        ::args::
            DataObj: instance of another Data object containing data to append (must be of the same dataType and same TimeWindow)"""
        if self.dataType == DataObj.dataType:
            for col in DataObj.data.columns:
                if col in self.data.columns and col != 'T':
                    self.data[col+'2'] = DataObj.data[col]
                else:
                    self.data[col] = DataObj.data[col]
        print(self.data.columns)

    def pruneData(self, timeWindow):
        """Prunes data to fit in specific timeWindow. plotType must be timeCourse and timeWinow must fit into recorded data.
            ::args::
                timeWindow: list or tuple containing t_min and t_may of time interval"""
        self.data = self.data.loc[self.data.iloc[:,0]>timeWindow[0]]
        self.data = self.data.loc[self.data.iloc[:,0]<timeWindow[1]]

    def cutTimeWidnow(self, timeWindow):
        """Cuts out data interval from data and glues separate parts back together. plotType must be timeCourse and timeWindow must fit into recorded data
            ::args::
                timeWindow: list or tuple containing t_min and t_may of time interval"""
                
        self.data = self.data.loc[((self.data['T']<timeWindow[0]) | (self.data['T']>timeWindow[1]))]
        self._data_gap = timeWindow

"""-------------------------------------------------------------------------------------------------------------------------------------"""

def loadCedarData(path, col_names, dataType, plotFormat):
    """loads cedar data from .csv file and transforms into neat format.
    ::args::
        path: path to .csv file
        plotFormat: plotting options
        col_names: naming of columns -> should start with T
        
    ::return::
        Data: Data object"""
    time_converter = lambda x: float(x.replace('s', ' '))
    df = pd.read_csv(path, names=col_names, skiprows=1, delimiter=',', converters={0: time_converter})
    data = Data(df, dataType, plotFormat)
    
    return data

def loadWebotsData(path, col_names, dataType, plotFormat):
    """loads webots data from .csv file and transforms into neat format.
    ::args::
        path: path to .csv file
        pltFormat: plotting options
        col_names: naming of columns -> should start with T
        
    ::return::
        Data: Data object"""
    sound_converter = lambda x: list(map(float, x[1:-1].split(',')))
    Hist_converter = lambda x: list(map(float, x[1:-1].split('.')[:-1]))
    goal_converter = lambda x: list(map(float, x[1:-1].split(',')))
    df = pd.read_csv(path, names=col_names, skiprows=1, delimiter='\t', converters={'sound': sound_converter, 'counter': Hist_converter, 'g': goal_converter})
    data = Data(df, dataType, plotFormat)

    return data

def generateSnapShotSeries(DataObj, snapShotTimePoints):
    """Generates a number of data objects of type snapshot, that contain data of specefied time points.
        ::args::
            DataObj: instance of DataObj to generate snapshots of.
            snapShotTimePoints: list of time points to define snapshots."""
    snapShotSeries = []
    for timePoint in snapShotTimePoints:
        beforeSnap = list(DataObj.data.loc[DataObj.data.iloc[:,0]<timePoint].iloc[:,0])
        afterSnap = list(DataObj.data.loc[DataObj.data.iloc[:,0]>timePoint].iloc[:,0])
        closestTime = beforeSnap[-1] if (timePoint-beforeSnap[-1]) < (afterSnap[0]-timePoint) else afterSnap[0]
        snapShotData = DataObj.data.loc[DataObj.data.iloc[:,0]==closestTime]

        snapShot = Data(snapShotData, DataObj.dataType, DataObj.plotFormat.copy())
        snapShot.pltType = 'snapshot'
        snapShot.snapShotMarkers = snapShotTimePoints
        snapShot._field_dim = DataObj._field_dim
        snapShot._field_size = DataObj._field_size

        snapShotSeries += [snapShot]
        
    return snapShotSeries
