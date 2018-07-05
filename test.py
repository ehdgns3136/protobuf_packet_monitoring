from PyQt5.QtWidgets import *

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, str):
        super().__init__(str)
        # print(str)

    def __lt__(self, other):
        data = self.data(0)
        other_data = other.data(0)
        if data.isdigit() and other_data.isdigit():
            return data < other_data
        elif data[:len(data)-1].replace(" ", "").isdigit() and other_data[:len(other_data)-1].replace(" ", "").isdigit():
            return int(data[:len(data)-1]) < int(other_data[:len(other_data)-1])
        else:
            return data < other_data

item1 = MyQTableWidgetItem("1032")
item2 = MyQTableWidgetItem("1031")

item3 = MyQTableWidgetItem("1032 B")
item4 = MyQTableWidgetItem("203 B")

item5 = MyQTableWidgetItem("apple")
item6 = MyQTableWidgetItem("banana")

print(item1 > item2)
print(item3 < item4)
print(item5 < item6)