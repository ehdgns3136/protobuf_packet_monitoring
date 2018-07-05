import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

style.use('fivethirtyeight')

fig = plt.Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(1, 1, 1)

plot = ax.plot([1,2,3],[1,2,3])
for line in plot:
    ax.add_line(line)

# def animate(i):
#     graph_data = open('samplefile.txt', 'r').read()
#     lines = graph_data.split('\n')
#     xs = []
#     ys = []
#
#     for line in lines:
#         if len(line) > 1:
#             x, y = line.split(',')
#             xs.append(x)
#             ys.append(y)
#     ax.clear()
#     ax.plot(xs, ys)
#
# ani = animation.FuncAnimation(fig, animate, interval=1000)

canvas.draw()

plt.show()