import numpy as np
from matplotlib import pyplot

from Plot import Plot

class Plotter(object):
    plots = []

    def __init__(self, num_columns, num_clusters):
        self.color_map = pyplot.cm.get_cmap('hsv', num_clusters + 1)
        self.num_columns = num_columns
        pyplot.close('all')

    def addPlot(self, plot):
        self.plots.append(plot)

    def show(self):
        self.num_plots = len(self.plots)
        self.num_rows = self.calcRowNumber(plot_number=self.num_plots, num_subplots_per_row=self.num_columns)

        self.figure, axes = pyplot.subplots(nrows=self.num_rows, ncols=self.num_columns, sharex='col', sharey='row')
        for axis, plot in zip(axes.flat, self.plots):
            num_clusters = len(plot.clusters)
            axis.set_title(plot.label)
            colors = map(lambda color_num: self.color_map(color_num), range(num_clusters))
            for cluster, color in zip(plot.clusters, colors):
                x = cluster.getXValues()
                y = cluster.getYValues()
                axis.scatter(x, y, color=color)
                axis.plot(cluster.centroid.x, cluster.centroid.y, 'x', color=color)
                print('label: ', plot.label, ' cluster id_num: ', cluster.id_num, ' centroid: ', cluster.centroid, ' color: ', color)
        self.figure.subplots_adjust(wspace=0.5, hspace=0.5)
        pyplot.show()

    def calcRowNumber(self, plot_number, num_subplots_per_row):
        return (plot_number - 1) // num_subplots_per_row + 1

    def calcColumnNumber(self, plot_number, num_subplots_per_row):
        return (plot_number - 1) % num_subplots_per_row + 1

