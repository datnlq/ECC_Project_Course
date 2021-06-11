import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5 import uic
import PyQt5.QtCore as qtc
import sqlite3
from sqlite3 import Error
import hashlib as h
import sys

class Server():
    def __init__(self):
        super().__init__()
        try:
            self.conn = sqlite3.connect("ECCapp.db")
            self.cur = self.conn.cursor()
        # print(sqlite3.version)
        except Error as e:
            print(e)

    def selectStudent(self, username):
        self.cur.execute("SELECT * FROM STUDENT WHERE StudentID=?", (username,))

        row = self.cur.fetchone()
        return row

    def studentResult(self, username, semester, schoolyear):
        self.cur.execute("SELECT md.ModuleID, md.NameSubject, md.NumCredit, rs.ProcessPoint, rs.MidPoint, rs.LabPoint, rs.EndPoint, rs.AveragePoint, rs.Note FROM MODULE md, RESULT rs WHERE md.ModuleID = rs.ModuleID and rs.StudentID = ? and md.Semester = ? and md.SchoolYear = ?", (username, semester, schoolyear,))
        self.row = self.cur.fetchall()
        return self.row

    def selectTeacher(self, username):
        self.cur.execute("SELECT * FROM TEACHER WHERE TeacherID=?", (username,))
        self.row = self.cur.fetchone()
        return self.row

    def selectSubjectList(self, username, semester, schoolyear):
        self.cur.execute("SELECT ModuleID, NameSubject, NumStudent FROM MODULE WHERE TeacherID = ? and Semester = ? and SchoolYear = ?", (username, semester, schoolyear,))

        self.row = self.cur.fetchall()
        return self.row

    def selectListStudent(self, nameModule):
        self.cur.execute("SELECT st.StudentID, st.Fullname, st.Sex, rs.ProcessPoint, rs.MidPoint, rs.LabPoint,EndPoint,rs.AveragePoint,rs.Note FROM STUDENT st, RESULT rs, MODULE md WHERE st.StudentID = rs.StudentID and rs.ModuleID = md.ModuleID and md.ModuleID = ?", (nameModule,))

        self.row = self.cur.fetchall()
        return self.row

    def checkSign(self, passCheck, passInput):
        print(passInput)
        hash_passInput = h.sha1(bytes(passInput, 'utf-8')).hexdigest()
        print(hash_passInput)
        hash_passCheck = h.sha1(bytes(passCheck, 'utf-8')).hexdigest()
        print(hash_passCheck)
        
        if(hash_passCheck == hash_passInput):
            return True
        else:
            return False
    
    def checkUserPass(self,username, passInput):
        infor = self.selectStudent(username)
        if(infor == None):
            infor = self.selectTeacher(username)
            if (infor == None):
                return 0
            else:
                if (self.checkSign(infor[6], passInput) == True):
                    return 1
                else:
                    return 0
        else:
            if (self.checkSign(infor[7], passInput) == True):
                return 2
            else:
                return 0
#endregion Database Server

class Student(qtw.QWidget):
    def __init__(self, StudentID):
        super().__init__()
        self.StudentID = StudentID
        self.server = Server()
        #Load giao diện lên
        uic.loadUi("student.ui", self)

        self.loadProfile()

        #button Log Out
        #self.buttonLogout.clicked.connect(self.LogOut)

        #button Xem kết quả
        self.buttonResult.clicked.connect(self.loadResult)

        #Set up lại cái table, tại nó khó sửa trên giao diện quá
        self.tableResult.setColumnWidth(0, 160)
        self.tableResult.setColumnWidth(1, 150)
        self.tableResult.setColumnWidth(8, 110)
        print(self.selectSemester.currentText()+self.selectYear.currentText())
        '''delegate = ReadOnlyDelegate(self)
        for i in range (tableResult.columnCount()):
            tableResult.setItemDelegateForColumn(i, delegate)'''


    def loadResult(self):
        result = self.server.studentResult(self.StudentID, self.selectSemester.currentText(), self.selectYear.currentText())
        self.loadTableResult(result)
        


    def loadTableResult(self, listModule):
        row = 0
        sumCredit = 0 
        sumPoint = 0
        self.tableResult.setRowCount(len(listModule))
        if (len(listModule) != 0):
            for i in range(len(listModule)):  
                sumCredit +=  listModule[i][2]
                sumPoint += listModule[i][7]
                self.tableResult.setItem(row, 0, qtw.QTableWidgetItem(listModule[i][0]))
                self.tableResult.setItem(row, 1, qtw.QTableWidgetItem(listModule[i][1]))
                self.tableResult.setItem(row, 2, qtw.QTableWidgetItem(str(listModule[i][2])))
                self.tableResult.setItem(row, 3, qtw.QTableWidgetItem(str(listModule[i][3])))
                self.tableResult.setItem(row, 4, qtw.QTableWidgetItem(str(listModule[i][4])))
                self.tableResult.setItem(row, 5, qtw.QTableWidgetItem(str(listModule[i][5])))
                self.tableResult.setItem(row, 6, qtw.QTableWidgetItem(str(listModule[i][6])))
                self.tableResult.setItem(row, 7, qtw.QTableWidgetItem(str(listModule[i][7])))
                self.tableResult.setItem(row, 8, qtw.QTableWidgetItem(listModule[i][8]))
                row = row + 1
            self.labelNumberCredit.setText(str(sumCredit))
            averageSemester = sumPoint/len(listModule)
            self.labelAveragePoint.setText(str(averageSemester))
            if (averageSemester < 5):
                self.labelClassify = "Yeu"
            elif (averageSemester >= 5 and averageSemester < 8):
                self.labelClassify = "Kha"
            elif (averageSemester >= 8 and averageSemester < 9):
                self.labelClassify = "Gioi"
            else:
                self.labelClassify = "Xuat sac"

    def loadProfile(self):
        #Load Profile
        profile = self.server.selectStudent(self.StudentID)
        self.labelIDStudent.setText(profile[0])
        self.labelName.setText(profile[1])
        self.labelSex.setText(profile[2])
        self.labelYear.setText(profile[3])
        self.labelFaculty.setText(profile[4])
        self.labelPhone.setText(profile[5])
        self.labelMail.setText(profile[6])

    
app = qtw.QApplication([])

a = Student("19521336")
a.show()
app.exec_()
