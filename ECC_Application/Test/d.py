import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5 import uic
import PyQt5.QtCore as qtc
import sqlite3
from sqlite3 import Error
import hashlib as h
import sys

#region Database Server
class Server():
    def __init__(self):
        super().__init__()
        self.a = 10
        self.b = 10

server = Server()
print(server.a)