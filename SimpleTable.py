import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
from time import sleep

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, str):
        super().__init__(str)
        # print(str)

    def __lt__(self, other):
        data = self.data()
        other_data = other.data()
        if data.isdigit() and other_data.isdigit():
            return data < other_data
        elif data[:len(data)-1].replace(" ", "").isdigit() and other_data[:len(other_data)-1].replace(" ", "").isdigit():
            return data[:len(data)-1] < other_data[:len(other_data)-1]
        else:
            return data < other_data


class MyWindow(QTableWidget):
    def __init__(self):
        super().__init__(2, 2)
        self.setupUI()

    def get_darker_color(self, color):
        darker = lambda hex_str: int(hex_str, 16) - 20 if int(hex_str, 16) - 20 >= 0 else 0
        return '#%02X%02X%02X' % (darker(color[1:3]), darker(color[3:5]), darker(color[5:7]))

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)

        self.resize(290, 290)
        self.setHorizontalHeaderLabels(['visible', 'color'])

        header = self.horizontalHeader()
        header.sectionClicked.connect(self.horizontal_header_clicked)

        myItem1 = MyQTableWidgetItem("103 B")
        myItem2 = MyQTableWidgetItem("104 B")


        self.setButtonToCell(0, 1)
        self.setButtonToCell(1, 1)
        self.setItem(0, 0, myItem1)
        self.setCellWidget(1, 0, QLabel('0'))

    def horizontal_header_clicked(self, idx):
        print('hello', idx)

    def clickButton(self, i):
        print(i)
        self.sortByColumn(0, i)

    def selectColumn(self, p_int):
        print(p_int)

    def setButtonToCell(self, row, col):
        self.button = QPushButton()
        self.button.setFixedWidth(13)
        self.button.setFixedHeight(13)
        self.button.clicked.connect(lambda : self.clickButton(row))

        color = "#a2ffff"
        self.button.setStyleSheet(
            "QPushButton { background-color: %s; border-style: outset; border-width: 1px; border-color: rgb(212, 212, 212);} QPushButton:hover { border-color: rgb(160, 160, 160);} QPushButton:pressed { background-color: %s;}" % (
            color, self.get_darker_color(color)))
        button_widget = QWidget()
        layout = QHBoxLayout(button_widget)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(row, col, button_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()