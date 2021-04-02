#!/usr/bin/env python3

import cv2
import sys
import platform
import numpy as np
from os import system, path
from PyQt5 import QtCore, QtGui, QtWidgets
# Main window UI File
from depend import Ui_mainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.show()
        # Connect slider for Upper Hue parameter to its function
        self.ui.upper_hue_horizontalSlider.valueChanged.connect(self.adjustHueUpper)
        # Connect upper hue line edit to slider function
        self.ui.upper_hue_lineEdit.returnPressed.connect(self.setHueUpper)
        # Connect slider for Upper Saturation parameter to its function
        self.ui.upper_saturation_horizontalSlider.valueChanged.connect(self.adjustSaturationUpper)
        # Connect upper saturation line edit to slider function
        self.ui.upper_saturation_lineEdit.returnPressed.connect(self.setSaturationUpper)
        # Connect slider for Upper Value parameter to its function
        self.ui.upper_value_horizontalSlider.valueChanged.connect(self.adjustValueUpper)
        # Connect upper value line edit to slider function
        self.ui.upper_value_lineEdit.returnPressed.connect(self.setValueUpper)
        # Connect slider for Lower Hue parameter to its function
        self.ui.lower_hue_horizontalSlider.valueChanged.connect(self.adjustHueLower)
        # Connect lower hue line edit to slider function
        self.ui.lower_hue_lineEdit.returnPressed.connect(self.setHueLower)
        # Connect slider for Lower Saturation parameter to its function
        self.ui.lower_saturation_horizontalSlider.valueChanged.connect(self.adjustSaturationLower)
        # Connect lower saturation line edit to slider function
        self.ui.lower_saturation_lineEdit.returnPressed.connect(self.setSaturationLower)
        # Connect slider for Lower Value parameter to its function
        self.ui.lower_value_horizontalSlider.valueChanged.connect(self.adjustValueLower)
        # Connect lower value line edit to slider function
        self.ui.lower_value_lineEdit.returnPressed.connect(self.setValueLower)
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    # Function to adjust upper hue slider
    def adjustHueUpper(self, value):
        self.ui.upper_hue_lineEdit.setText(str(value))

    # Function to force upper hue slider to given int
    def setHueUpper(self):
        val = int(self.ui.upper_hue_lineEdit.text())
        self.ui.upper_hue_horizontalSlider.setValue(val)

    # Function to adjust upper saturation slider
    def adjustSaturationUpper(self, value):
        self.ui.upper_saturation_lineEdit.setText(str(value))

    # Function to force upper saturation slider to given int
    def setSaturationUpper(self):
        val = int(self.ui.upper_saturation_lineEdit.text())
        self.ui.upper_saturation_horizontalSlider.setValue(val)

    # Function to adjust upper value slider
    def adjustValueUpper(self, value):
        self.ui.upper_value_lineEdit.setText(str(value))

    # Function to force upper value slider to given int
    def setValueUpper(self):
        val = int(self.ui.upper_value_lineEdit.text())
        self.ui.upper_value_horizontalSlider.setValue(val)

    # Function to adjust lower hue slider
    def adjustHueLower(self, value):
        self.ui.lower_hue_lineEdit.setText(str(value))

    # Function to force lower hue slider to given int
    def setHueLower(self):
        val = int(self.ui.lower_hue_lineEdit.text())
        self.ui.lower_hue_horizontalSlider.setValue(val)

    # Function to adjust lower saturation slider
    def adjustSaturationLower(self, value):
        self.ui.lower_saturation_lineEdit.setText(str(value))

    # Function to force lower saturation slider to given int
    def setSaturationLower(self):
        val = int(self.ui.lower_saturation_lineEdit.text())
        self.ui.lower_saturation_horizontalSlider.setValue(val)

    # Function to adjust lower value slider
    def adjustValueLower(self, value):
        self.ui.lower_value_lineEdit.setText(str(value))

    # Function to force lower value slider to given int
    def setValueLower(self):
        val = int(self.ui.lower_value_lineEdit.text())
        self.ui.lower_value_horizontalSlider.setValue(val)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    # Updates the image_label with a new OpenCV image
    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.label.setPixmap(qt_img)

    # Function to convert OpenCV output to QPixmap
    def convert_cv_qt(self, cv_img):
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
        h, w, ch = res.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(res.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)


class VideoThread(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # Set camera path and capture from web cam
        cap = cv2.VideoCapture(2)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # Terminate capture
        cap.release()

    def stop(self):
        # Sets run flag to False and waits for thread to finish
        self._run_flag = False
        self.wait()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
