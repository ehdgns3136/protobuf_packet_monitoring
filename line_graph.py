import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
np.random.seed(1)

x = np.random.rand(15)
y = np.random.rand(15)
names = np.array(list("ABCDEFGHIJKLMNO"))
c = np.random.randint(1,5,size=15)

norm = plt.Normalize(1,4)
cmap = plt.cm.RdYlGn

fig, ax = plt.subplots()
# fig = Figure()
# ax = fig.add_subplot(1, 1, 1)
# fig,ax = plt.subplots()
sc = plt.scatter(x,y,c=c, s=100, cmap=cmap, norm=norm)

annot = ax.annotate("hello", xy=(0,0), xytext=(0, -15), textcoords="offset points", bbox=dict(boxstyle="round", fc="black"), color="white", horizontalalignment="center")
ax.set_ylim(0, 2)

def update_annot(x):
    annot.xy = (x, 0)

vlines = None

def hover(event):
    global vlines
    if event.inaxes == ax:
        # print(event.xdata, event.ydata)
        ymin, ymax = ax.get_ylim()
        xmin, xmax = ax.get_xlim()

        if event.xdata > xmin and event.xdata < xmax:
            if vlines is None:
                vlines = ax.axvline(event.xdata, ymin, ymax)
            else:
                vlines.remove()
                vlines = ax.axvline(event.xdata, ymin, ymax)

        update_annot(event.xdata)
        annot.set_visible(True)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()