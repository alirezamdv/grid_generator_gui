import os
import sys

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout,
    QWidget, QPushButton,
    QLabel, QLineEdit,
    QPlainTextEdit, QGroupBox,
    QCheckBox, QGridLayout, QMessageBox, QDialog
)
from PyQt5 import QtGui, QtCore
from pyqtlet import L, MapWidget
import json

from PolyWidget import PolyBox
from ProjFactory import ProjFactory
from StartDialog import CustomDialog, PolyDialog
from nc2bin import NetcdfToBin
from utils import check_path, gradient, bounding_box, is_inside


def warning_box(text="warning!"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning Message")
    msg.setText("Error")
    msg.setInformativeText(text)
    msg.exec_()


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
            print(os.getenv("topography_path"))
            path = "/home/amd/work/awi/repo/chile_30sec.nc"
            t = 'netcdf'
            self.project_name = "alireza"
            print(path)
            if t == 'netcdf':
                nc = NetcdfToBin(path)
                self.data = nc.data
            # ProjFactory()

            # gradient(data['topo'], os.path.dirname(data['topo_path']))
            self.bound = {
                'bound': [[self.data['lat_max'], self.data['lon_min']],
                          [self.data['lat_min'], self.data['lon_max']]],
                'poly': [[self.data['lat_max'], self.data['lon_min']], [self.data['lat_max'], self.data['lon_max']],
                         [self.data['lat_min'], self.data['lon_max']], [self.data['lat_min'], self.data['lon_min']]]
            }
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
        self.map.drawCreated.connect(self.draw_)
        # self.map.drawEdited.connect(lambda x: print(x))
        self.draw_bounds(self.bound['poly'], "global", options={"color": "#ff7800", "weight": 3})
        # self.map.fitBounds(self.bound)
        self.polygon = self.bound['poly']
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
        self.poly_edit = QPushButton("edit the poly file")
        self.poly_edit.clicked.connect(self.poly_text_edit)
        vbox.addWidget(self.poly_edit, 2, 4)

        self.input01 = QLineEdit(",".join([str(i) for i in self.bound['bound']]))
        self.input01.setReadOnly(True)
        vbox.addWidget(self.input01, 2, 3)
        self.checkbox.stateChanged.connect(lambda: self.global_checked(self.checkbox, self.input01))

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
        # self.poly = PolyBox()
        self.poly()
        # self.layout.addWidget(self.poly)

        self.show()

    def popup(self, x):
        print(x)
        # L.p .popup().setLatLng(x)
        # .setContent('<p>Hello world!<br />This is a nice popup.</p>')
        # .openOn(map);

    # def draw_point(self, point):
    #     point = L.marker(point)
    #     self.drawControl.featureGroup.addLayer(point)

    def poly_text_edit(self):
        with open(f'{self.project_name}.poly', 'r+') as poly:
            content = poly.read()
            dlg = PolyDialog(content)
            if dlg.exec():
                poly.seek(0)
                poly.write(dlg.txt)
                poly.truncate()

    def draw_bounds(self, bounds, name, polygon=True, options=None):
        if options is None:
            options = {}
        if polygon:
            marker = L.polygon(bounds, options=options)
        else:
            marker = L.rectangle(bounds, options=options)
        marker.setObjectName(name)
        self.drawControl.featureGroup.addLayer(marker)
        # self.map.addLayer(marker)

    def draw_(self, e):
        if e['layerType'] == "polygon":
            self.remove_shape()
            self.remove_shape('Rectangle', n=None)
            box_color = 'red'
            _bbx = e['layer']['_bounds']
            _nodes = e['layer']['_latlngs']['0']
            bbx = [[_bbx['_northEast']['lat'], _bbx['_northEast']['lng']],
                   [_bbx['_southWest']['lat'],
                    _bbx['_southWest']['lng']]]
            print(is_inside(self.bound['bound'], bbx))
            if not is_inside(self.bound['bound'], bbx):
                box_color = 'black'
                self.polygon = [[_nodes[str(p)]['lat'], _nodes[str(p)]['lng']] for p in _nodes.keys()]
                self.poly()
            else:
                warning_box("the bounding box of the polygon is overlapping the data bounds")
                # self.remove_shape(n=1)
                # self.remove_shape('Rectangle', 1)

            self.draw_bounds(bbx, 'regional', polygon=False,
                             options={'color': box_color, 'weight': '3', 'dashArray': '20, 20', 'dashOffset': '0'})
            # print(is_inside(self.bound, self.polygon['boundingbox']))


            self.input01.setText(str(bbx))

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

    def start_draw_polygon(self):
        script = """
        document.querySelector('.leaflet-draw-draw-polygon').click();
        """

        self.map.runJavaScript(script)

    def global_checked(self, box, input):
        print(box.isChecked())
        if box.isChecked():
            input.setReadOnly(True)
            input.setText(str(self.bound))
            self.draw_polygon.setEnabled(False)
            self.polygon = self.bound['poly']
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

    def poly(self):
        n = len(self.polygon)
        # must be 2
        dimension = 2
        n_attributes = 0
        n_attribute_node = 2  # TODO get it from user
        # # of boundary markers (0 or 1)
        n_boundary_markers = 1
        txt = f'{n} {dimension} {n_attributes} {n_boundary_markers}\n'
        for i in range(1, n + 1):
            txt += f'{i} {self.polygon[i - 1][1]} {self.polygon[i - 1][0]} {n_attribute_node} \n'
        txt += f'{n} {n_boundary_markers}\n'
        for i in range(1, n + 1):
            if i == n:
                txt += f'{i} {i} {1} {n_boundary_markers}\n'
            else:
                txt += f'{i} {i} {i + 1} {n_boundary_markers}\n'
        txt += '0'
        with open(f'{self.project_name}.poly', 'w+') as poly:
            poly.write(txt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())
