from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib.pyplot as plt
import math


class Graph(FigureCanvas, TimedAnimation):
    def __init__(self, packets_info, graph_press_callback, update_table_callback):
        self.fig = Figure(figsize=(10, 5))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ydatas = {}
        self.xdatas = []
        self.xticks = [i for i in range(100)]
        self.current_time = 0
        self.temp_ydatas = {}
        self.unit = 1
        self.current_mouse_area = "out" # 'out', 'figure', 'axes'
        self.vline = None
        self.hline = None
        self.time_annot = None
        self.size_annot = None
        self.drawed_time = 0
        self.is_record = True
        self.packets_info = packets_info
        self.force_draw = False
        self.need_update = False
        self.graph_press_callback = graph_press_callback
        self.update_table_callback = update_table_callback
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=1000, blit=True)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        self.fig.canvas.mpl_connect("button_press_event", self.press)
        self.fig.canvas.mpl_connect("figure_enter_event", self.figure_enter)
        self.fig.canvas.mpl_connect("figure_leave_event", self.figure_leave)
        self.fig.canvas.mpl_connect("axes_enter_event", self.axes_enter)
        self.fig.canvas.mpl_connect("axes_leave_event", self.axes_leave)
        self.fig.tight_layout(rect=(0, 0, 0.97, 1))
        # self.fig.set_tight_layout({"h_pad": True})
        plt.style.use('seaborn-white')

    def figure_enter(self, event):
        self.current_mouse_area = "figure"

    def figure_leave(self, event):
        self.current_mouse_area = "out"

    def axes_enter(self, event):
        self.current_mouse_area = "axes"

    def axes_leave(self, event):
        self.current_mouse_area = "figure"

    def press(self, event):
        if self.current_mouse_area == "axes" and event.xdata < 100 and event.xdata >= 0 and len(self.xdatas) > 0:
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
        self.update_table_callback()
        if len(self.xdatas) > 0:
            if self.is_record or self.force_draw:
                self.ax.clear()
                for packet_id in self.ydatas.keys():
                    if packet_id in self.selected_packets:
                        self.ax.plot(self.xticks, self.ydatas[packet_id], color=self.packets_info[packet_id]["color"])
                self.ax.grid(color='#d0d0d0', linestyle='-', linewidth=0.3)
                self.ax.yaxis.set_ticks_position("right")

            if self.vline is not None:
                if self.current_mouse_area == "axes":
                    if self.is_record or self.force_draw:
                        self.vline.set_visible(True)
                        self.ax.add_line(self.vline)
                    else:
                        self.vline.set_visible(True)
                else:
                    self.vline.set_visible(False)

            if self.time_annot is not None:
                if self.current_mouse_area == "axes":
                    if self.is_record or self.force_draw:
                        self.time_annot.set_visible(True)
                        self.ax._add_text(self.time_annot)
                    else:
                        self.time_annot.set_visible(True)
                else:
                    self.time_annot.set_visible(False)

            if self.hline is not None:
                if self.current_mouse_area == "axes":
                    if self.is_record or self.force_draw:
                        self.hline.set_visible(True)
                        self.ax.add_line(self.hline)
                    else:
                        self.hline.set_visible(True)
                else:
                    self.hline.set_visible(False)

            if self.size_annot is not None:
                if self.current_mouse_area == "axes":
                    if self.is_record or self.force_draw:
                        self.size_annot.set_visible(True)
                        self.ax._add_text(self.size_annot)
                    else:
                        self.size_annot.set_visible(True)
                else:
                    self.size_annot.set_visible(False)

            unit = self.unit
            if unit == 1 or unit == 30 or unit == 60:
                # set visible xtick per unit*10
                xtick_unit = unit * 10
            elif unit == 5 or unit == 10 or unit == 600 or unit == 1800 or unit == 3600:
                # set visible xtick per unit*12
                xtick_unit = unit * 12
            else:
                xtick_unit = 10

            xticks = []
            xtick_labels = []

            if self.force_draw:
                for i in range(len(self.xdatas)-1, -1, -1):
                    xtick = self.xdatas[i]
                    xtick -= xtick % unit

                    if xtick % xtick_unit == 0:
                        xticks.insert(0, self.xticks[i])
            else:
                is_unit_time = False

                for i in range(len(self.xdatas)-1, -1, -1):
                    xtick = self.xdatas[i]
                    if xtick % xtick_unit == 0:
                        xticks.insert(0, self.xticks[i])
                        is_unit_time = True
                if not is_unit_time:
                    self.ax.set_xticks(self.saved_xticks)
                    self.ax.set_xticklabels(self.saved_xtick_labels)
                    return

            for i in xticks:
                tick_time = datetime.datetime.fromtimestamp(self.xdatas[i])
                xtick_labels.append("%02d:%02d:%02d" % (tick_time.hour, tick_time.minute, tick_time.second))

            self.ax.set_xticks(xticks)
            self.ax.set_xticklabels(xtick_labels)
            self.saved_xticks = xticks
            self.saved_xtick_labels = xtick_labels
            if self.force_draw:
                self.force_draw = False

            self.fig.canvas.draw_idle()


    def new_frame_seq(self):
        return iter(range(100))

    def update_packet_data(self, packets, unit, selected_packets, now, force_draw, updated_packet_id):
        self.selected_packets = selected_packets

        if force_draw:
            count = 0

            xdatas = []  # same for all
            now = time = int(self.xdatas[len(self.xdatas) - 1])

            while count < 100:
                xdatas.insert(0, time)
                time -= unit
                count += 1
            self.xdatas = xdatas

            ydatas = {}
            for packet_id in selected_packets:
                count = 0
                ydata = []
                while count < 100:
                    size_sum = 0
                    for i in range(now - count * unit, now - (count + 1) * unit, -1):
                        if i in packets[packet_id]:
                            for size in packets[packet_id][i]:
                                size_sum += size
                    ydata.insert(0, size_sum)
                    count += 1
                ydatas.update({
                    packet_id: ydata
                })

            self.ydatas = ydatas

            self.force_draw = force_draw
            self._draw_frame(0)
        elif self.is_record:
            count = 0
            if len(self.xdatas) == 0:
                xdatas = []  # same for all
                time = now
                while count < 100:
                    xdatas.insert(0, time)
                    time -= unit
                    count += 1
                self.xdatas = xdatas

                ydatas = {}
                for packet_id in selected_packets:
                    count = 0
                    ydata = []
                    while count < 100:
                        size_sum = 0
                        for i in range(now-count*unit, now-(count+1)*unit, -1):
                            if i in packets[packet_id]:
                                for size in packets[packet_id][i]:
                                    size_sum += size
                        ydata.insert(0, size_sum)
                        count += 1
                    ydatas.update({
                        packet_id: ydata
                    })
                self.ydatas = ydatas
            elif len(self.xdatas) > 0:
                if now % unit == 0:
                    if now not in self.xdatas:
                        self.xdatas.remove(self.xdatas[0])
                        self.xdatas.append(now)

                    if self.current_time != now:
                        for packet_id in selected_packets:
                            size_sum = 0
                            for i in range(now-1, now-unit, -1):
                                if i in packets[packet_id]:
                                    for size in packets[packet_id][i]:
                                        size_sum += size

                            if packet_id in self.ydatas:
                                ydata = self.ydatas[packet_id]
                                ydata.remove(ydata[0])
                                ydata.append(size_sum)
                            else:
                                ydata = [0 for i in range(0, 99, 1)]
                                ydata.append(size_sum)
                                self.ydatas.update({
                                    packet_id: ydata
                                })
                        self.current_time = now

                    if updated_packet_id is not None:
                        updated_packet_size = packets[updated_packet_id][now][-1]
                        if updated_packet_id in self.ydatas:
                            self.ydatas[updated_packet_id][-1] += updated_packet_size
                        else:
                            ydata = [0 for i in range(0, 99, 1)]
                            ydata.append(updated_packet_size)
                            self.ydatas.update({
                                updated_packet_id: ydata,
                            })


    def update_time_unit(self, unit):
        self.unit = unit
        self.event_source.interval = unit * 1000
        self.need_update = True

    def hover(self, event):
        if event.inaxes == self.ax and len(self.xdatas) > 0 and self.current_mouse_area == "axes":
            xtick_labels = self.ax.get_xticklabels()

            i = len(xtick_labels)-1
            while ':' not in xtick_labels[i].get_text():
                i -= 1
                if i < 0:
                    return
            xtick_data = xtick_labels[i].get_text()

            hour, minute, second = xtick_data.split(':')
            hovered_time = datetime.datetime.now()
            hovered_time = hovered_time.replace(hour=int(hour), minute=int(minute), second=int(second))
            hovered_time = hovered_time.timestamp()
            mouse_pos_x = int(round(event.xdata))
            xtick_x = xtick_labels[i].get_position()[0]

            hovered_time += self.unit * (mouse_pos_x - xtick_x)
            hovered_time = datetime.datetime.fromtimestamp(hovered_time)
            time_annot_text = "%02d/%02d %02d:%02d:%02d" % (hovered_time.month, hovered_time.day, hovered_time.hour, hovered_time.minute, hovered_time.second)
            ymin, ymax = self.ax.get_ylim()

            if mouse_pos_x < 100 and mouse_pos_x >= 0:
                if self.vline is not None:
                    if self.vline.get_xdata() != mouse_pos_x:
                        self.vline.set_xdata(mouse_pos_x)
                else:
                    self.vline = self.ax.axvline(mouse_pos_x, ymin, ymax, linewidth=0.2, color="#000000")

                if self.time_annot is not None:
                    if self.time_annot.xy[0] != mouse_pos_x:
                        self.time_annot.xy = (mouse_pos_x, 0)
                        self.time_annot.set_text(time_annot_text)
                else:
                    self.time_annot = self.ax.annotate(time_annot_text, xy=(mouse_pos_x, 0), xytext=(0, -25), textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="black"), color="white",
                                        horizontalalignment="center", fontsize=8)

            mouse_pos_y = int(round(event.ydata))
            xmin, xmax = self.ax.get_xlim()
            if mouse_pos_y >= 0:
                if self.hline is not None:
                    if self.hline.get_ydata() != mouse_pos_y:
                        self.hline.set_ydata(mouse_pos_y)
                else:
                    self.hline = self.ax.axhline(mouse_pos_y, xmin, xmax, linewidth=0.2, color="#000000")

                if self.size_annot is not None:
                    if self.size_annot.xy[1] != mouse_pos_y:
                        self.size_annot.xy = (xmax, mouse_pos_y)
                        self.size_annot.set_text(self.convert_size(mouse_pos_y))
                else:
                    self.size_annot = self.ax.annotate(self.convert_size(mouse_pos_y), xy=(xmax, mouse_pos_y), xytext=(5, 0), textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="black"), color="white",
                                        horizontalalignment="left", fontsize=8)

            if self.need_update:
                self._draw_frame(0)
                self.need_update = False

            self.fig.canvas.draw_idle()

    def update_is_record(self, is_record):
        self.is_record = is_record

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
