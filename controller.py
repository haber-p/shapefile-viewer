import re

class ShpViewerCtrl:

    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        self._view.buttons['selectFile'].clicked.connect(lambda: self._view.chooseFile())
        self._view.buttons['load'].clicked.connect(lambda: self._view.updateMap())
        self._view.buttons['export'].clicked.connect(lambda: self._view.exportMap())
        self._view.buttons['confirm'].clicked.connect(lambda: self._view.updateMap(filling=self.getFillingCol(), boundaries=self.getBoundariesCol(), title=self.getTitle(), axes=self.getAxes(), basemap=self.getBaseMap()))

    def getFillingCol(self):
        color = self._view.colorLine.text()
        if not validateColor(color):
            color = self._view.map.filling
        return color

    def getBoundariesCol(self):
        color = self._view.boundaryLine.text()
        if not validateColor(color):
            color = self._view.map.boundaries
        return color

    def getTitle(self):
        return self._view.titleLine.text()

    def getAxes(self):
        return self._view.axesYes.isChecked()

    def getBaseMap(self):
        basemap = str(self._view.basemap.currentText())
        if basemap is "None":
            basemap = None
        return basemap


hexColor = "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"


def validateColor(color):
    if re.match(hexColor, color):
        return True
    else:
        return False





