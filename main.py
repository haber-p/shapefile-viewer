import sys
from PyQt5.QtWidgets import QApplication
from ui import ShpViewerUI
from controller import ShpViewerCtrl

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ShpViewerUI()
    view.show()
    ShpViewerCtrl(view=view)
    sys.exit(app.exec())




