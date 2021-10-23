from PyQt5.QtWidgets import (QWidget, QGridLayout, QGroupBox, QVBoxLayout, QLineEdit, QLabel, QPushButton)


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())


class AreaBox(QWidget):

    def __init__(self, start_to_draw):
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
        self.vbox = QGridLayout()
        self.number_of_area = 1
        self.layouts = {}
        self.name = QLineEdit(f"priority_area_{self.number_of_area}")
        self.addButton = QPushButton("add priority area")
        self.addButton.clicked.connect(self.add)
        self.delButton = QPushButton("delete a priority area")
        self.delButton.clicked.connect(self.delete)

        self.vbox.addWidget(self.name, 1, 1)
        self.vbox.addWidget(self.addButton, 1, 2)
        self.vbox.addWidget(self.delButton, 1, 3)
        self.areas = []
        groupbox.setLayout(self.vbox)

    def add(self):
        self.number_of_area += 1
        l_name = self.name.text()
        self.name.setText(f"priority_area_{self.number_of_area}")
        self.layouts[l_name] = QGridLayout()
        p_area_name = QLineEdit(l_name)
        p_area_name.setReadOnly(True)
        p_area_inner = QLineEdit("inner_circle")
        p_area_outer = QLineEdit("outer_circle")
        p_area_res = QLineEdit("resolution")
        p_area = QPushButton("Add priority area on map")
        p_area.clicked.connect(self.start_draw_point)
        self.layouts[l_name].addWidget(p_area_name, self.number_of_area, 1)
        self.layouts[l_name].addWidget(p_area_inner, self.number_of_area, 2)
        self.layouts[l_name].addWidget(p_area_outer, self.number_of_area, 3)
        self.layouts[l_name].addWidget(p_area_res, self.number_of_area, 4)
        self.layouts[l_name].addWidget(p_area, self.number_of_area, 5)
        self.vbox.addLayout(self.layouts[l_name], self.number_of_area, 1)

    def delete(self):
        box = self.name.text()
        try:
            for i in range(self.vbox.count()):
                layout_item = self.vbox.itemAt(i)
                print(layout_item.layout())
                if layout_item.layout() == self.layouts[box]:
                    deleteItemsOfLayout(layout_item.layout())
                    self.vbox.removeItem(layout_item)
                    break
        except KeyError as er:
            return
