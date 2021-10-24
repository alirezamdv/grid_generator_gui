"""
a.mahdavi@outlook.com
"""

from PyQt5.QtWidgets import (QWidget, QGridLayout, QGroupBox, QVBoxLayout, QLineEdit, QLabel, QPushButton)


# def deleteItemsOfLayout(layout):
#     if layout is not None:
#         while layout.count():
#             item = layout.takeAt(0)
#             widget = item.widget()
#             if widget is not None:
#                 widget.setParent(None)
#             else:
#                 deleteItemsOfLayout(item.layout())


class AreaBox(QWidget):

    def __init__(self, start_to_draw, warning):
        QWidget.__init__(self)

        self.setWindowTitle("GroupBox")
        layout = QVBoxLayout()
        self.setLayout(layout)
        myQLabel = QLabel()
        groupbox = QGroupBox("priority area")
        # groupbox.setMinimumSize(1500,1500)
        groupbox.setCheckable(False)
        layout.addWidget(groupbox)
        self.start_draw_point = start_to_draw
        self.warning = warning
        self.vbox = QGridLayout()
        self.number_of_area = 1
        self.points = {}
        self.areas = []
        groupbox.setLayout(self.vbox)
        self.init_ui()

    def init_ui(self):
        # l_name = self.name.text()
        # self.layouts[l_name] = QGridLayout()
        p_area_name_label = QLabel("area_name")
        self.p_area_name = QLineEdit(f"priority_area_{self.number_of_area}")
        # p_area_name.setReadOnly(True)
        p_area_inner_label = QLabel("inner_circle")
        self.p_area_inner = QLineEdit("0.5")
        p_area_outer_label = QLabel("outer_circle")
        self.p_area_outer = QLineEdit("0.7")
        p_area_res_label = QLabel("resolution")
        self.p_area_res = QLineEdit("200.0")
        self.long = QLineEdit("longitude")
        self.lat = QLineEdit("latitude")
        self.p_area = QPushButton("Add priority area on map")
        self.p_area.clicked.connect(self.start_draw_point)
        self.addButton = QPushButton("add priority area")
        self.addButton.clicked.connect(self.add)
        self.delButton = QPushButton("delete a priority area")
        self.delButton.clicked.connect(self.delete)
        self.vbox.addWidget(p_area_name_label, 1, 2)
        self.vbox.addWidget(self.p_area_name, 1, 3)
        self.vbox.addWidget(p_area_inner_label, 1, 4)
        self.vbox.addWidget(self.p_area_inner, 1, 5)
        self.vbox.addWidget(p_area_outer_label, 1, 6)
        self.vbox.addWidget(self.p_area_outer, 1, 7)
        self.vbox.addWidget(p_area_res_label, 1, 8)
        self.vbox.addWidget(self.p_area_res, 1, 9)
        self.vbox.addWidget(self.long, 1, 10)
        self.vbox.addWidget(self.lat, 1, 11)
        self.vbox.addWidget(self.p_area, 1, 12)
        self.vbox.addWidget(self.addButton, 2, 3)
        self.vbox.addWidget(self.delButton, 2, 4)

    def add(self, name):
        self.warning(type="Info", text=f"the {self.p_area_name.text()} is added.")
        self.areas.append([
            self.p_area_name.text(),
            self.long.text(),
            self.lat.text(),
            self.p_area_inner.text(),
            self.p_area_outer.text(),
            self.p_area_res.text(),
        ])
        self.number_of_area += 1
        # self.name.setText(f"priority_area_{self.number_of_area}")
        # p_area_name = QLineEdit(l_name)
        # p_area_name.setReadOnly(True)
        # p_area_inner = QLineEdit("inner_circle")
        # p_area_outer = QLineEdit("outer_circle")
        # p_area_res = QLineEdit("resolution")
        # p_area = QPushButton("Add priority area on map")
        # p_area.clicked.connect(self.start_draw_point)
        # self.layouts[l_name].addWidget(p_area_name, self.number_of_area, 1)
        # self.layouts[l_name].addWidget(p_area_inner, self.number_of_area, 2)
        # self.layouts[l_name].addWidget(p_area_outer, self.number_of_area, 3)
        # self.layouts[l_name].addWidget(p_area_res, self.number_of_area, 4)
        # self.layouts[l_name].addWidget(p_area, self.number_of_area, 5)
        # self.vbox.addLayout(self.layouts[l_name], self.number_of_area, 1)

    def delete(self):
        self.warning(type="Info", text=f"the {self.p_area_name.text()} is removed.")
        for p in self.areas:
            if p[0] == self.p_area_name.text():
                self.areas.remove(p)
                break
        # try:
        #     for i in range(self.vbox.count()):
        #         layout_item = self.vbox.itemAt(i)
        #         print(layout_item.layout())
        #         if layout_item.layout() == self.layouts[box]:
        #             deleteItemsOfLayout(layout_item.layout())
        #             self.vbox.removeItem(layout_item)
        #             break
        # except KeyError as er:
        #     return
