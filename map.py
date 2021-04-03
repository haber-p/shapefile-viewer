import geopandas as gpd
import contextily as ctx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
matplotlib.use('Qt5Agg')


class ShpMap(FigureCanvasQTAgg):

    def __init__(self, data, **kwargs):
        self._setDefault()
        if kwargs:
            self._updateSettings(**kwargs)
        self.fig = self._generatePlot(data)
        super(ShpMap, self).__init__(self.fig)

    @classmethod
    def createMap(cls, path, **kwargs):
        cls.path = path
        cls.file = gpd.read_file(cls.path)
        cls.data = cls.file
        return cls(cls.data, **kwargs)

    @classmethod
    def createFilteredMap(cls, path, filter, **kwargs):
        cls.path = path
        column, value = filter[0], filter[1]
        cls.data = cls.file[cls.file[column] == value]
        return cls(cls.data, **kwargs)

    def _setDefault(self):
        self.filling = "#76d3e8"
        self.boundaries = "#aaaaaa"
        self.title = None
        self.axes = True
        self.basemap = "None"

    def _updateSettings(self, filling, boundaries, title, axes, basemap):
        self.filling = filling
        self.boundaries = boundaries
        self.title = title
        self.axes = axes
        self.basemap = basemap

    def _generatePlot(self, data):
        basemapTypes = {"LightGray": ctx.providers.Stamen.TonerLite,
                        "OpenStreetMap": ctx.providers.OpenStreetMap.Mapnik,
                        "Topographic": ctx.providers.OpenTopoMap}
        fig, ax = plt.subplots(1, 1)
        if self.basemap == "None":
            data.plot(ax=ax, legend=True, color=self.filling)
        else:
            data = data.to_crs(3857)
            data.plot(ax=ax, legend=True, color=self.filling, alpha=0.5)
            ctx.add_basemap(ax, source=basemapTypes[self.basemap])
        data.boundary.plot(ax=ax, color=self.boundaries)
        ax.set_title(self.title, fontsize=14, fontweight='bold')
        if self.axes == False:
            ax.set_axis_off()
        return fig

    def getAttributes(self):
        return self.file.columns

    def exportMap(self):
        self._generatePlot()
        plt.savefig('yourMap.png')
