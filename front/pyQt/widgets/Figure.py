import matplotlib.pyplot as plt
import random
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Figure():
    def __init__(self, islive=False):
        self.figure = plt.figure(figsize=(15,5))
        self.figure.set_facecolor('0.915')
        self.canvas = FigureCanvas(self.figure)
        self.x = [1, 2, 3, 4, 5, 6]
        self.y = [random.random() for i in range(6)]
        self.plot()

    def plot(self):
        """  """
        # Create Figure
        self.figure.clf()
        self.axes = self.figure.add_subplot(111)
        self.line, = self.axes.plot(self.x, self.y)
        # Set Color
        self.axes.set_facecolor('0.915')
        # Draw Graph
        self.canvas.draw()
    
    def update(self):
        self.y = [random.random() for i in range(6)]
        self.line.set_ydata(self.y)
        self.canvas.draw()
        self.canvas.flush_events()

