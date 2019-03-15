"""
PyQt imports
"""
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton, QLineEdit, QStackedLayout
from PyQt5.QtCore import QTimer, QThread, QEventLoop

"""
Local imports
"""
from widgets.Figure import Figure

class Watcher(QGroupBox):
    def __init__(self, name=""):
        super(Watcher, self).__init__(name)
        self.name = name

        self.stack = QStackedLayout()
        self.createInitialWidget()
        self.stack.addWidget(self.initial_widget)
        self.setLayout(self.stack)

        self.islive = True
        if(self.islive):
            self.update_delay = 200

    def createInitialWidget(self):
        self.initial_widget = QWidget()
        self.initial_layout = QVBoxLayout()
        self.topic_input = QLineEdit()
        self.b1 = QPushButton("Connect")
        self.b1.clicked.connect(self.connect)
        self.initial_layout.addWidget(self.topic_input)
        self.initial_layout.addWidget(self.b1)
        self.initial_widget.setLayout(self.initial_layout)

    def createActiveWidget(self, id):
            self.active_widget = QWidget()
            # Create Layout
            self.active_layout = QVBoxLayout()
            # Add canvas to the watcher
            self.figure = Figure(self.islive)
            # Add return button
            self.b2 = QPushButton("Disconnect")
            self.b2.clicked.connect(self.disconnect)
            self.active_layout.addWidget(self.b2)
            self.active_layout.addWidget(self.figure.canvas)
            self.active_widget.setLayout(self.active_layout)
            if(self.islive):
                self.activeThread = GraphUpdateTread(self.update_delay, self.figure)
                self.activeThread.start()

    def connect(self):
        if(self.topic_input.text() != ''):
            self.createActiveWidget(self.topic_input.text())
            self.stack.addWidget(self.active_widget)
            self.display(1)

    def disconnect(self):
        self.stack.removeWidget(self.active_widget)
        if(self.islive):
            self.activeThread.terminate()
        self.display(0)

    def display(self, i):
        self.stack.setCurrentIndex(i)

    def close(self):
        print("Closing Watcher", self)
        try:
            print("Closing ", self, self.activeThread, self.activeThread.isRunning())
            if(self.activeThread.isRunning()):
                self.activeThread.terminate()
            print("Closed ", self, self.activeThread, self.activeThread.isRunning())
        except AttributeError:
            print("Watcher", self, "has no active thread")


class GraphUpdateTread(QThread):
    def __init__(self, update_delay, target_figure):
        QThread.__init__(self)
        self.timer = QTimer()
        self.update_delay = update_delay
        self.timer.setInterval(self.update_delay)
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.process)

        self.target_figure = target_figure

    def run(self):
        self.timer.start()
        loop = QEventLoop()
        loop.exec_()

    def process(self):
        self.target_figure.update()
