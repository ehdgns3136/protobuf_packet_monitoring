from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Graph import Graph
from .Table import Table

class MonitorWindow(QWidget):
    def __init__(self, width, height, update_time_unit_callback, record_state_change_callback,
                 color_box_click_callback, graph_press_callback, packets_info):
        super().__init__()
        self.setupUI(width, height, packets_info, color_box_click_callback, graph_press_callback)
        self.update_time_unit_callback = update_time_unit_callback
        self.record_state_change_callback = record_state_change_callback
        self.is_record = True

    def setupUI(self, width, height, packets_info, color_box_click_callback, graph_press_callback):
        self.setGeometry(600, 100, width, height)
        self.setWindowTitle("Packet Monitor")
        self.setWindowIcon(QIcon('icon.png'))

        # firstLayout, set time unit
        self.unitComboBox = QComboBox()
        self.unitComboBox.setStyleSheet("QComboBox {width: 30px; height: 25px;}")

        units = ["1s", "5s", "10s", "30s", "1m", "10m", "30m (slow)", "1h (slow)"]
        for unit in units:
            self.unitComboBox.addItem(unit)
        self.unitComboBox.activated[str].connect(self.unitComboBox_clicked)

        self.recordButton = QPushButton("record")
        self.recordButton.setStyleSheet("QPushButton { background-color: #db2828; color: white; border-radius: 3px; width: 80px; height: 25px;} QPushButton::hover {background-color: #ba2121;}")
        self.recordButton.clicked.connect(self.record_state_change)

        firstLayout = QHBoxLayout()
        firstLayout.addStretch(1)
        firstLayout.addWidget(self.recordButton)
        firstLayout.addWidget(self.unitComboBox)

        # secondLayout, Grpah
        self.graph = Graph(packets_info, graph_press_callback)
        secondLayout = QHBoxLayout()
        secondLayout.addWidget(self.graph)

        # thirdLayout, Table
        self.table = Table(width, height, packets_info, color_box_click_callback)
        thirdLayout = QHBoxLayout()
        thirdLayout.addWidget(self.table)

        layout = QVBoxLayout()
        layout.addLayout(firstLayout)
        layout.addLayout(secondLayout)
        layout.addLayout(thirdLayout)
        self.setStyleSheet('background: white;')
        self.setLayout(layout)

    def unitComboBox_clicked(self, text):
        self.update_time_unit_callback(text)

    def update_packet_data(self, packets, unit, selected_packets, selected_time, now, force_draw=False):
        self.graph.update_packet_data(packets, unit, selected_packets, now, force_draw)
        self.table.update_packet_data(packets, unit, selected_time, now)

    def update_time_unit(self, unit):
        self.graph.update_time_unit(unit)
        self.table.update_time_unit(unit)

    def record_state_change(self):
        self.record_state_change_callback()

    def update_is_record(self, is_record):
        self.graph.update_is_record(is_record)
        self.table.update_is_record(is_record)
        self.is_record = is_record
        if is_record:
            self.recordButton.setStyleSheet(
                "QPushButton { background-color: #db2828; color: white; border-radius: 3px; width: 80px; height: 25px;} QPushButton::hover {background-color: #ba2121;}")
        else:
            self.recordButton.setStyleSheet(
                "QPushButton { background-color: rgb(200, 200, 200); color: rgb(100, 100, 100); border-radius: 3px; width: 80px; height: 25px;} QPushButton::hover {background-color: #afafaf;}")


