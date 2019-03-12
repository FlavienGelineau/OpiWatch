"""
Useful imports
"""
import sys, os


"""
PyQt imports
"""
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

"""
Local imports
"""
from widgets.Watcher import Watcher

class App(QWidget):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        self.setWindowTitle("Opiwatch")
        QApplication.setStyle("Fusion")

        self.mainLayout = QGridLayout()

        # Label and Logo
        self.label = QLabel(self)
        self.label.setText('test')
        self.label.move(20, 0)

        # Watchers
        self.line_size = 2
        self.watchers = []
        self.watchers.extend([Watcher() for i in range(3)])
        for i, watcher in enumerate(self.watchers):
            line = i // self.line_size
            column = i % self.line_size
            watcher.setFixedHeight(300)
            watcher.setFixedWidth(400)
            self.mainLayout.addWidget(watcher, column, line)
        
        self.setLayout(self.mainLayout)

    def closeEvent(self, event):
        """
        All active watchers are stopped on closing.
        """
        print("Exit...")
        for watcher in self.watchers:
            watcher.close()
        print("Ready to exit.")
        event.accept()



if __name__ == "__main__":

    # Instanciate the app
    app = QApplication([])
    mainWindow = App()

    # Center the main window on the screen
    screenGeometry = QApplication.desktop().screenGeometry()
    x = (screenGeometry.width() - mainWindow.width()) / 2
    y = (screenGeometry.height() - mainWindow.height()) / 2
    mainWindow.move(x, y)

    # Display app
    mainWindow.show()

    # Give control back to the user
    app.exec()
    print("out")
    sys.exit(app.exec_())