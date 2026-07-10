from PyQt6.QtWidgets import QApplication
from CEO_FrontPage import CEOPage
import sys


app = QApplication(sys.argv)

window =  CEOPage()
window.show()

app.exec()