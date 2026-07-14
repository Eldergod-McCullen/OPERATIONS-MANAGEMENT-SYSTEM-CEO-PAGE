from PyQt6 import QtCore, QtWidgets

class VisitorsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Visitors_Page")
        self.setStyleSheet("background-color: #f0f2f5;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        lbl = QtWidgets.QLabel("VISITORS")
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("""
            color: #1e3a6e;
            font-size: 28px;
            font-weight: bold;
            font-family: 'Arial Black', sans-serif;
            letter-spacing: 2px;
        """)
        layout.addWidget(lbl)
