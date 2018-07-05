from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class MyCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 20, blit = True)

    def _draw_frame(self, framedata):
        graph_data = open('samplefile.txt', 'r').read()

        lines = graph_data.split('\n')
        xs = []
        ys = []

        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)
        self.ax.plot(xs, ys)

        for tick in self.ax.get_xticklabels():
            print(tick, end=" ")
        print()
        self.fig.canvas.draw()

        # print(self.ax.get_xticks())


    def new_frame_seq(self):
        return iter(range(4))



''' End Class '''