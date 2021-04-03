import re

hexColor = "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"


def validateColor(color):
    if re.match(hexColor, color):
        return True
    else:
        return False


class ShpViewerCtrl:

    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _connectSignals(self):
        self._view.buttons['selectFile'].clicked.connect(lambda: self._view.chooseFile())
        self._view.buttons['load'].clicked.connect(lambda: self._view.showMap())
        self._view.buttons['export'].clicked.connect(lambda: self._view.exportMap())
        self._view.buttons['settings'].clicked.connect(lambda: self._view.showMap(**self._createKwargs()))

    def _passFillingCol(self):
        color = self._view.colorLine.text()
        if not validateColor(color):
            color = self._view.map.filling
        return color

    def _passBoundariesCol(self):
        color = self._view.boundaryLine.text()
        if not validateColor(color):
            color = self._view.map.boundaries
        return color

    def _passTitle(self):
        return self._view.titleLine.text()

    def _passAxes(self):
        return self._view.axesYes.isChecked()

    def _passBasemap(self):
        basemap = str(self._view.basemap.currentText())
        return basemap

    def _passFilter(self):
        attribute = str(self._view.mapAttributes.currentText())
        condition = self._view.filterLine.text()
        if condition != "":
            filter = [attribute, condition]
            return filter
        else:
            return None

    def _createKwargs(self):
        kwargs = {}
        kwargs['filter'] = self._passFilter()
        kwargs['filling'] = self._passFillingCol()
        kwargs['boundaries'] = self._passBoundariesCol()
        kwargs['title'] = self._passTitle()
        kwargs['axes'] = self._passAxes()
        kwargs['basemap'] = self._passBasemap()
        return kwargs








