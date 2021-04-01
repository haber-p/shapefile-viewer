from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from map import *


class ShpViewerUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # set general window properties
        self.setWindowTitle("Shapefile Viewer")
        self.setGeometry(400, 100, 1100, 900)
        # set central widget and layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget()
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)
        # add elements
        self._addButtons()
        self._createFileLoader()
        self._createStatusBar()
        self._createMapManager()

    def _addButtons(self):
        self.buttons = {
            'selectFile': QPushButton('...'),
            'load': QPushButton('Load'),
            'export': QPushButton('Export'),
            'filter': QPushButton('Filter')
        }

    def _createFileLoader(self):
        layout = QGridLayout()
        self.pathLine = QLineEdit()
        self.pathLine.setReadOnly(True)
        layout.addWidget(self.pathLine,0, 0, 1, 7)
        layout.addWidget(self.buttons['selectFile'], 0, 7)
        layout.addWidget(self.buttons['load'], 1, 0)
        layout.addWidget(self.buttons['export'], 1, 1)
        self.generalLayout.addLayout(layout)

    def _createMapManager(self):
        # create options layout
        self.titleLine = QLineEdit()
        self.titleLine.setFixedSize(150, 25)
        self.colorLine = QLineEdit()
        self.colorLine.setFixedSize(150, 25)
        self.boundaryLine = QLineEdit()
        self.boundaryLine.setFixedSize(150, 25)
        self.axesYes = QRadioButton("Yes")
        self.axesYes.setChecked(True)
        self.axesNo = QRadioButton("No")
        self.basemap = QComboBox()
        basemaps = ("None", "LightGray", "OpenStreetMap", "Topographic")
        self.basemap.addItems(basemaps)
        optionsLayout = QVBoxLayout()
        optionsLayout.setAlignment(Qt.AlignTop)
        optionsLayout.addWidget((QLabel("Title:")))
        optionsLayout.addWidget(self.titleLine)
        optionsLayout.addWidget((QLabel("Map color:")))
        optionsLayout.addWidget(self.colorLine)
        optionsLayout.addWidget((QLabel("Boundaries color:")))
        optionsLayout.addWidget(self.boundaryLine)
        optionsLayout.addWidget((QLabel("Display axes:")))
        optionsLayout.addWidget(self.axesYes)
        optionsLayout.addWidget(self.axesNo)
        optionsLayout.addWidget((QLabel("Base map:")))
        optionsLayout.addWidget(self.basemap)

        self.mapAttributes = QComboBox()
        optionsLayout.addWidget(QLabel("Filter by attribute:"))
        optionsLayout.addWidget(self.mapAttributes)
        optionsLayout.addWidget((QLabel("Condition:")))
        self.filterLine = QLineEdit()
        self.filterLine.setFixedSize(150, 25)
        optionsLayout.addWidget(self.filterLine)
        optionsLayout.addWidget(self.buttons['filter'])

        self.managerLayout = QHBoxLayout()
        self.managerLayout.addLayout(optionsLayout)

        # display map
        try:
            self.map = ShpMap(self.path)
        except:
            self.map = QWidget()
        finally:
            self.managerLayout.addWidget(self.map)

        self.managerLayout.setAlignment(Qt.AlignLeft)
        self.generalLayout.addLayout(self.managerLayout)

    def _createStatusBar(self):
        status = QStatusBar()
        status.setStyleSheet("background-color : #cccccc")
        self.setStatusBar(status)

    def _setPath(self, path):
        self.path = path
        self.pathLine.setText(path)

    def chooseFile(self):
        fileName,filter = QFileDialog.getOpenFileName(self, filter="(*.shp)")
        self._setPath(fileName)
        print(self.path)

    def updateMap(self, filter=None, **kwargs):
        if hasattr(self, "path"):
            self.statusBar().showMessage("Map updating... Please wait")
            if filter:
                newMap = ShpMap.filterMap(self.path, filter=filter, **kwargs)
            else:
                newMap = ShpMap.createNew(self.path, **kwargs)
            self.managerLayout.replaceWidget(self.map, newMap)
            self.map = newMap
            self.statusBar().showMessage("Map updated successfully", 3000)
            attributes = self.map.getColNames()
            self.mapAttributes.clear()
            self.mapAttributes.addItems(attributes)
        else:
            self.statusBar().showMessage("Choose a file first")

    def changeColors(self, **kwargs):
        newMap = self.map.update(**kwargs)
        self.managerLayout.replaceWidget(self.map, newMap)
        self.map = newMap

    def exportMap(self):
        if hasattr(self,"path"):
            self.map.exportMap()
        else:
            self.statusBar().showMessage("Choose a file first")
