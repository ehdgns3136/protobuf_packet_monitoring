import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
np.random.seed(1)

x = np.random.rand(15)
y = np.random.rand(15)
names = np.array(list("ABCDEFGHIJKLMNO"))
c = np.random.randint(1,5,size=15)

norm = plt.Normalize(1,4)
cmap = plt.cm.RdYlGn

fig,ax = plt.subplots()
sc = plt.scatter(x,y,c=c, s=100, cmap=cmap, norm=norm)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

isPress = False
pressPos = (0, 0)
releasePos = (0, 0)

def hover(event):
    if isPress:
        ymin, ymax = ax.get_ylim()
        if event.xdata > pressPos[0]:
            start = pressPos[0]
            end = event.xdata
            ax.add_patch(patches.Rectangle((start, ymin), start-end, ymax-ymin))
            fig.canvas.draw_idle()
        else:
            start = event.xdata
            end = pressPos[0]
            ax.add_patch(patches.Rectangle((start, ymin), start - end, ymax - ymin))
            fig.canvas.draw_idle()


def press(event):
    global isPress, pressPos
    isPress = True
    pressPos = (event.xdata, event.ydata)


def release(event):
    global isPress, releasePos
    isPress = False
    releasePos = (event.xdata, event.ydata)


fig.canvas.mpl_connect("motion_notify_event", hover)
fig.canvas.mpl_connect("button_press_event", press)
fig.canvas.mpl_connect("button_release_event", release)

plt.show()