from threading import Thread
import socket
import re
import datetime
import sys
from time import sleep
from PyQt5.QtWidgets import *
from .Window import MonitorWindow
import random

class PacketMonitor:
    byte_limit = 10000
    width = 1100
    height = 900

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 8080))
        self.packets_info = self.build_packets_info()
        self.packets = {}
        self.all_packets_size = 0
        self.all_packets_count = 0
        self.selected_packets = []
        self.selected_time = None

        self.unit = 1
        self.is_record = True
        self.first_record_time = None

        self.app = QApplication(sys.argv)
        self.window = MonitorWindow(
            self.width,
            self.height,
            self.update_time_unit_callback,
            self.record_state_change_callback,
            self.color_box_click_callback,
            self.graph_press_callback,
            self.packets_info
        )
        self.packet_count = 0

    def get_random_color(self):
        r = lambda: random.randint(0, 255)
        return '#%02X%02X%02X' % (r(), r(), r())

    def build_packets_info(self):
        packets_info = {}

        f = open("network.proto", 'r', encoding="UTF-8")
        p = re.compile('.*=.*;')
        is_packet = False

        while True:
            line = f.readline()
            if not line:
                break

            if "message Packet" in line:
                is_packet = True

            if is_packet:
                if "}" in line:
                    break

                if p.match(line):
                    line = line.replace(" ", "").replace(";", "").replace("\n", "").replace("\t", "")
                    if "/" in line:
                        idx = line.find("/")
                        line = line[:idx]
                    if len(line) == 0:
                        continue
                    pair = line.split("=")
                    packets_info.update({
                        pair[1]: {
                            "name": pair[0],
                            "color": self.get_random_color(),
                            "visible": True,
                        }
                    })
        f.close()
        return packets_info

    def handle_packet(self):
        while True:
            data, addr = self.sock.recvfrom(self.byte_limit)
            id, size = data.decode().split(':')
            now = int(datetime.datetime.now().timestamp())
            if self.first_record_time is None:
                self.first_record_time = now
                self.window.table.first_record_time = now

            if id in self.packets:
                if now in self.packets[id]:
                    self.packets[id][now].append(int(size))
                else:
                    self.packets[id].update({
                        now: [int(size)]
                    })
            else:
                self.selected_packets.append(id)
                self.packets.update({
                    id: {
                        now: [int(size)]
                    }
                })
            self.window.update_packet_data(self.packets, self.unit, self.selected_packets, self.selected_time, now, False, id)

    def periodic_update_canvas(self):
        while True:
            if len(self.packets) > 0:
                now = int(datetime.datetime.now().timestamp())
                self.window.update_packet_data(self.packets, self.unit, self.selected_packets, self.selected_time, now, False)
            sleep(self.unit)

    def update_time_unit_callback(self, unit):
        time_unit = unit[len(unit)-1]
        if time_unit == 's':
            self.unit = int(unit[:len(unit)-1])
        elif time_unit == 'm':
            self.unit = int(unit[:len(unit)-1]) * 60
        elif time_unit == 'h':
            self.unit = int(unit[:len(unit)-1]) * 3600
        self.window.update_time_unit(self.unit)
        now = int(datetime.datetime.now().timestamp())
        self.window.update_packet_data(self.packets, self.unit, self.selected_packets, self.selected_time, now, True)

    def record_state_change_callback(self):
        self.is_record = not self.is_record
        self.selected_time = None
        self.window.update_is_record(self.is_record)
        if self.is_record:
            now = int(datetime.datetime.now().timestamp())
            self.window.update_packet_data(self.packets, self.unit, self.selected_packets, self.selected_time, now, True)


    def color_box_click_callback(self, packet_id):
        self.packets_info[packet_id]["visible"] = not self.packets_info[packet_id]["visible"]

        if not self.packets_info[packet_id]["visible"]:
            if packet_id in self.selected_packets:
                self.selected_packets.remove(packet_id)
        else:
            if packet_id not in self.selected_packets:
                self.selected_packets.append(packet_id)
        now = int(datetime.datetime.now().timestamp())
        self.window.update_packet_data(self.packets, self.unit, self.selected_packets, self.selected_time, now, True)

    def graph_press_callback(self, selected_time):
        self.selected_time = selected_time

        if self.is_record:
            self.record_state_change_callback()
        now = int(datetime.datetime.now().timestamp())
        self.window.update_packet_data(self.packets, self.unit, self.selected_packets, selected_time, now, True)

    def run(self):
        thread1 = Thread(target=self.handle_packet)
        thread1.start()

        thread2 = Thread(target=self.periodic_update_canvas)
        thread2.start()

        self.window.show()
        self.app.exec_()