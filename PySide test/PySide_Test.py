import MaxPlus
import sqlite3
from pymxs import runtime as rt
from PySide.QtGui import *

class GCProtector(object):
    widgets = []

ui_form, ui_widget = MaxPlus.LoadUiType('test_ui.ui')
class mainWindow(ui_form, ui_widget):
	def __init__(self, parent=MaxPlus.GetQMaxWindow()):
		super(mainWindow, self).__init__(parent)
		self.setupUi(self)
		self.show()
		
		self.setWindowTitle('Widget')


if __name__ == '__main__':
	window = mainWindow()
	GCProtector.widgets.append(window)