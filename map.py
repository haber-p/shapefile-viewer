import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import contextily as ctx
matplotlib.use('Qt5Agg')


class ShpMap(FigureCanvasQTAgg):

    def __init__(self, path, **kwargs):
        self.path = path
        self._setDefault()
        if kwargs:
            self.updateAttributes(**kwargs)
        fig = self._generatePlot()
        super(ShpMap, self).__init__(fig)

    def _setDefault(self):
        self.filling = "#f4a4a4"
        self.boundaries = "#aaaaaa"
        self.title = None
        self.axes = True
        self.basemap = 'None'

    def _generatePlot(self):
        basemapTypes = {"LightGray": ctx.providers.Stamen.TonerLite,
                        "OpenStreetMap": ctx.providers.OpenStreetMap.Mapnik,
                        "Topographic": ctx.providers.OpenTopoMap}
        self.file = gpd.read_file(self.path)
        fig, ax = plt.subplots(1, 1)
        if self.basemap == None or self.basemap == 'None':
            self.file.plot(ax=ax, legend=True, color=self.filling)
            self.file.boundary.plot(ax=ax, color=self.boundaries)
        else:
            self.file = self.file.to_crs(3857)
            self.file.plot(ax=ax, legend=True, color=self.filling, alpha=0.5)
            self.file.boundary.plot(ax=ax, color=self.boundaries)
            ctx.add_basemap(ax, source=basemapTypes[self.basemap])
        ax.set_title(self.title, fontsize=14, fontweight='bold')
        if self.axes == False:
            ax.set_axis_off()
        return fig

    def updateAttributes(self, filling, boundaries, title, axes, basemap):
        self.filling = filling
        self.boundaries = boundaries
        self.title = title
        self.axes = axes
        self.basemap = basemap

    def exportMap(self):
        self._generatePlot()
        plt.savefig('yourMap.png')





    """def __init__(self, path, filling="#f4a4a4", boundaries="#ffffff", title=None, axes=True, basemap="None"):
        self.file = gpd.read_file(path)
        if basemap == "None":
            fig, ax = plt.subplots(1,1)
            self.file.plot(ax=ax, legend=True, color=filling)
            self.file.boundary.plot(ax=ax, color=boundaries)
            ax.set_title(title, fontsize=14, fontweight='bold')
        else:
            basemapTypes = {"LightGray": ctx.providers.Stamen.TonerLite, "OpenStreetMap": ctx.providers.OpenStreetMap.Mapnik, "Topographic": ctx.providers.OpenTopoMap}
            fig, ax = plt.subplots(1, 1)
            self.file = self.file.to_crs(3857)
            self.file.plot(ax=ax, legend=True, color=filling, alpha=0.5)
            self.file.boundary.plot(ax=ax, color=boundaries)
            ctx.add_basemap(ax, source=basemapTypes[basemap])
            ax.set_title(title, fontsize=14, fontweight='bold')
        if axes==False:
            ax.set_axis_off()

        super(ShpMap, self).__init__(fig)"""






