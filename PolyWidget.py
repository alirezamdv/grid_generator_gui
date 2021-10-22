from PyQt5.QtWidgets import (QWidget, QGridLayout, QGroupBox, QVBoxLayout, QLineEdit, QLabel)


class PolyBox(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("GroupBox")
        layout = QVBoxLayout()
        self.setLayout(layout)
        myQLabel = QLabel()
        # myQLabel.setText('''<a href='http://stackoverflow.com'>stackoverflow</a>''')
        # myQLabel.setOpenExternalLinks(True)
        groupbox = QGroupBox(f"Poly file")
        groupbox.setCheckable(False)
        layout.addWidget(groupbox)

        vbox = QGridLayout()
        groupbox.setLayout(vbox)

        # line 1
        node_label = QLabel('number of nodes: ')
        self.node_number = QLineEdit("4")
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        attributes_label = QLabel('number of attributes: ')
        self.attr_number1 = QLineEdit("2")
        self.attr_number2 = QLineEdit("0")
        self.attr_number3 = QLineEdit("1")
        vbox.addWidget(attributes_label, 1, 3)
        vbox.addWidget(self.attr_number1, 1, 4)
        vbox.addWidget(self.attr_number2, 1, 5)
        vbox.addWidget(self.attr_number3, 1, 6)

        # line 2
        node_1 = QLabel('node ')
        self.node_1 = QLineEdit('1')
        vbox.addWidget(node_label, 2, 1)
        vbox.addWidget(self.node_number, 2, 2)

        northEast = QLabel('north east: ')
        self.northEast = QLineEdit("lng , lat")
        vbox.addWidget(northEast, 2, 3)
        vbox.addWidget(self.northEast, 2, 4)
        node_attr= QLabel('node attribute: ')
        self.node_attr = QLineEdit('2')
        vbox.addWidget(node_attr, 2, 5)
        vbox.addWidget(self.node_attr, 2, 6)




        # line 3
        node_1 = QLabel('node ')
        self.node_1 = QLineEdit('1')
        vbox.addWidget(node_1, 3, 1)
        vbox.addWidget(self.node_1, 3, 2)

        southWest = QLabel('south west: ')
        self.southWest = QLineEdit("lng , lat")
        vbox.addWidget(southWest, 3, 3)
        vbox.addWidget(self.southWest, 3, 4)
        node_attr = QLabel('node attribute: ')
        self.node_attr = QLineEdit('2')
        vbox.addWidget(node_attr, 2, 5)
        vbox.addWidget(self.node_attr, 2, 6)
        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # line 1
        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        node_label = QLabel('Node Number')
        self.node_number = QLineEdit()
        vbox.addWidget(node_label, 1, 1)
        vbox.addWidget(self.node_number, 1, 2)

        # vbox.addWidget(radiobutton)

        # vbox.addWidget( myQLabel)

        # radiobutton = QRadioButton("RadioButton 2")
        # vbox.addWidget(radiobutton)
        #
        # radiobutton = QRadioButton("RadioButton 3")
        # vbox.addWidget(radiobutton)
        #
        # radiobutton = QRadioButton("RadioButton 4")
        # vbox.addWidget(radiobutton)
