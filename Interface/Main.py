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
        try:
            self.conn = sqlite3.connect("ECCapp.db")
            self.cur = self.conn.cursor()
        # print(sqlite3.version)
        except Error as e:
            print(e)

    #Dùng cho StudentForm
    #selectStudent truy vấn Profile
    #studentResult truy vấn thông tin kết quả học tập theo kỳ và năm học
    def selectStudent(self, username):
        self.cur.execute("SELECT * FROM STUDENT WHERE StudentID=?", (username,))

        self.row = self.cur.fetchone()
        return self.row

    def studentResult(self, username, semester, schoolyear):
        self.cur.execute("SELECT md.ModuleID, md.NameSubject, md.NumCredit, rs.ProcessPoint, rs.MidPoint, rs.LabPoint, rs.EndPoint, rs.AveragePoint, rs.Note FROM MODULE md, RESULT rs WHERE md.ModuleID = rs.ModuleID and rs.StudentID = ? and md.Semester = ? and md.SchoolYear = ?", (username, semester, schoolyear,))
        self.row = self.cur.fetchall()
        return self.row

    #Dùng cho TeacherForm
    #selectTeacher truy vấn Profile
    #selectSubjectList truy vấn danh sách lớp giáo viên dạy dựa theo kỳ và năm học
    #selectSubject truy vấn thông tin học phần theo ModuleID 
    #selectListStudent truy vấn danh sách học sinh và điểm 
    def selectTeacher(self, username):
        self.cur.execute("SELECT * FROM TEACHER WHERE TeacherID=?", (username,))
        self.row = self.cur.fetchone()
        return self.row

    def selectSubjectList(self, username, semester, schoolyear):
        self.cur.execute("SELECT ModuleID FROM MODULE WHERE TeacherID = ? and Semester = ? and SchoolYear = ?", (username, semester, schoolyear,))

        self.row = self.cur.fetchall()
        return self.row

    def selectSubject(self, ModuleID):
        self.cur.execute("SELECT ModuleID, NameSubject, NumStudent FROM MODULE WHERE ModuleID = ?", (ModuleID,))

        self.row = self.cur.fetchone()
        return self.row

    def selectListStudent(self, nameModule):
        self.cur.execute("SELECT st.StudentID, st.Fullname, st.Sex, rs.ProcessPoint, rs.MidPoint, rs.LabPoint,EndPoint,rs.AveragePoint,rs.Note FROM STUDENT st, RESULT rs, MODULE md WHERE st.StudentID = rs.StudentID and rs.ModuleID = md.ModuleID and md.ModuleID = ?", (nameModule,))

        self.row = self.cur.fetchall()
        return self.row

    #Hai method này dùng để checkpass
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


class ReadOnlyDelegate(qtw.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


#region LogIn form
class LogIn(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Load giao diện
        uic.loadUi("login.ui", self)
        
        #Button Log In
        self.buttonLogin.clicked.connect(self.checkPass)

    #Check mật khẩu
    def checkPass(self):
        server = Server()
        username = self.lineUsername.text()
        passInput = self.linePassword.text()

        check = server.checkUserPass(username, passInput)
        if check == 0:
            msg = qtw.QMessageBox.about(self,"Notification", "Username or password is incorrect!")
        elif check == 1:
            teacher = Teacher(username)
            stack.addWidget(teacher)
            stack.setCurrentIndex(stack.currentIndex() + 1)
        else:
            student = Student(username)
            stack.addWidget(student)
            stack.setCurrentIndex(stack.currentIndex() + 1)
#endregion LogIn form


#region Teacher Form
class Teacher(qtw.QWidget):
    def __init__(self, TeacherID):
        super().__init__()
        self.TeacherID = TeacherID
        self.server = Server()
        uic.loadUi("teacher.ui", self)

        #button Log Out
        self.buttonLogout.clicked.connect(self.LogOut)

        #Button Sửa điểm
        buttonEdit = self.findChild(qtw.QPushButton, 'buttonEdit')

        #Load Profile
        self.loadProfile()

        #Load bảng điểm lớp học
        self.loadSubjectList()

        #ListClass change
        self.selectSemester.currentTextChanged.connect(self.loadSubjectList)
        self.selectYear.currentIndexChanged.connect(self.loadSubjectList)
        
        #Set up lại kích thước table trong giao diện
        self.tableClass.setColumnWidth(1, 150)
        self.tableClass.setColumnWidth(8, 110)
        self.listClass.clicked.connect(self.loadListStudent)
     
    #Dùng load bảng kết quả lớp học và thông tin học phần
    def loadListStudent(self):
        self.tableClass.setRowCount(0)
        if (self.listClass != None):
            nameModule = self.listClass.currentItem().text()
            listStudent = self.server.selectListStudent(nameModule)
            self.loadTableClass(listStudent)
            inforModule = self.server.selectSubject(nameModule)
            self.loadInforModule(inforModule)
    
    #Dùng load thông tin học phần
    def loadInforModule(self, inforModule):
        self.labelIDClass.setText(inforModule[0])
        self.labelNameSubject.setText(inforModule[1])
        self.labelNumber.setText(str(inforModule[2]))

    #Dùng load bảng
    def loadTableClass(self, listStudent):
        row = 0 
        self.tableClass.setRowCount(len(listStudent))
        if (len(listStudent) != 0):
            for i in range(len(listStudent)):  
                self.tableClass.setItem(row, 0, qtw.QTableWidgetItem(listStudent[i][0]))
                self.tableClass.setItem(row, 1, qtw.QTableWidgetItem(listStudent[i][1]))
                self.tableClass.setItem(row, 2, qtw.QTableWidgetItem(listStudent[i][2]))
                self.tableClass.setItem(row, 3, qtw.QTableWidgetItem(str(listStudent[i][3])))
                self.tableClass.setItem(row, 4, qtw.QTableWidgetItem(str(listStudent[i][4])))
                self.tableClass.setItem(row, 5, qtw.QTableWidgetItem(str(listStudent[i][5])))
                self.tableClass.setItem(row, 6, qtw.QTableWidgetItem(str(listStudent[i][6])))
                self.tableClass.setItem(row, 7, qtw.QTableWidgetItem(str(listStudent[i][7])))
                self.tableClass.setItem(row, 8, qtw.QTableWidgetItem(listStudent[i][8]))
                row = row + 1

    #Dùng log out
    def LogOut(self):
        ret = qtw.QMessageBox.warning(self,"Test", "Are you sure?", qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if ret == qtw.QMessageBox.Yes:
            login = LogIn()
            stack.addWidget(login)
            stack.setCurrentIndex(stack.currentIndex() + 1)

    #Dùng load profile
    def loadProfile(self):
        #Load Profile
        profile = self.server.selectTeacher(self.TeacherID)
        self.labelIDTeacher.setText(profile[0])
        self.labelName.setText(profile[1])
        self.labelSex.setText(profile[2])
        self.labelFaculty.setText(profile[3])
        self.labelPhone.setText(profile[4])
        self.labelMail.setText(profile[5])

    #Dùng loas danh sách lớp học
    def loadSubjectList(self):
        self.listClass.clear()
        subjectList = self.server.selectSubjectList(self.TeacherID, self.selectSemester.currentText(), self.selectYear.currentText())

        if(subjectList != []):
            for i in range(len(subjectList)):
                self.listClass.insertItem(i, subjectList[i][0])
#endregion Teacher Form


#region Student Form
class Student(qtw.QWidget):
    def __init__(self, StudentID):
        super().__init__()
        self.StudentID = StudentID
        self.server = Server()
        #Load giao diện lên
        uic.loadUi("student.ui", self)

        #Load Profile
        self.loadProfile()

        #button Log Out
        self.buttonLogout.clicked.connect(self.LogOut)

        #button Xem kết quả
        self.buttonResult.clicked.connect(self.loadResult)

        #Set up lại kích thước table trong giao diện
        self.tableResult.setColumnWidth(0, 160)
        self.tableResult.setColumnWidth(1, 150)
        self.tableResult.setColumnWidth(8, 110)

    #Load thông tin học kỳ và nguyên cái bảng
    def loadResult(self):
        result = self.server.studentResult(self.StudentID, self.selectSemester.currentText(), self.selectYear.currentText())
        self.loadTableResult(result)

    #Load bảng và thông tin học kỳ
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
                self.labelClassify.setText("Yeu")
            elif averageSemester >= 5 and averageSemester < 8:
                self.labelClassify.setText("Trung binh")
            elif averageSemester >= 8 and averageSemester < 9:
                self.labelClassify.setText("Gioi")
            else:
                self.labelClassify.setText("Xuat sac")

    #Load Profile
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

    #Log out
    def LogOut(self):
        ret = qtw.QMessageBox.warning(self,"Test", "Are you sure?", qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if ret == qtw.QMessageBox.Yes:
            login = LogIn()
            stack.addWidget(login)
            stack.setCurrentIndex(stack.currentIndex() + 1)
#endregion Student Form

app = qtw.QApplication([])

stack = qtw.QStackedWidget()
login = LogIn()
stack.addWidget(login)
stack.setStyleSheet("background-color: white;")
stack.setWindowIcon(qtg.QIcon('uit.ico'))
stack.setWindowTitle("EEC Application")
stack.move(50, 50)
stack.show()
app.exec_()