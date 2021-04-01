#!/usr/bin/env python3

import cv2
import sys
import platform
import numpy as np
from os import system, path
from PyQt5 import QtCore, QtGui, QtWidgets
# Main window UI File
from depend import Ui_mainWindow

CAMPATH = 3


class VideoThread(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(CAMPATH)
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
        # Connect slider for Upper Hue parameter to its function
        self.ui.upper_hue_horizontalSlider.valueChanged.connect(self.adjustHueUpper)
        # Connect slider for Upper Saturation parameter to its function
        self.ui.upper_saturation_horizontalSlider.valueChanged.connect(self.adjustSaturationUpper)
        # Connect slider for Upper Value parameter to its function
        self.ui.upper_value_horizontalSlider.valueChanged.connect(self.adjustValueUpper)
        # Connect slider for Lower Hue parameter to its function
        self.ui.lower_hue_horizontalSlider.valueChanged.connect(self.adjustHueLower)
        # Connect slider for Lower Saturation parameter to its function
        self.ui.lower_saturation_horizontalSlider.valueChanged.connect(self.adjustSaturationLower)
        # Connect slider for Lower Value parameter to its function
        self.ui.lower_value_horizontalSlider.valueChanged.connect(self.adjustValueLower)
        #
        self.ui.test_pushButton.clicked.connect(self.parseCameraPath)
        #
        self.ui.reset_pushButton.clicked.connect(self.resetCameraPath)
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    # Function to Adjust hue slider
    def adjustHueUpper(self, value):
        self.ui.upper_hue_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustSaturationUpper(self, value):
        self.ui.upper_saturation_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustValueUpper(self, value):
        self.ui.upper_value_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustHueLower(self, value):
        self.ui.lower_hue_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustSaturationLower(self, value):
        self.ui.lower_saturation_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustValueLower(self, value):
        self.ui.lower_value_lineEdit.setText(str(value))

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    # Function to get camera path set by the user
    def parseCameraPath(self):
        # print(self.ui.camera_path_lineEdit.text())
        CAMPATH = int(self.ui.camera_path_lineEdit.text())

    # Function to reset camera path to 0
    def resetCameraPath(self):
        self.ui.camera_path_lineEdit.setText("0")

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
        # define range of color in HSV
        lower_H = self.ui.lower_hue_horizontalSlider.value()
        lower_S = self.ui.lower_saturation_horizontalSlider.value()
        lower_V = self.ui.lower_value_horizontalSlider.value()
        upper_H = self.ui.upper_hue_horizontalSlider.value()
        upper_S = self.ui.upper_saturation_horizontalSlider.value()
        upper_V = self.ui.upper_value_horizontalSlider.value()
        lower_bound = np.array([lower_H, lower_S, lower_V])
        upper_bound = np.array([upper_H, upper_S, upper_V])
        # Threshold the HSV image for target color
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
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


# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html
# https://docs.wpilib.org/en/stable/docs/software/vision-processing/wpilibpi/image-thresholding.html
