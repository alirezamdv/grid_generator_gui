import sys
import os
import configparser
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QCheckBox,
    QPushButton, QGridLayout,
    QDialogButtonBox, QVBoxLayout,
    QLabel, QGroupBox, QComboBox
)

from utils import PathValidator


def get_configs():
    parser = configparser.ConfigParser()
    parser.read("./config.ini")
    return parser.get("global_configs", "projects").split(",")


class CustomDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grid Generator initializer!")

        QBtn = QDialogButtonBox.Open | QDialogButtonBox.Cancel
        self.ITEMS = get_configs()
        self.buttonBox = QDialogButtonBox(QBtn)
        self.layout = QVBoxLayout()
        self.validation_label = QLabel()
        self.validation_label.setStyleSheet("color: rgb(255, 0, 0);")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # input box 1
        self.groupbox = QGroupBox("Project Inputs: ")
        self.layout.addWidget(self.groupbox)
        vbox = QGridLayout()
        self.groupbox.setLayout(vbox)
        project_name_label = QLabel("Project Name: ")
        self.cb = QComboBox()
        c = len([un for un in self.ITEMS if "untitled" in un.split("_")]) + 1
        self.cb.addItem("untitled" + "_" + str(c))
        os.environ["project_name"] = "untitled" + "_" + str(c)
        self.cb.addItems(self.ITEMS)
        self.cb.setEditable(True)
        self.cb.currentIndexChanged.connect(self.selectionchange)
        # self.project_name_input = QLineEdit("untitled")
        # self.project_name_input.editingFinished.connect(self.project_name_changed)
        vbox.addWidget(project_name_label, 1, 1)
        vbox.addWidget(self.cb, 1, 2)

        self.netCDF_checkBox = QCheckBox("read Topography from NetCDF ")
        self.netCDF_checkBox.setChecked(True)
        self.netCDF_checkBox.toggled.connect(self.disable_inputs)
        vbox.addWidget(self.netCDF_checkBox, 2, 1)
        self.netCDF_path = QLineEdit("path to netCDF!")
        self.netCDF_path.setObjectName("netcdf_path")
        self.netCDF_path.editingFinished.connect(lambda: self.path_changed(self.netCDF_path))
        vbox.addWidget(self.netCDF_path, 2, 2)
        lon_label = QLabel("path to binary file of longitude(.bin32): ")
        lat_label = QLabel("path to binary file of latitude(.bin32): ")
        topo_label = QLabel("path to binary file of topography(.bin32): ")
        grad_label = QLabel("path to binary file of grade(.bin32): ")

        self.longitude_path = QLineEdit()
        self.longitude_path.setObjectName("longitude_path")
        self.longitude_path.editingFinished.connect(lambda: self.path_changed(self.longitude_path))
        self.latitude_path = QLineEdit()
        self.latitude_path.setObjectName("latitude_path")
        self.latitude_path.editingFinished.connect(lambda: self.path_changed(self.latitude_path))
        self.topography_path = QLineEdit()
        self.topography_path.setObjectName("topography_path")
        self.topography_path.editingFinished.connect(lambda: self.path_changed(self.topography_path))

        self.grad_path = QLineEdit()
        self.grad_path.setObjectName("grad_path")
        self.grad_path.editingFinished.connect(lambda: self.path_changed(self.grad_path))

        self.longitude_path.setDisabled(True)
        self.latitude_path.setDisabled(True)
        self.topography_path.setDisabled(True)
        self.grad_path.setDisabled(True)

        vbox.addWidget(lon_label, 3, 1)
        vbox.addWidget(self.longitude_path, 3, 2)

        vbox.addWidget(lat_label, 4, 1)
        vbox.addWidget(self.latitude_path, 4, 2)

        vbox.addWidget(topo_label, 5, 1)
        vbox.addWidget(self.topography_path, 5, 2)

        vbox.addWidget(grad_label, 6, 1)
        vbox.addWidget(self.grad_path, 6, 2)

        # self.input01.setReadOnly(True)
        # vbox.addWidget(self.input01, 2, 2)
        # self.checkbox.stateChanged.connect(lambda: self.checkButt(self.checkbox, self.input01))
        # message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(self.groupbox)
        self.layout.addWidget(self.validation_label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def selectionchange(self, i):
        item = self.cb.itemText(i)
        if item not in self.ITEMS:
            self.ITEMS += [item]
            os.environ["projects_"] = ",".join(self.ITEMS)
        os.environ["project_name"] = self.cb.itemText(i)

    def disable_inputs(self):
        if self.netCDF_checkBox.isChecked():
            self.netCDF_path.setDisabled(False)
            self.longitude_path.setDisabled(True)
            self.latitude_path.setDisabled(True)
            self.topography_path.setDisabled(True)
            self.grad_path.setDisabled(True)
        else:
            self.netCDF_path.setDisabled(True)
            self.longitude_path.setDisabled(False)
            self.latitude_path.setDisabled(False)
            self.topography_path.setDisabled(False)
            self.grad_path.setDisabled(False)

    def path_changed(self, x):
        if not os.path.isfile(x.text().strip()):
            x.setStyleSheet("color: rgb(255, 0, 0);")
            self.validation_label.setText(f'please enter valid path for {x.objectName()}!')
        else:
            x.setStyleSheet("color: rgb(0, 0, 0);")
            self.validation_label.setText('')
            os.environ[x.objectName()] = x.text().strip()
