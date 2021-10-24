"""
a.mahdavi@outlook.com
"""

import os
import configparser
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox


class PathValidator(QtGui.QValidator):
    def __init__(self, parent=None):
        super(PathValidator, self).__init__(parent)

    def validate(self, string, index):
        if not string:
            return QtGui.QValidator.Acceptable, string, index
        state = QtGui.QValidator.Acceptable
        if not os.path.exists(string):
            print(string)
            state = QtGui.QValidator.Invalid
        return state, string, index


def get_configs():
    parser = configparser.ConfigParser()
    parser.read("src/config.ini")
    return parser, parser.get("global_configs", "projects").split(",")


def write_configs(parser):
    with open("src/config.ini", "w") as f:
        parser.write(f)


def check_path():
    if os.getenv("netcdf_path"):
        return "netcdf", os.getenv("netcdf_path")
    if os.getenv("longitude_path") and os.getenv("latitude_path") \
            and os.getenv("topography_path") and os.getenv("grad_path"):
        return 'bin', {'lon': os.getenv("longitude_path"),
                       'lat': os.getenv("latitude_path"),
                       'topo': os.getenv("topography_path"),
                       'grad': os.getenv("grad_path")}

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText('I cant find either netCDF file or the binary files!')
    msg.setWindowTitle("Error")
    msg.exec_()


def gradient(tp, path) -> None:
    # calculate topography gradient
    tpx, tpy = np.gradient(tp)
    tpxy = np.sqrt(np.power(tpx, 2) + np.power(tpy, 2))  # absolute value of the gradient
    tpxy = tpxy / np.max(np.max(tpxy))  # normalise to 1
    with open(path + '/grad.bin32', 'wb') as f:
        # metadata[f'{var}_binary_len'] = len(np_arr.tobytes())
        f.write(tpxy.tobytes())
        print(f'successfully wrote the grade with {tpxy.shape} shape to grad.bin32. ')


def get_len_of_variable_from_binary(path) -> int:
    return len(np.fromfile(path))


def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return [(min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))]


def create_project(name):
    parser, proj = get_configs()
    os.makedirs("./" + name, exist_ok=True)
    os.environ['project_path'] = "./" + name + "/"
    proj.append(name)
    parser.set("global_configs", "projects", ','.join(proj))
    write_configs(parser)


def is_inside(box1, box2):
    py1, px1 = box2[0]
    py2, px2 = box2[1]
    y1, x1 = box1[0]
    y2, x2 = box1[1]
    logic1 = (x1 < px1 < x2 or y1 < py1 < y2)
    logic2 = (x1 < px2 < x2 or y1 < py2 < y2)
    # print(box1, '\n', box2)
    # print(f"point({py1, px1} is inside {box1}) ", logic1, '\n')
    # print(f"point({py2, px2} is inside {box1}) ", logic1, '\n')
    return not (logic1 and logic2)
