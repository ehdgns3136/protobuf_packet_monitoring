from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import time
from PyQt5.QtWidgets import *
import sys
import numpy as np
import matplotlib.pyplot as plt



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 400, 400)
        graph = Graph()
        layout = QHBoxLayout()
        layout.addWidget(graph)
        self.setLayout(layout)


class Graph(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ydatas = []
        self.xdatas = []
        self.build_data()
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=1000, blit=True)

    def build_data(self):
        self.xdatas = []
        self.ydatas = []
        for i in range(0, 10000, 1000):
            self.xdatas.append(i)

        for i in range(10):
            ydata = []
            for j in range(10):
                ydata.append(random.randrange(0, 10000))
            self.ydatas.append(ydata)

        self.time_annot = self.ax.annotate("hello", xy=(0, 0), xytext=(0, 0),
                                           textcoords="offset points",
                                           bbox=dict(boxstyle="round", fc="black"), color="white",
                                           horizontalalignment="center", fontsize=8)


    def _draw_frame(self, framedata):
        saved_time = time.time()
        self.ax.clear()
        lines = []
        self.ax.grid(color='#d0d0d0', linestyle='-', linewidth=0.5)

        self.ax.plot(self.xdatas, self.ydatas[0])
        # for ydata in self.ydatas:
        #     lines.extend(self.ax.plot(self.xdatas, ydata))

        # self.ax.set
        # print(np.arange(5))

        print(self.ax.get_xticks()[0])
        print(self.ax.get_xticks()[len(self.ax.get_xticks())-1])

        self.ax.set_xticks([-2000, 0, 2000, 4000, 6000, 8000])
        self.ax.set_xticklabels(['a','b','c','d','e', 'f'])
        # # xticks(np.arange(5), ('Tom', 'Dick', 'Harry', 'Sally', 'Sue'))
        #
        for tick in self.ax.get_xticklabels():
            print(tick)

        # print(self.ax.get_xticks())

        self.fig.canvas.draw_idle()
        self.build_data()
        print(time.time()-saved_time)

    # def _post_draw(self, framedata, blit):
    #     super()._post_draw(framedata, blit)
    #     saved_time = time.time()
    #     print(self.ax.get_xticks())
    #     self.ax.set_xticklabels(self.xdatas)
    #     print('post draw: ', time.time()-saved_time)


    def new_frame_seq(self):
        return iter(range(len(self.xdatas)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
