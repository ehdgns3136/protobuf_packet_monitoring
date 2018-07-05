from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

class Graph(FigureCanvas, TimedAnimation):
    def __init__(self, packets_info, graph_press_callback):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ydatas = {}
        self.xdatas = []
        self.unit = 1
        self.current_mouse_area = "out" # 'out', 'figure', 'axes'
        self.vline = None
        self.time_annot = None
        self.drawed_time = 0
        self.is_record = True
        self.packets_info = packets_info
        self.force_draw = False
        self.graph_press_callback = graph_press_callback
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=1000, blit=True)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        self.fig.canvas.mpl_connect("button_press_event", self.press)
        self.fig.canvas.mpl_connect("figure_enter_event", self.figure_enter)
        self.fig.canvas.mpl_connect("figure_leave_event", self.figure_leave)
        self.fig.canvas.mpl_connect("axes_enter_event", self.axes_enter)
        self.fig.canvas.mpl_connect("axes_leave_event", self.axes_leave)

    def figure_enter(self, event):
        self.current_mouse_area = "figure"

    def figure_leave(self, event):
        self.current_mouse_area = "out"

    def axes_enter(self, event):
        self.current_mouse_area = "axes"

    def axes_leave(self, event):
        self.current_mouse_area = "figure"

    def press(self, event):
        if self.current_mouse_area == "axes" and event.xdata < 100 and event.xdata >= 0:
            xtick_labels = self.ax.get_xticklabels()
            xtick_data = xtick_labels[len(xtick_labels) - 1]
            if ':' not in xtick_data.get_text():
                return

            hour, minute, second = xtick_data.get_text().split(':')
            hovered_time = datetime.datetime.now()
            hovered_time = hovered_time.replace(hour=int(hour), minute=int(minute), second=int(second))
            hovered_time = hovered_time.timestamp()
            mouse_pos_x = int(round(event.xdata))
            xtick_x = xtick_data.get_position()[0]

            hovered_time += self.unit * (mouse_pos_x - xtick_x)

            self.graph_press_callback(int(hovered_time))


    def _draw_frame(self, framedata):
        if self.is_record or self.force_draw:
            self.ax.clear()
            for packet_id in self.ydatas.keys():
                if packet_id in self.selected_packets:
                    self.ax.plot(self.xdatas, self.ydatas[packet_id], color=self.packets_info[packet_id]["color"])
            self.ax.grid(color='#d0d0d0', linestyle='-', linewidth=0.5)

        if self.vline is not None:
            if self.current_mouse_area == "axes":
                self.vline.set_visible(True)
                self.ax.add_line(self.vline)
            else:
                self.vline.set_visible(False)

        if self.time_annot is not None:
            if self.current_mouse_area == "axes":
                self.time_annot.set_visible(True)
                self.ax._add_text(self.time_annot)
            else:
                self.time_annot.set_visible(False)

        self.fig.canvas.draw()

        if len(self.xdatas) > 0 and self.is_record or self.force_draw:
            unit = self.unit
            if unit == 1 or unit == 30 or unit == 60:
                # set visible xtick per unit*10
                xtick_unit = unit * 10
            elif unit == 5 or unit == 10 or unit == 600 or unit == 1800 or unit == 3600:
                # set visible xtick per unit*12
                xtick_unit = unit * 12
            else:
                xtick_unit = 10

            xticks = self.ax.get_xticks()
            xtick_labels = self.ax.get_xticklabels()

            is_unit_time = False
            new_xticks = []
            new_xtick_labels = []

            if self.force_draw:
                for i in range(len(xticks)-1, -1, -1):
                    xtick = int(xtick_labels[i].get_text())
                    xtick -= xtick % unit

                    if xtick % xtick_unit == 0:
                        new_xticks.insert(0, xticks[i])
            else:
                for i in range(len(xticks)-1, -1, -1):
                    xtick = int(xtick_labels[i].get_text())
                    if xtick % xtick_unit == 0:
                        new_xticks.insert(0, xticks[i])
                        is_unit_time = True
                if not is_unit_time:
                    self.ax.set_xticks(self.saved_xticks)
                    self.ax.set_xticklabels(self.saved_xtick_labels)
                    return

            for i in new_xticks:
                tick_time = datetime.datetime.fromtimestamp(int(xtick_labels[i].get_text()))
                new_xtick_labels.append("%02d:%02d:%02d" % (tick_time.hour, tick_time.minute, tick_time.second))

            self.ax.set_xticks(new_xticks)
            self.ax.set_xticklabels(new_xtick_labels)
            self.saved_xticks = new_xticks
            self.saved_xtick_labels = new_xtick_labels
            if self.force_draw:
                self.force_draw = False

    def new_frame_seq(self):
        if len(self.xdatas) > 0:
            return iter(range(len(self.xdatas)))
        else:
            return iter(range(1000))

    def update_packet_data(self, packets, unit, selected_packets, now, force_draw):
        self.selected_packets = selected_packets

        if self.is_record:
            count = 0
            if (len(self.xdatas) > 0 and self.xdatas[len(self.xdatas)-1] != now) or (len(self.xdatas) == 0):
                xdatas = [] # same for all
                time = now

                while count < 100:
                    xdatas.insert(0, str(time))
                    time -= unit
                    count += 1
                self.xdatas = xdatas

            ydatas = {}
            for packet_id in selected_packets:
                if packet_id in packets.keys():
                    count = 0
                    ydata = []
                    while count < 100:
                        size = 0
                        for i in range(now-count*unit, now-(count+1)*unit, -1):
                            if i in packets[packet_id]:
                                size += packets[packet_id][i]
                        ydata.insert(0, size)
                        count += 1
                    ydatas.update({
                        packet_id: ydata
                    })

            self.ydatas = ydatas
        elif force_draw:
            count = 0

            xdatas = []  # same for all
            now = time = int(self.xdatas[len(self.xdatas)-1])

            while count < 100:
                xdatas.insert(0, str(time))
                time -= unit
                count += 1
            self.xdatas = xdatas

            ydatas = {}
            for packet_id in selected_packets:
                if packet_id in packets.keys():
                    count = 0
                    ydata = []
                    while count < 100:
                        size = 0
                        for i in range(now - count * unit, now - (count + 1) * unit, -1):
                            if i in packets[packet_id]:
                                size += packets[packet_id][i]
                        ydata.insert(0, size)
                        count += 1
                    ydatas.update({
                        packet_id: ydata
                    })

            self.ydatas = ydatas

            self.force_draw = force_draw
            self._draw_frame(0)


    def update_time_unit(self, unit):
        self.unit = unit

    def hover(self, event):
        if event.inaxes == self.ax and len(self.xdatas) > 0 and self.current_mouse_area == "axes":
            xtick_labels = self.ax.get_xticklabels()
            xtick_data = xtick_labels[len(xtick_labels) - 1]
            if ':' not in xtick_data.get_text():
                return

            hour, minute, second = xtick_data.get_text().split(':')
            hovered_time = datetime.datetime.now()
            hovered_time = hovered_time.replace(hour=int(hour), minute=int(minute), second=int(second))
            hovered_time = hovered_time.timestamp()
            mouse_pos_x = int(round(event.xdata))
            xtick_x = xtick_data.get_position()[0]

            hovered_time += self.unit * (mouse_pos_x - xtick_x)
            hovered_time = datetime.datetime.fromtimestamp(hovered_time)
            time_annot_text = "%02d/%02d %02d:%02d:%02d" % (hovered_time.month, hovered_time.day, hovered_time.hour, hovered_time.minute, hovered_time.second)
            ymin, ymax = self.ax.get_ylim()

            if mouse_pos_x < 100 and mouse_pos_x >= 0:
                if self.vline is not None:
                    if self.vline.get_xdata() != mouse_pos_x:
                        self.vline.set_xdata(mouse_pos_x)
                else:
                    self.vline = self.ax.axvline(mouse_pos_x, ymin, ymax, linewidth=0.6, color="#666666")

                if self.time_annot is not None:
                    if self.time_annot.xy[0] != mouse_pos_x:
                        self.time_annot.xy = (mouse_pos_x, 0)
                        self.time_annot.set_text(time_annot_text)
                else:
                    self.time_annot = self.ax.annotate(time_annot_text, xy=(mouse_pos_x, 0), xytext=(0, -26), textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="black"), color="white",
                                        horizontalalignment="center", fontsize=8)

            self.fig.canvas.draw_idle()

    def update_is_record(self, is_record):
        self.is_record = is_record
