from PyQt5.QtWidgets import *
import sys, os
import PyQt5
import json
import io
import creator
import detector
import Trainer
import cv2
import numpy as np

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Library'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(500, 500)

        # Add tabs
        self.tabs.addTab(self.tab1, "Add student")
        self.tabs.addTab(self.tab2, "Verify")

        # Create first tab
        self.createTab1()
        # Create second tab
        self.createTab2()
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        list = os.listdir("images")
        file_count = len(list)
        if(file_count>0):
            Trainer.train()


    def createTab1(self):
        self.formGroupBox = QGroupBox("Add new")
        self.formGroupBox.resize(300, 300);
        # creating spin box to select age
        self.ageSpinBar = QSpinBox()

        # creating combo box to select degree
        self.bodLineEdit = QDateEdit()

        # creating a line edit
        self.nameLineEdit = QLineEdit()

        # creating a line edit
        self.idLineEdit = QLineEdit()

        # creating a line edit
        self.classLineEdit = QLineEdit()

        # calling the method that create the form
        self.createForm()

        self.tab1.layout = QVBoxLayout(self)
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.saveData)
        self.tab1.layout.addWidget(self.formGroupBox)
        self.tab1.layout.addWidget(self.addButton)
        self.tab1.setLayout(self.tab1.layout)
    def createTab2(self):
        self.tab2.layout = QVBoxLayout(self)
        self.recoButton=QPushButton("Recognize")
        self.recoButton.clicked.connect(detector.detect)
        self.tab2.layout.addWidget(QLabel("Nhấn q để ngừng nhận diện"))
        self.tab2.layout.addWidget(self.recoButton)
        self.tab2.setLayout(self.tab2.layout)
    def createForm(self):
        # creating a form layout
        layout = QFormLayout()

        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Name"), self.nameLineEdit)

        # for degree and adding combo box
        layout.addRow(QLabel("ID"), self.idLineEdit)
        # for birthday
        layout.addRow(QLabel("Birthday"), self.bodLineEdit)
        # for age and adding spin box
        layout.addRow(QLabel("Class"), self.classLineEdit)

        # setting layout
        self.formGroupBox.setLayout(layout)

    def saveData(self):
        self.notify("Press Ok to take photo - Nhìn thẳng vào webcam")
        if(creator.takePhoto(self.idLineEdit.text())):
            file = open("data.txt", "ab")
            data = self.idLineEdit.text() + "-" + self.nameLineEdit.text() + "-" + self.classLineEdit.text() + "-" + self.bodLineEdit.text()+"\n"
            data=data.encode("utf8")
            file.write(data)
        Trainer.train()
    def notify(self, str):
        noti=QMessageBox()
        noti.setIcon(QMessageBox.Information)
        noti.setText(str)
        noti.setWindowTitle("Notification")
        noti.setStandardButtons(QMessageBox.Ok)
        noti.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    loadLabel('data.txt')
    print(targetName)
