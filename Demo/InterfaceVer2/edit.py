import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5 import uic
import PyQt5.QtCore as qtc
import sqlite3
from sqlite3 import Error
import hashlib as h
import sys

class Teacher(qtw.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("teacher.ui", self)
        self.selectSemester.currentIndexChanged.connect(self.change)
    def change(self):
        print(self.selectSemester.currentText())

app = qtw.QApplication([])
teacher = Teacher()
teacher.show()
app.exec_()

