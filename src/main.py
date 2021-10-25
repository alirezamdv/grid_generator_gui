"""
alireza.mahdavi@awi.de
a.mahdavi@outlook.com
"""

import os
import subprocess
import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QLineEdit,
    QGroupBox,
    QCheckBox, QGridLayout, QMessageBox, QComboBox
)
from pyqtlet import L, MapWidget

from src.Areas import AreaBox
from src.StartDialog import CustomDialog, PolyDialog
from src.nc2bin import NetcdfToBin
from src.replace_global_constants import replace_global_Constants
from src.utils import check_path, is_inside, create_project
from src.polygons.polygons import polygons as pols


def warning_box(type="Error", text="warning!"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning Message")
    msg.setText(type)
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
            t, path = check_path()
            self.project_name = os.getenv("project_name")
            print(os.getenv("topography_path"))
            # path = "/home/amd/work/awi/repo/chile_30sec.nc"
            # t = 'netcdf'
            print(path)
            if t == 'netcdf':
                self.nc = NetcdfToBin(path)
                self.data = self.nc.data

            # gradient(data['topo'], os.path.dirname(data['topo_path']))
            self.bound = {
                'bound': [[self.data['lat_max'], self.data['lon_min']],
                          [self.data['lat_min'], self.data['lon_max']]],
                'poly': [[self.data['lat_max'], self.data['lon_min']], [self.data['lat_max'], self.data['lon_max']],
                         [self.data['lat_min'], self.data['lon_max']], [self.data['lat_min'], self.data['lon_min']]]
            }
            create_project(self.project_name)
            self.project_path = os.getenv("project_path")
        else:
            print("Cancel!")
            self.close()
            exit(1)

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
            }
        })
        self.map.addControl(self.drawControl)
        self.map.clicked.connect(lambda x: self.popup(x))
        self.map.drawCreated.connect(self.draw_)
        # self.map.drawEdited.connect(self.draw_)
        self.draw_bounds(self.bound['poly'], "global", options={"color": "#ff7800", "weight": 3})
        # self.map.fitBounds(self.bound)
        self.polygon = self.bound['poly']
        self.points = []
        # START DIALOG

        # input box 1
        self.groupbox = QGroupBox(self.project_name)
        self.groupbox.setCheckable(True)
        self.layout.addWidget(self.groupbox)
        self.vbox = QGridLayout()
        self.groupbox.setLayout(self.vbox)
        self.checkbox = QCheckBox("Use the datasets bounds as Polygon")
        self.checkbox.setChecked(True)
        self.draw_polygon = QPushButton("Draw Polygon")
        self.draw_polygon.clicked.connect(self.start_draw_polygon)
        self.draw_polygon.setEnabled(False)
        self.vbox.addWidget(self.checkbox, 2, 1)
        self.vbox.addWidget(self.draw_polygon, 2, 2)
        self.poly_edit = QPushButton("edit the poly file")
        self.poly_edit.clicked.connect(self.poly_text_edit)
        self.vbox.addWidget(self.poly_edit, 2, 4)
        self.dropdown = QComboBox()
        self.dropdown.addItem("select a polygon")
        self.dropdown.addItems(pols.keys())
        self.dropdown.currentIndexChanged.connect(self.dropdown_changed)
        self.vbox.addWidget(self.dropdown, 2, 5)
        self.ref_factor_label = QLabel("Refinement Factor c_t [sec]: ")
        self.ref_factor = QLineEdit("10")

        self.steepness_label = QLabel("Steepness refinement ratio [1/sec] (c_grad = ratio * c_t): ")
        self.steepness = QLineEdit("0.5")

        self.min_depth_label = QLabel("Minimal depth dep_min [m] (finest resolution = c_t * sqrt(g * dep_min): ")
        self.min_depth = QLineEdit("0.1")

        self.c_res_label = QLabel("Coarsest resolution: ")
        self.c_res = QLineEdit("2000.")
        self.f_res_label = QLabel("Finest resolution: ")
        self.f_res = QLineEdit("200.")
        self.coast_res_label = QLabel("Coastal resolution: ")
        self.coast_res = QLineEdit("1000.")

        self.areas = AreaBox(self.start_draw_point, warning_box)

        self.save_butt = QPushButton("save")
        self.save_butt.clicked.connect(self.save)

        self.run_butt = QPushButton("run")
        self.run_butt.clicked.connect(self.run)

        self.vbox.addWidget(self.ref_factor_label, 3, 1)
        self.vbox.addWidget(self.ref_factor, 3, 2)
        self.vbox.addWidget(self.steepness_label, 3, 3)
        self.vbox.addWidget(self.steepness, 3, 4)
        self.vbox.addWidget(self.min_depth_label, 3, 5)
        self.vbox.addWidget(self.min_depth, 3, 6)
        self.vbox.addWidget(self.c_res_label, 4, 1)
        self.vbox.addWidget(self.c_res, 4, 2)
        self.vbox.addWidget(self.f_res_label, 4, 3)
        self.vbox.addWidget(self.f_res, 4, 4)
        self.vbox.addWidget(self.coast_res_label, 4, 5)
        self.vbox.addWidget(self.coast_res, 4, 6)

        self.vbox.addWidget(self.areas, 5, 3, 3, 3)

        self.vbox.addWidget(self.save_butt, 6, 1)
        self.vbox.addWidget(self.run_butt, 6, 2)

        self.checkbox.stateChanged.connect(lambda: self.global_checked(self.checkbox))
        self.poly()
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
        with open(f'{self.project_path}{self.project_name}.poly', 'r+') as poly:
            content = poly.read()
            dlg = PolyDialog(content)
            if dlg.exec():
                poly.seek(0)
                poly.write(dlg.txt)
                poly.truncate()

    def dropdown_changed(self, i):
        item = self.dropdown.itemText(i)
        if item in pols.keys():
            self.remove_shape(n=None)
            self.remove_shape('Rectangle', n=None)
            self.polygon = pols[item]
            self.draw_bounds(self.polygon, 'bound', polygon=True)
            self.poly()

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
                warning_box(text="the bounding box of the polygon is overlapping the data bounds")
                # self.remove_shape(n=1)
                # self.remove_shape('Rectangle', 1)

            self.draw_bounds(bbx, 'regional', polygon=False,
                             options={'color': box_color, 'weight': '3', 'dashArray': '20, 20', 'dashOffset': '0'})
            # print(is_inside(self.bound, self.polygon['boundingbox']))
        if e['layerType'] == 'marker':
            point = e['layer']['_latlng']
            print(e)
            self.areas.lat.setText(str(point['lat']))
            self.areas.long.setText(str(point['lng']))
            self.draw_circle(point, radius=float(self.areas.p_area_inner.text()) * 100, alpha=0.4)
            self.draw_circle(point, radius=float(self.areas.p_area_outer.text()) * 100, color='white')

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

    def start_draw_point(self):
        script = """
        document.querySelector('.leaflet-draw-draw-marker').click();
        """

        self.map.runJavaScript(script)

    def draw_circle(self, point, radius, color="blue", alpha=0.2):
        circle = L.circle(point, {
            'radius': radius,
            'color': color,
            'fillOpacity': alpha,
        })
        self.map.addLayer(circle)

    def global_checked(self, box):
        if box.isChecked():
            self.draw_polygon.setEnabled(False)
            self.polygon = self.bound['poly']
            self.poly()
        else:
            self.draw_polygon.setEnabled(True)

    def project_name_changed(self):
        self.groupbox.setTitle(self.project_name_input.text())

    def remove_shape(self, shape='Polygon', n=-1):
        _shapes = [pol for pol in self.drawControl.featureGroup.layers if
                   str(shape) in pol.__class__.__name__ and pol.objectName() != 'global']
        if len(_shapes) > 0:
            [self.drawControl.featureGroup.removeLayer(p) for p in _shapes[:n]]

    def mesh_setup(self):
        n_p_areas = len(self.areas.areas)
        txt = ""
        txt += f'{self.c_res.text()}\n'
        txt += f'{self.f_res.text()}\n'
        txt += f'{self.coast_res.text()}\n'
        txt += f'0\n'
        txt += f'{n_p_areas}\n'
        for i in range(n_p_areas):
            txt += f'{" ".join(self.areas.areas[i])}\n'

        with open(self.project_path + "mesh_setup.txt", 'w+') as f:
            f.write(txt)

    def modify_triangle_c(self):
        self.nc.get_data(write=True)
        p = self.nc.out_path
        lon = p + "/lon.bin32"
        lat = p + "/lat.bin32"
        topo = p + "/topo.bin32"
        grad = p + "/grad.bin32"
        lenLon = self.data['lon_len']
        lenLat = self.data['lat_len']
        replace_global_Constants(self.project_name, self.project_path, lenLat, lenLon, lon, lat, topo, grad)

    def save(self):
        print(self.areas.areas)
        self.mesh_setup()
        self.mesh_params()
        self.modify_triangle_c()
        print("saved...")

    def run(self):
        self.save()
        print(self.project_path)
        make_process = subprocess.Popen(["make", "clean", "all"], stderr=subprocess.STDOUT, cwd=self.project_path)
        if make_process.wait() != 0:
            print("ooops!")

    def save_point(self):
        pass

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
        with open(self.project_path + f'{self.project_name}.poly', 'w+') as poly:
            poly.write(txt)

    def mesh_params(self):
        path, file = os.path.split(self.nc.path)
        txt = "### ProjectName\n"
        txt += f'{self.project_name}\n'
        txt = "### ProjectPath\n"
        txt += f'{self.project_path}\n'
        txt = "### BathymetryName\n"
        txt += "Bathymetry_Name\n"
        txt += "### BathymetryPath\n"
        txt += f'{path}\n'
        txt += "### BathymetryDataSet\n"
        txt += f'{file}\n'
        txt += "### Refinement Factor c_t [sec] \n"
        txt += f'{self.ref_factor.text()}\n'
        txt += "### Steepness refinement ratio [1/sec] (c_grad = ratio * c_t)\n"
        txt += f'{self.steepness.text()}\n'
        txt += "### minimal depth dep_min [m] (finest resolution = c_t * sqrt(g * dep_min))\n"
        txt += f'{self.min_depth.text()}\n'
        with open(self.project_path + 'mesh_parameters.txt', 'w+') as m:
            m.write(txt)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = MapWindow()
#     sys.exit(app.exec_())
