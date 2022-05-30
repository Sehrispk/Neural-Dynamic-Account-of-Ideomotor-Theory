from cProfile import label
from tracemalloc import Snapshot
import matplotlib.pyplot as plt
import numpy as np
from brokenaxes import brokenaxes
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as mcol
from matplotlib.gridspec import GridSpec

class PlotFigure:
    def __init__(self, plotData, size, format) -> None:
        self.size = size
        self.lineWidth = format['lineWidth']
        self.title = format['title']
        self.figure = plt.figure(figsize=(size[0]/25.4, size[1]/25.4))
        if self.title: self.figure.suptitle(self.title, fontsize=20)
        self.subaxes = {}
        self.artists = {}
        self.plotData = plotData

        for key, value in plotData.items():
                self.subaxes[key] = self.figure.add_subplot(value.pltPosition[0], value.pltPosition[1], value.pltPosition[2])

    def _plot_timeCourse(self, data, key):
        if not data._data_gap:
            self.subaxes[key].axhline(y=0, color='black', linestyle='-', linewidth=self.lineWidth)
            for col in data.data.columns[1:]:
                self.subaxes[key].plot(data.data.iloc[:,0].values,
                                        data.data[col].values, 
                                        label=col, 
                                        color=data.colors[col] if data.colors else 'r', 
                                        linewidth=self.lineWidth)
            if data.snapShotMarkers:
                for t in data.snapShotMarkers:
                    self.subaxes[key].vlines(t, 
                                        data.xyLimits['y'][0], 
                                        data.xyLimits['y'][1], 
                                        colors='grey', 
                                        linestyle='dotted', 
                                        alpha=1, 
                                        linewidth=self.lineWidth)

        elif data._data_gap:   
            self.figure.delaxes(self.subaxes[key])
            gs = GridSpec(data.pltPosition[0],data.pltPosition[1],figure=self.figure)
            self.subaxes[key] = brokenaxes(xlims=((data.xyLimits['x'][0], data._data_gap[0]), (data._data_gap[1], data.xyLimits['x'][1])), 
                                            subplot_spec=gs[data.pltPosition[2]-1,:], 
                                            wspace=0.1, 
                                            d=0)
            self.subaxes[key].axhline(y=0, color='black', linestyle='-', linewidth=self.lineWidth)

            for ax in self.subaxes[key].axs:
                interval = ax.get_xlim()
                if ax.get_subplotspec().is_first_row(): 
                    secx_ax = ax.secondary_xaxis("top", functions=(lambda x: x, lambda x: x))
                    secx_ax.xaxis.set_ticklabels([])
                    secx_ax.tick_params('both', direction='in', top=True)
                if ax.get_subplotspec().is_last_col():
                    secy_ax = ax.secondary_yaxis("right", functions=(lambda x: x, lambda x: x))
                    secy_ax.yaxis.set_ticklabels([])
                    secy_ax.tick_params('both', direction='in', right=True)
                
                if data.snapShotMarkers:
                    for t in data.snapShotMarkers:
                        if t > interval[0] and t < interval[1]:
                            ax.vlines(t, 
                                data.xyLimits['y'][0], 
                                data.xyLimits['y'][1], 
                                colors='grey', 
                                linestyle='dotted', 
                                alpha=1, 
                                linewidth=self.lineWidth)

            for col in data.data.columns[1:]:
                self.subaxes[key].plot(data.data.iloc[:,0].values,
                                    data.data[col].values,
                                    label=col,
                                    color=data.colors[col] if data.colors else 'r',
                                    linewidth=self.lineWidth)
            
        self.subaxes[key].legend(loc='lower left', ncol=3 if len(data.data.columns) > 4 else 1, fontsize=14)
        self.subaxes[key].tick_params('both', direction='in', top=True, right=True, labelsize=16)
        self.subaxes[key].set_xlim(data.xyLimits['x'] if not data._data_gap else None)
        self.subaxes[key].set_ylim(data.xyLimits['y'])

        self._set_label(data, key)
        self._set_ticks(data, key)

    def _plot_node_snapShot(self, data, key):
        """Internal function to plot snapshot of nodes at a specific point in time. Is called through PlotFigure.plot()."""
        labels = []
        ticks = []
        tick_pos = 0
        for col in data.data.columns[1:]:
            self.subaxes[key].plot(tick_pos, 
                                    data.data[col].values, 
                                    marker=".", 
                                    markersize=30,
                                    color=data.colors[col] if data.colors else 'r')
            labels += [col]
            ticks += [tick_pos]
            tick_pos += 0.5
        data.xyTicks['x'] = {'ticks': ticks, 'label': labels}

        self.subaxes[key].text(0.05, 0.95, "T={}s".format(round(data.data.iloc[:,0].values[0],1)), transform= self.subaxes[key].transAxes, fontsize=16, verticalalignment='top')
        self.subaxes[key].axhline(y=0, color='black', linestyle='-', linewidth=self.lineWidth)
        self.subaxes[key].tick_params('both', direction='in', top=True, right=True)
        self.subaxes[key].set_xlim([-0.2,len(ticks)/2-0.3])
        self.subaxes[key].set_ylim(data.xyLimits['y'])

        self._set_label(data, key)
        self._set_ticks(data, key)

    def _plot_image(self, data, key):
        """Internal plot function to show image of E-Puck camera. Is called through PlotFigure.plot() function."""
        image = data.data.iloc[:, 1:].values.reshape((52,39,3)).transpose([1,0,2])
        b, g, r = np.split(image, 3, axis=2)
        image = np.dstack((r,g,b))
        self.subaxes[key].imshow(image.astype(np.uint8))
        self.subaxes[key].set_xticks([])
        self.subaxes[key].set_yticks([])
        self.subaxes[key].text(0.05, 
                                0.95, 
                                "T={}s".format(round(data.data.iloc[:,0].values[0],1)), 
                                transform= self.subaxes[key].transAxes, 
                                fontsize=16,
                                verticalalignment='top')
                                
        self._set_label(data, key)

    def _plot_1d_field(self, data, key):
        """Internal function to plot snapshot of 1d-field. Is called through PlotFigure.plot()"""
        xRange = [x for x in range(data._field_dim[0], data._field_dim[1], int((data._field_dim[1]-data._field_dim[0])/len(list(data.data.iloc[:,1:].values[0]))))]
        plotData = list(data.data.iloc[:, 1:].values[0])
        if data.xyLabel['x'] == 'Color':
            xRange.insert(0, -1)
            xRange.append(21)
            plotData.insert(0, plotData[-1])
            plotData.append(plotData[1])
        self.subaxes[key].axhline(y=0, color='black', linestyle='-', linewidth=self.lineWidth)
        self.subaxes[key].plot(xRange, plotData, label=data.xyLabel['y'], color= 'r', linewidth=self.lineWidth)
        self.subaxes[key].text(0.05, 
                                0.95, 
                                "T={}s".format(round(data.data.iloc[:,0].values[0],1)), 
                                transform=self.subaxes[key].transAxes, 
                                fontsize=16,
                                verticalalignment='top')
        self.subaxes[key].tick_params('both', direction='in', top=True, right=True)
        #self.subaxes[key].set_xlim(data.xyLimits['x'])
        self.subaxes[key].set_ylim(data.xyLimits['y'])
        if data.xyLabel['x'] == 'Color':
            self.subaxes[key].set_xlim([0,21])

        self._set_label(data, key)
        self._set_ticks(data, key)

    def _plot_2d_field(self, data, key):
        """Internal function to plot snapshot of 2d-field. Is called through PlotFigure.plot()"""
        image = data.data.iloc[:, 1:].values.reshape((data._field_size[0],data._field_size[1]))
        image = image.T
        if data.xyLimits['y']:
            art = self.subaxes[key].imshow(image, cmap='jet', vmin=data.xyLimits['y'][0], vmax=data.xyLimits['y'][1])
        else:
            art = self.subaxes[key].imshow(image, cmap='jet')
        divider =  make_axes_locatable(self.subaxes[key])
        bar_axis = divider.append_axes("right", size="5%", pad=0.05)
        bar = plt.colorbar(art, cax=bar_axis)
        
        self.subaxes[key].text(0.05, 
                                1.2, 
                                "T={}s".format(round(data.data.iloc[:,0].values[0],1)), 
                                transform= self.subaxes[key].transAxes, 
                                fontsize=16,
                                verticalalignment='top',
                                color='black')

        self._set_label(data, key)
        self._set_ticks(data, key)

    def _set_ticks(self, data, key):
        if data.xyTicks['x'] != None:
            if data.xyTicks['x']['ticks'] != None and data.xyTicks['x']['label'] == None:
                self.subaxes[key].set_xticks(data.xyTicks['x']['ticks'], minor=False)
            elif data.xyTicks['x']['ticks'] == None and data.xyTicks['x']['label'] != None:
                self.subaxes[key].xaxis.set_ticklabels(data.xyTicks['x']['label'], fontsize=14)
            elif data.xyTicks['x']['ticks'] != None and data.xyTicks['x']['label'] != None:
                self.subaxes[key].set_xticks(data.xyTicks['x']['ticks'], labels=data.xyTicks['x']['label'], minor=False, fontsize=14)

        if data.xyTicks['y'] != None:
            if data.xyTicks['y']['ticks'] != None and data.xyTicks['y']['label'] == None:
                self.subaxes[key].set_yticks(data.xyTicks['y']['ticks'], minor=False)
            elif data.xyTicks['y']['ticks'] == None and data.xyTicks['y']['label'] != None:
                self.subaxes[key].yaxis.set_ticklabels(data.xyTicks['y']['label'])
            elif data.xyTicks['y']['ticks'] != None and data.xyTicks['y']['label'] != None:
                self.subaxes[key].set_yticks(data.xyTicks['y']['ticks'], labels=data.xyTicks['y']['label'], minor=False)

    def _set_label(self, data, key):
        if data.xyLabel['x'] != None:
            if data._data_gap:
                self.subaxes[key].set_xlabel(data.xyLabel['x'], fontsize=20,labelpad=20)
            else:
                self.subaxes[key].set_xlabel(data.xyLabel['x'], fontsize=20,labelpad=0)
        
        if data.xyLabel['y'] != None:
            if data._data_gap:
                self.subaxes[key].set_ylabel(data.xyLabel['y'], fontsize=20,labelpad=data._label_pad if data._label_pad else 30)
            else:
                self.subaxes[key].set_ylabel(data.xyLabel['y'], fontsize=20,labelpad=data._label_pad if data._label_pad else 5)

    def plot(self):
        for key in list(self.subaxes.keys()):
            if self.plotData[key].pltType  == 'timecourse':
                self._plot_timeCourse(self.plotData[key], key)
            elif self.plotData[key].pltType == 'snapshot' and self.plotData[key].dataType == 'node':
                self._plot_node_snapShot(self.plotData[key], key)
            elif self.plotData[key].pltType == 'snapshot' and self.plotData[key].dataType == 'image':
                self._plot_image(self.plotData[key], key)
            elif self.plotData[key].pltType == 'snapshot' and self.plotData[key].dataType == '1dfield':
                self._plot_1d_field(self.plotData[key], key)
            elif self.plotData[key].pltType == 'snapshot' and self.plotData[key].dataType == '2dfield':
                self._plot_2d_field(self.plotData[key], key)
            
        #plt.tight_layout()
