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

    def updateResult(self, ProcessPoint, MidPoint, LabPoint, EndPoint, AveragePoint, Note, StudentID, ModuleID):
        self.cur.execute("""UPDATE RESULT SET ProcessPoint = ?, MidPoint = ?, LabPoint = ?, EndPoint = ?, AveragePoint = ?, Note = ? WHERE StudentID = ? and ModuleID = ?""", (ProcessPoint,MidPoint, LabPoint, EndPoint, AveragePoint, Note,StudentID,ModuleID,))
        self.conn.commit()
    def view(self):
        self.cur.execute("""SELECT*FROM RESULT WHERE StudentID = '19522307'""")
        [print(row) for row in self.cur.fetchall()]

server = Server()
update = (9, 9, 9, 9,'Dat','19522307','NT216.L21.ANTT')
server.updateResult(9,9,9,9,9, 'Dat','19522307', 'IT007.L21', )
server.view()