from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
import math

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, str):
        super().__init__(str)

    def __lt__(self, other):
        data = self.data(0)
        other_data = other.data(0)
        data_type = self.get_type()
        other_type = other.get_type()
        if data_type == 'count' and other_type == 'count':
            return int(data) < int(other_data)
        elif data_type == 'size' and other_type == 'size':
            return self.get_size() < other.get_size()
        else:
            return data > other_data

    def get_type(self):
        data = self.data(0)
        if data.isdigit():
            return 'count'
        data = data.replace(" ", "")
        if data[len(data)-1] == 'B':
            if data[len(data)-2] in ['K', 'M', 'G', 'T', 'P', 'E', 'Z', 'V']:
                to_check = data[:len(data)-2]
            else:
                to_check = data[:len(data)-1]

            try:
                float(to_check)
            except ValueError:
                return 'name'

            return 'size'
        return 'name'

    def get_size(self):
        data = self.data(0)
        data = data.replace(" ", "")
        size_name = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

        for i in range(len(size_name)-1, -1, -1):
            if size_name[i] in data:
                if size_name[i] == 'B':
                    return float(data[:len(data)-1])
                return float(data[:len(data)-2]) * 1024 ** i



class Table(QTableWidget, QObject):
    update_table_signal = pyqtSignal(dict)

    def __init__(self, width, height, packets_info, color_box_click_callback):
        super().__init__(3, 4)
        self.setupUI(width, height)
        self.packets_info = packets_info
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 370)
        self.setColumnWidth(2, 300)
        self.setColumnWidth(3, 300)
        self.cell_items = {}
        self.setShowGrid(False)
        self.update_table_signal.connect(self.update_table)
        self.color_box_click_callback = color_box_click_callback
        self.is_record = True
        self.sort_by = 3
        self.selected_time = None

    def setupUI(self, width, height):
        self.setGeometry(800, 200, width, height)
        self.verticalHeader().hide()

    def update_packet_data(self, packets, unit, selected_time, now):
        if self.is_record:
            if selected_time is None:
                cell_datas = {}
                for packet_id in packets.keys():
                    time_count = 0
                    size_sum = 0
                    packet_count = 0
                    while time_count < unit * 100:
                        for i in range(unit):
                            time = now-(time_count + i)
                            if time in packets[packet_id]:
                                if len(packets[packet_id][time]) > 0:
                                    packet_count += len(packets[packet_id][time])
                                    for size in packets[packet_id][time]:
                                        size_sum += size
                        time_count += unit

                    info = self.packets_info[packet_id]
                    cell_data = [info['visible'], info['color'], info['name'], packet_count, size_sum]
                    cell_datas.update({
                        packet_id: cell_data
                    })
                self.selected_time = None
                self.update_table_signal.emit(cell_datas)
        else:
            if selected_time is not None or self.selected_time is not None:
                if selected_time is None and self.selected_time is not None:
                    selected_time = self.selected_time
                cell_datas = {}
                for packet_id in packets.keys():
                    size_sum = 0
                    packet_count = 0
                    for i in range(unit):
                        time = selected_time-i
                        if time in packets[packet_id]:
                            if len(packets[packet_id][time]) > 0:
                                packet_count += len(packets[packet_id][time])
                                for size in packets[packet_id][time]:
                                    size_sum += size

                    info = self.packets_info[packet_id]
                    cell_data = [info['visible'], info['color'], info['name'], packet_count, size_sum]
                    cell_datas.update({
                        packet_id: cell_data
                    })
                self.selected_time = selected_time
                self.update_table_signal.emit(cell_datas)
            else:
                cell_datas = {}
                for packet_id in packets.keys():
                    time_count = 0
                    size_sum = 0
                    packet_count = 0
                    while time_count < unit * 100:
                        for i in range(unit):
                            time = self.stop_time - (time_count + i)
                            if time in packets[packet_id]:
                                if len(packets[packet_id][time]) > 0:
                                    packet_count += len(packets[packet_id][time])
                                    for size in packets[packet_id][time]:
                                        size_sum += size
                        time_count += unit

                    info = self.packets_info[packet_id]
                    cell_data = [info['visible'], info['color'], info['name'], packet_count, size_sum]
                    cell_datas.update({
                        packet_id: cell_data
                    })
                self.update_table_signal.emit(cell_datas)


    def get_darker_color(self, color):
        darker = lambda hex_str: int(hex_str, 16) - 20 if int(hex_str, 16) - 20 >= 0 else 0
        return '#%02X%02X%02X' % (darker(color[1:3]), darker(color[3:5]), darker(color[5:7]))

    def get_row_items(self, data, packet_id):
        # row, col
        button = QPushButton()
        button.setFixedWidth(15)
        button.setFixedHeight(15)

        visible = data[0]
        if visible:
            button.setStyleSheet(
                "QPushButton { background-color: %s; border-style: outset; border-width: 1px; border-color: rgb(212, 212, 212);} QPushButton:hover { border-color: rgb(160, 160, 160);} QPushButton:pressed { background-color: %s;}" % (
                data[1], self.get_darker_color(data[1])))
        else:
            button.setStyleSheet("QPushButton { background-color: white; border-style: outset; border-width: 1px; border-color: rgb(212, 212, 212);} QPushButton:hover { border-color: rgb(160, 160, 160);} QPushButton:pressed { background-color: rgb(250, 250, 250);}")

        button.clicked.connect(lambda : self.colorBoxClicked(packet_id))
        button_widget = QWidget()
        layout = QHBoxLayout(button_widget)
        layout.addWidget(button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        name = MyQTableWidgetItem(data[2])
        name.setTextAlignment(Qt.AlignCenter)

        count = MyQTableWidgetItem(str(data[3]))
        count.setTextAlignment(Qt.AlignCenter)

        size = MyQTableWidgetItem(self.convert_size(data[4]))
        size.setTextAlignment(Qt.AlignCenter)

        row_items = [button_widget, name, count, size]
        return row_items

    def update_table(self, cell_datas):
        self.clear()
        self.setHorizontalHeaderLabels(['Visible/Color', 'Name', 'Count', 'Size(Byte)'])

        header = self.horizontalHeader()
        header.sectionClicked.connect(self.horizontal_header_clicked)

        row = 0
        self.setRowCount(len(cell_datas.keys()))
        for packet_id in cell_datas.keys():
            row_items = self.get_row_items(cell_datas[packet_id], packet_id)
            self.setCellWidget(row, 0, row_items[0])
            self.setItem(row, 1, row_items[1])
            self.setItem(row, 2, row_items[2])
            self.setItem(row, 3, row_items[3])
            row += 1

        self.sortByColumn(self.sort_by, Qt.DescendingOrder)

    def horizontal_header_clicked(self, col):
        if col != 0:
            self.sortByColumn(col, Qt.DescendingOrder)
            self.sort_by = col

    def colorBoxClicked(self, packet_id):
        self.color_box_click_callback(packet_id)

    def update_is_record(self, is_record):
        self.is_record = is_record

        if not is_record:
            self.stop_time = int(datetime.datetime.now().timestamp())

    def update_time_unit(self, unit):
        self.unit = unit

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
