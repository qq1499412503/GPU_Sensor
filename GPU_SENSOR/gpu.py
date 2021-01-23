# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from home import Ui_MainWindow
from about import Ui_Dialog
import sys
import pynvml
import time

class Backend(QThread):
    update_data = pyqtSignal(list)
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    def run(self):
        while True:
            temp = str(pynvml.nvmlDeviceGetTemperature(self.handle, pynvml.NVML_TEMPERATURE_GPU))
            name = str(pynvml.nvmlDeviceGetName(self.handle))
            meminfo = pynvml.nvmlDeviceGetMemoryInfo(self.handle)
            total = str(round(meminfo.total/1024**3,2))
            used = str(round(meminfo.used/1024**3,2))
            free = str(round(meminfo.free/1024**3,2))
            data = [{'temp':temp,'name':name,'total':total,'used':used,'free':free}]
            self.update_data.emit(data)
            time.sleep(1)





class About(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self, parent=None):
        super(About,self).__init__(parent)
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionAbout.triggered.connect(self.about_window)

    def about_window(self):
        widget = About()
        widget.exec_()

    def handleDisplay(self, data):
        self.ui.label_10.setText(data[0]['temp'] +' C'+ '\N{DEGREE SIGN}')
        self.ui.label_2.setText(data[0]['name'][2:-1])
        self.ui.label_4.setText(data[0]['total'] + '   GB')
        self.ui.label_6.setText(data[0]['used'] + '   GB')
        self.ui.label_8.setText(data[0]['free'] + '   GB')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    back = Backend()
    window = MainWindow()
    back.update_data.connect(window.handleDisplay)
    back.start()
    window.show()
    sys.exit(app.exec_())
    pynvml.nvmlShutdown()
