#!/usr/bin/env python3

import cv2
import sys
import platform
import numpy as np
from os import system, path
from PyQt5 import QtCore, QtGui, QtWidgets
# Main window UI File
from depend import Ui_mainWindow

hVal = 0
sVal = 0
vVal = 0


class VideoThread(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(2)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.show()
        # Connect slider for Hue parameter to its function
        self.ui.hue_horizontalSlider.valueChanged.connect(self.adjustHue)
        # Connect slider for Saturation parameter to its function
        self.ui.saturation_horizontalSlider.valueChanged.connect(self.adjustSaturation)
        # Connect slider for Value parameter to its function
        self.ui.value_horizontalSlider.valueChanged.connect(self.adjustValue)
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    # Function to Adjust hue slider
    def adjustHue(self, value):
        self.ui.hue_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustSaturation(self, value):
        self.ui.saturation_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustValue(self, value):
        self.ui.value_lineEdit.setText(str(value))

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([255, 255, 255])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(rgb_image, rgb_image, mask=mask)
        #rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = res.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(res.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

