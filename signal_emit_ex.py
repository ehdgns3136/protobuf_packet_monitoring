import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
from time import sleep

class MyWindow(QWidget, QObject):
    cell_update = pyqtSignal(int)

    def __init__(self):
        QObject.__init__(self)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)

        self.tableWidget = QTableWidget(100, 2)
        self.tableWidget.resize(290, 290)
        self.tableWidget.setHorizontalHeaderLabels(['visible', 'color'])
        self.tableWidget.verticalHeader().hide()
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def updateCell(self, i):
        self.button = QPushButton()
        self.button.setStyleSheet("QPushButton { background-color: blue }")
        # button.clicked.connect(lambda *args, row=1, column=0: self.buttonClicked(row, column))

        self.tableWidget.setCellWidget(i, 1, self.button)

    def roop(self):
        i = 0
        while i < 100:
            self.cell_update.emit(i)
            i += 1
            sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    # mywindow.roop()

    mywindow.cell_update.connect(mywindow.updateCell)

    thread = Thread(target=mywindow.roop)
    thread.start()
    mywindow.show()
    app.exec_()
