#!/usr/bin/env python3

import cv2
import sys
import platform
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
        # Connect slider for Hue parameter to its function
        self.ui.hue_horizontalSlider.valueChanged.connect(self.adjustHue)
        # Connect slider for Saturation parameter to its function
        self.ui.saturation_horizontalSlider.valueChanged.connect(self.adjustSaturation)
        # Connect slider for Value parameter to its function
        self.ui.value_horizontalSlider.valueChanged.connect(self.adjustValue)

    # Function to Adjust hue slider
    def adjustHue(self, value):
        self.ui.hue_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustSaturation(self, value):
        self.ui.saturation_lineEdit.setText(str(value))

    # Function to Adjust hue slider
    def adjustValue(self, value):
        self.ui.value_lineEdit.setText(str(value))
    #     # When checked connect the appropriate checkboxes to the corresponding function
    #     self.ui.checkBox_p1.stateChanged.connect(self.p1)
    #     # On toolbutton click execute the find_directory function
    #     self.ui.toolButton.clicked.connect(self.find_directory)
    #     # On append_button click execute the execute_append function
    #     self.ui.append_button.clicked.connect(self.execute_append)
    #     # On reset_button click execute the execute_reset function
    #     self.ui.reset_button.clicked.connect(self.execute_reset)
    #     # On execute_button click execute the execute_abort function
    #     self.ui.abort_button.clicked.connect(self.execute_abort)

    # # Function to append the first parameter to the file
    # def p1(self, checked):
    #     statement = "<launch> parameter 1 placeholder </launch>"
    #     if checked:
    #         self.ui.file_preview.append(statement)
    #     else:
    #         self.ui.file_preview.undo()

    # # Function to append file to preview

    # def execute_append(self):
    #     # Select all the text in the file editor
    #     self.ui.file_editor.selectAll()
    #     # Cut all the selected text in the file editor
    #     self.ui.file_editor.cut()
    #     # Append an empty line in the file preview
    #     self.ui.file_preview.append("")
    #     # Move to the beginning of the next empty block
    #     self.ui.file_preview.moveCursor(QtGui.QTextCursor.NextBlock)
    #     # Paste all the copied text into the file preview
    #     self.ui.file_preview.paste()
    #     # Append an empty line in the file preview
    #     self.ui.file_preview.append("")

    # # Function to find the directory to save file
    # def find_directory(self):
    #     # Pop open file explorer so user can select the directory they want to use
    #     directory = QtWidgets.QFileDialog.getExistingDirectory()
    #     # Preview the directory in the File Path window
    #     self.ui.text_directory_preview.setText(directory)
    #     self.ui.text_directory_preview.home(True)
    #     # On build_button click execute the execute_build function
    #     self.ui.build_button.clicked.connect(self.execute_build)

    # # Function to build the file and save it to the specified directory
    # def execute_build(self):
    #     # If filename is modified then allow the build to execute
    #     if (self.ui.file_name_input.isModified() == True):
    #         # Read the users input for File Name
    #         fileName = self.ui.file_name_input.text()
    #         # File Path where the file will be saved
    #         fileDir = self.ui.text_directory_preview.text()
    #         # Append the File Name to the File Path
    #         completeName = path.join(fileDir, fileName)
    #         # Create & open the writable output file
    #         outFile = open(completeName, "w")
    #         # Write the contents of the File Preview into the created file
    #         outFile.write(str(self.ui.file_preview.toPlainText()))
    #         # Close the file
    #         outFile.close()
    #         print("File Name: " + fileName)
    #         print("Is Saved In Directory:" + fileDir)

    # # Function to (Reset) the Config Manager
    # def execute_reset(self):
    #     # Uncheck all check boxes
    #     self.ui.checkBox_p1.setChecked(False)
    #     # Clear all the text in the file editor
    #     self.ui.file_editor.clear()
    #     # Clear all the text in the file preview
    #     self.ui.file_preview.clear()
    #     # Clear the filename being displayed
    #     self.ui.file_name_input.clear()
    #     # Clear the current directory being displayed
    #     self.ui.text_directory_preview.clear()

    # # Function to (Close) the Config Manager
    # def execute_abort(self):
    #     self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
