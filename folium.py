# import json
# import os
# import sys
# from pathlib import Path
# import io
# from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
# import folium
# CURRENT_DIRECTORY = Path(__file__).resolve().parent
#
#
# class MapManager(QtCore.QObject):
#     clicked = QtCore.pyqtSignal(float, float)
#
#     @QtCore.pyqtSlot(str, str)
#     def receive_data(self, message, json_data):
#         data = json.loads(json_data)
#         if message == "click":
#             self.clicked.emit(data["lat"], data["lng"])
#
#
# class Widget(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self._was_clicked = False
#
#         self.button = QtWidgets.QPushButton("Press me")
#         self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
#
#         self.view = QtWebEngineWidgets.QWebEngineView()
#         map_manager = MapManager(self)
#         channel = QtWebChannel.QWebChannel(self.view)
#         channel.registerObject("map_manager", map_manager)
#         self.view.page().setWebChannel(channel)
#         filename = os.fspath(CURRENT_DIRECTORY / "index.html")
#         url = QtCore.QUrl.fromLocalFile(filename)
#         self.view.load(url)
#
#         lay = QtWidgets.QVBoxLayout(self)
#         lay.addWidget(self.button)
#         lay.addWidget(self.label)
#         lay.addWidget(view)
#
#         map_manager.clicked.connect(self.handle_map_clicked)
#         self.button.clicked.connect(self.handle_button_clicked)
#
#     def handle_map_clicked(self, lat, lng):
#         if self._was_clicked:
#             self.label.setText(f"latitude: {lat} longitude: {lng}")
#         self._was_clicked = False
#
#     def handle_button_clicked(self):
#         self._was_clicked = True
#
#
# # if __name__ == "__main__":
# #     app = QtWidgets.QApplication(sys.argv)
# #
# #     w = Widget()
# #     w.show()
# #
# #     sys.exit(app.exec_())
#
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     #     app = QtWidgets.QApplication(sys.argv)
#
#     m = folium.Map(
#         location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13
#     )
#
#     data = io.BytesIO()
#     m.save(data, close_file=False)
#
#     # w = QtWebEngineWidgets.QWebEngineView()
#     w = Widget()
#     w.view.setHtml(data.getvalue().decode())
#     w.resize(640, 480)
#     w.show()
#
#     sys.exit(app.exec_())

import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        print(msg)  # Check js errors
        if 'coordinates' in msg:
            self.parent.handleConsoleMessage(msg)


class FoliumDisplay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Grid Generator')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        coordinate = (51.301100, 5.272991)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=4,
            location=coordinate)

        # Add Custom JS to folium map
        m = self.add_customjs(m)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()  # start web engine
        page = WebEnginePage(self)
        webView.setPage(page)
        webView.setHtml(data.getvalue().decode())  # give html of folium map to webengine
        layout.addWidget(webView)

        #### CEATE SELECT  BUTTON
        self.button_select_point = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(10)
        self.button_select_point.setFont(font)

        self.button_select_point.setGeometry(QtCore.QRect(100, 20, 200, 50))
        self.button_select_point.setText("Select one point")
        self.button_select_point.clicked.connect(self.clicked_button_select_point)

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.button_select_point)
        layout.addWidget(self.label)

    def add_customjs(self, map_object):
        my_js2 = f""" var j =[] """
        my_js = f"""{map_object.get_name()}.on("click",
                 function (e) {{
                    var data = `{{"coordinates": ${{JSON.stringify(e.latlng)}}}}`;
                    j.push(data)
                    map_object.get_name().simple_marker(location=[data['coordinates']['lat'] data['coordinates']['lng']], popup='Camp Muir')
                    console.log(j)}});"""
        e2 = Element(my_js2)
        e = Element(my_js)
        html = map_object.get_root()
        html.script.get_root().render()
        # Insert new element or custom JS
        html.script._children[e2.get_name()] = e2
        html.script._children[e.get_name()] = e

        return map_object

    def clicked_button_select_point(self):
        print("Clicked")

    def handleConsoleMessage(self, msg):
        data = json.loads("[ " + msg + " ]")
        print("data....", data)

        for i in range(len(data)):
            lat = data[i]['coordinates']['lat']
            lng = data[i]['coordinates']['lng']
            coords = f"latitude: {lat} longitude: {lng}"
            self.label.setText(coords)

    def start():
        w = FoliumDisplay()
        w.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = FoliumDisplay()
    w.show()
    sys.exit(app.exec_())
