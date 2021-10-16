import os
import sys

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout,
    QWidget, QPushButton,
    QLabel, QLineEdit,
    QPlainTextEdit, QGroupBox,
    QCheckBox, QGridLayout, QMessageBox
)
from PyQt5 import QtGui, QtCore
from pyqtlet import L, MapWidget
import json

from StartDialog import CustomDialog
from nc2bin import NetcdfToBin
from utils import check_path, gradient, bounding_box, is_inside


class MapWindow(QWidget):
    def __init__(self):
        # Setting up the widgets and layout
        super().__init__()
        self.setWindowTitle('Grid Generator')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.mapWidget = MapWidget()
        self.layout = QGridLayout()
        self.layout.addWidget(self.mapWidget)
        self.setLayout(self.layout)
        dlg = CustomDialog()
        if dlg.exec():
            print("Success!")
            # t, path = check_path()
            path = "/home/amd/work/awi/repo/chile_30sec.nc"
            t = 'netcdf'
            print(path)
            if t == 'netcdf':
                nc = NetcdfToBin(path)
                data = nc.data
                print(data)

                # gradient(data['topo'], os.path.dirname(data['topo_path']))
                self.bound = [
                    [data['lat_max'], data['lon_min']],
                    [data['lat_min'], data['lon_max']]
                ]
        else:
            print("Cancel!")
            self.close()
            exit(1)
        # TODO get bounds from netCDF

        self.map = L.map(self.mapWidget)
        self.map.setView([3.515625, 31.052934], 2)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map)
        # print(self.map._onClick(self.map.clicked))
        self.editableLayers = L.featureGroup()
        self.editableLayers.addTo(self.map)
        self.drawControl = L.control().draw(options={
            'draw': {
                'polygon': True,
                'polyline': False,
                'rectangle': False,
                'circle': False
            },
            'edit': {
                'featureGroup': self.editableLayers
            }})
        self.map.addControl(self.drawControl)
        self.map.clicked.connect(lambda x: self.popup(x))
        self.map.drawCreated.connect(lambda x: self.draw_(x))
        self.draw_bounds(self.bound, "global", options={"color": "#ff7800", "weight": 3})
        # self.map.fitBounds(self.bound)
        self.polygon = {}
        self.points = []
        # START DIALOG

        # input box 1
        self.project_name = os.getenv("project_name")
        self.groupbox = QGroupBox(self.project_name)
        self.groupbox.setCheckable(True)
        self.layout.addWidget(self.groupbox)
        vbox = QGridLayout()
        self.groupbox.setLayout(vbox)
        self.checkbox = QCheckBox("Global")
        self.checkbox.setChecked(True)
        self.draw_polygon = QPushButton("Draw Polygon")
        self.draw_polygon.clicked.connect(self.start_draw_polygon)
        self.draw_polygon.setEnabled(False)
        vbox.addWidget(self.checkbox, 2, 1)
        vbox.addWidget(self.draw_polygon, 2, 2)
        self.input01 = QLineEdit(",".join([str(i) for i in self.bound]))
        self.input01.setReadOnly(True)
        vbox.addWidget(self.input01, 2, 3)
        self.checkbox.stateChanged.connect(lambda: self.checkButt(self.checkbox, self.input01))

        # button
        # self.button_select_point = QPushButton(self)
        # font = QtGui.QFont()
        # font.setFamily("Bauhaus 93")
        # font.setPointSize(10)
        # self.button_select_point.setFont(font)
        # self.button_select_point.setGeometry(QtCore.QRect(100, 20, 200, 50))
        # self.button_select_point.setText("Select one point")
        # self.button_select_point.clicked.connect(self.addMarker)
        # self.label = QLabel()
        # self.layout.addWidget(self.button_select_point)
        # self.layout.addWidget(self.label)

        # Create textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        self.layout.addWidget(self.textbox)

        self.show()

    def popup(self, x):
        print(x)
        # L.p .popup().setLatLng(x)
        # .setContent('<p>Hello world!<br />This is a nice popup.</p>')
        # .openOn(map);

    def draw_bounds(self, bounds, name, options=None):
        if options is None:
            options = {}
        marker = L.rectangle(bounds, options=options)
        marker.setObjectName(name)
        self.drawControl.featureGroup.addLayer(marker)
        # self.map.addLayer(marker)

    def draw_(self, e):
        if e['layerType'] == "polygon":
            self.remove_shape()
            self.remove_shape('Rectangle', n=None)

            bbx = e['layer']['_bounds']
            self.polygon['boundingbox'] = [[bbx['_northEast']['lat'], bbx['_northEast']['lng']],
                                           [bbx['_southWest']['lat'],
                                            bbx['_southWest']['lng']]]
            # print(is_inside(self.bound, self.polygon['boundingbox']))
            self.draw_bounds(self.polygon['boundingbox'], 'regional',
                             options={'color': 'black', 'weight': '3', 'dashArray': '20, 20', 'dashOffset': '0'})
            if is_inside(self.bound, self.polygon['boundingbox']):
                self.warning_box("the boundingbox of the polygon is overlapping the data bounds")
                self.remove_shape(n=1)
                self.remove_shape('Rectangle', 1)
            self.input01.setText(str(self.polygon['boundingbox']))

        # self.drawControl.featureGroup.toGeoJSON(lambda x: self.get_layer(x))
        # print(e)

        # if len([p for p in self.layers if 'Polygon' in p.keys()]) > 0:
        #     self.map.removeLayer(self.drawControl.featureGroup.getLayer())

    def get_layer(self, e):
        if len(e['features']) > 0:
            try:
                self.layers.append({
                    e['features'][-1]['geometry']['type']: e['features'][-1]['geometry']['coordinates']
                })
            except KeyError as er:
                print(er)

    def warning_box(self, text="warning!"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning Message")
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.exec_()

    def start_draw_polygon(self):
        script = """
        document.querySelector('.leaflet-draw-draw-polygon').click();
        """

        self.map.runJavaScript(script)

    def checkButt(self, box, input):
        print(box.isChecked())
        if box.isChecked():
            input.setReadOnly(True)
            input.setText(str(self.bound))
            self.draw_polygon.setEnabled(False)
        else:
            self.draw_polygon.setEnabled(True)
            input.setReadOnly(False)

    def project_name_changed(self):
        self.groupbox.setTitle(self.project_name_input.text())

    def remove_shape(self, shape='Polygon', n=-1):
        pols = [pol for pol in self.drawControl.featureGroup.layers if
                str(shape) in pol.__class__.__name__ and pol.objectName() != 'global']
        for p in pols:
            print(p.objectName())
        if len(pols) > 0:
            [self.drawControl.featureGroup.removeLayer(p) for p in pols[:n]]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())
