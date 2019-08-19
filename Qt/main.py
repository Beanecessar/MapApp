from PyQt5.QtWidgets import QApplication
import sys
from ui.MapMainWindow import MapMainWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	MainWindow = MapMainWindow()
	MainWindow.show()
	sys.exit(app.exec_())