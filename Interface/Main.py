import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5 import uic
import PyQt5.QtCore as qtc
import sys

#Này là cái class cho cái form 
class LogIn(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Load giao diện
        uic.loadUi("login.ui", self)

        #Các thành phần cần quan tâm thì t đặt ra ở đây. 
        #lineUsername là cái mà nhập username đó 
        #linePassword là nhập gì thì bít òy đó =))
        #buttonLogin là cái button mà nhấn dô thì kiểm tra pass.
        buttonLogin =  self.findChild(qtw.QPushButton, 'buttonLogin')
        lineUsername = self.findChild(qtw.QLineEdit, 'lineUsername')
        linePassword = self.findChild(qtw.QLineEdit, 'linePassword')

        #Muốn tạo event cho button thì như này nè!
        buttonLogin.clicked.connect(self.checkPass)

        #Cái hàm event ở dưới đây nha
    def checkPass(self):
        qtw.QMessageBox.warning(self,"Imformation", "Log in successful!")     



    
#Cái form giao diện teacher ở đây
class Teacher(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Load giao diện
        uic.loadUi("teacher.ui", self)

        #Load nguyên cái profile lên.
        labelIDTeacher = self.findChild(qtw.QLabel, 'labelIDTeacher')
        labelName = self.findChild(qtw.QLabel, 'labelName')
        labelSex = self.findChild(qtw.QLabel, 'labelSex')
        labelFaculty = self.findChild(qtw.QLabel, 'labelFaculty')
        labelPhone = self.findChild(qtw.QLabel, 'labelPhone')
        labelMail = self.findChild(qtw.QLabel, 'labelMail')

        #Xong các profile rùi add vô class TeacherProfile cho gọn:
        teacher = TeacherProfile(labelIDTeacher.text(), labelName.text(), labelSex.text(), labelFaculty.text(), labelPhone.text(), labelMail.text())

        #Load típ mấy cái khác
        #selectSemester là cái comboBox chọn học kỳ đó
        #selectYear là cái comboBox chọn năm học
        #buttonListClass là cái nút xem danh sách lớp học. OK mann!
        buttonLogout = self.findChild(qtw.QPushButton, 'buttonLogout')
        selectSemester = self.findChild(qtw.QComboBox, 'selectSemester')
        selectYear = self.findChild(qtw.QComboBox, 'selectYear')
        buttonListClass = self.findChild(qtw.QPushButton, 'buttonListClass')

        #Chỗ search
        lineSearch = self.findChild(qtw.QLineEdit, 'lineSearch')
        buttonSearch = self.findChild(qtw.QPushButton, 'buttonSearch')

        #Load cái list class lên sau khi chọn được học kỳ và năm học
        listClass = self.findChild(qtw.QListWidget, 'listClass')

        #Thông tin lớp học
        #Lần lượt là điền vào mấy cái ID lớp học, tên môn học, số tín chỉ, sĩ số, tiết
        labelIDClass = self.findChild(qtw.QLabel, 'labelIDClass')
        labelNameSubject = self.findChild(qtw.QLabel, 'labelNameSubject')
        labelMoney = self.findChild(qtw.QLabel, 'labelMoney')
        labelNumber = self.findChild(qtw.QLabel, 'labelNumber')
        labelTime = self.findChild(qtw.QLabel, 'labelTime')

        #Button Sửa điểm
        buttonEdit = self.findChild(qtw.QPushButton, 'buttonEdit')

        #Set up lại cái table, tại nó khó sửa trên giao diện quá
        tableClass = self.findChild(qtw.QTableWidget, 'tableClass')
        tableClass.setColumnWidth(1, 150)
        tableClass.setColumnWidth(8, 110)
        self.loadData()


    def loadData(self):
        student = [ResultStudent("19522307", "Nguyễn Thị Thu", "Nữ", 8, 8, 8, 8, 8), ResultStudent("19522306", "Nguyễn Văn Bé", "Nam", 9, 9, 9, 9, 9),]
        row = 0
        self.tableClass.setRowCount(len(student))
        for person in student:
            self.tableClass.setItem(row, 0, qtw.QTableWidgetItem(person.ID))
            self.tableClass.setItem(row, 1, qtw.QTableWidgetItem(person.name))
            self.tableClass.setItem(row, 2, qtw.QTableWidgetItem(person.sex))
            self.tableClass.setItem(row, 3, qtw.QTableWidgetItem(str(person.processPoint)))
            self.tableClass.setItem(row, 4, qtw.QTableWidgetItem(str(person.midPoint)))
            self.tableClass.setItem(row, 5, qtw.QTableWidgetItem(str(person.labPoint)))
            self.tableClass.setItem(row, 6, qtw.QTableWidgetItem(str(person.endPoint)))
            self.tableClass.setItem(row, 7, qtw.QTableWidgetItem(str(person.averagePoint)))
            row = row + 1



#Form student ở đây
class Student(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Load giao diện lên
        uic.loadUi("student.ui", self)

        #Load nguyên cái profile lên.
        labelIDStudent = self.findChild(qtw.QLabel, 'labelIDStudent')
        labelName = self.findChild(qtw.QLabel, 'labelName')
        labelSex = self.findChild(qtw.QLabel, 'labelSex')
        labelYear = self.findChild(qtw.QLabel, 'labelYear')
        labelFaculty = self.findChild(qtw.QLabel, 'labelFaculty')
        labelPhone = self.findChild(qtw.QLabel, 'labelPhone')
        labelMail = self.findChild(qtw.QLabel, 'labelMail')

        #Bỏ dô nguyên cái class cho dễ thở
        #student = StudentProfile(labelIDStudent.text(), labelName.text(), labelSex.text(), labelYear.text(), labelFaculty.text(), labelPhone.text(), labelMail.text())

        #button Log Out, Combo Box chọn học kỳ, năm học
        buttonLogout = self.findChild(qtw.QPushButton, 'buttonLogout')
        selectSemester = self.findChild(qtw.QComboBox, 'selectSemester')
        selectYear = self.findChild(qtw.QComboBox, 'selectYear')
        #button Xem kết quả
        buttonResult = self.findChild(qtw.QPushButton, 'buttonResult')

        #Chỗ search
        lineSearch = self.findChild(qtw.QLineEdit, 'lineSearch')
        buttonSearch = self.findChild(qtw.QPushButton, 'buttonSearch')

        #In thông tin học kỳ
        labelNumberMoney = self.findChild(qtw.QLabel, 'labelIDClass')
        labelAveragePoint = self.findChild(qtw.QLabel, 'labelAveragePoint') 
        labelClassify= self.findChild(qtw.QLabel, 'labelClassify') #Này là chỗ xếp loại Xuất sắc, Giỏi, Khá, Trung bình, Yếu mà không tìm ra được từ tiếng anh soang chảnh nào đặt biến

        #Set up lại cái table, tại nó khó sửa trên giao diện quá
        tableResult = self.findChild(qtw.QTableWidget, 'tableResult')
        tableResult.setColumnWidth(0, 160)
        tableResult.setColumnWidth(1, 150)
        tableResult.setColumnWidth(8, 110)
        self.loadData()

    def loadData(self):
        subject = [ResultSubject("NT219.L21.ANTT", "Mật mã học", 4, 8, 8, 8, 8, 8), ResultSubject("IT007.L21", "Hệ điều hành", 4, 9, 9, 9, 9, 9),]
        row = 0
        self.tableResult.setRowCount(len(subject))
        for sub in subject:
            self.tableResult.setItem(row, 0, qtw.QTableWidgetItem(sub.ID))
            self.tableResult.setItem(row, 1, qtw.QTableWidgetItem(sub.name))
            self.tableResult.setItem(row, 2, qtw.QTableWidgetItem(str(sub.money)))
            self.tableResult.setItem(row, 3, qtw.QTableWidgetItem(str(sub.processPoint)))
            self.tableResult.setItem(row, 4, qtw.QTableWidgetItem(str(sub.midPoint)))
            self.tableResult.setItem(row, 5, qtw.QTableWidgetItem(str(sub.labPoint)))
            self.tableResult.setItem(row, 6, qtw.QTableWidgetItem(str(sub.endPoint)))
            self.tableResult.setItem(row, 7, qtw.QTableWidgetItem(str(sub.averagePoint)))
            row = row + 1


#Class này dùng để làm profile của teacher
class TeacherProfile():
    def __init__(self, ID, name, sex, faculty, phone, mail):
        self.ID = ID
        self.name = name
        self.sex = sex
        self.faculty = faculty
        self.phone = phone
        self.mail = mail


#Profile của student
class StudentProfile():
    def __init__(self, ID, name, sex, year, faculty, phone, mail):
        self.ID = ID
        self.name = name
        self.sex = sex
        self.year = year
        self.faculty = faculty
        self.phone = phone
        self.mail = mail


#Dành cho mỗi dòng trong cái table của Form Teacher
class ResultStudent():
    def __init__(self, ID, name, sex, processPoint, midPoint, labPoint, endPoint, averagePoint):
        self.ID = ID
        self.name = name
        self.sex = sex
        self.processPoint = processPoint
        self.midPoint = midPoint
        self.labPoint = labPoint
        self.endPoint = endPoint
        self.averagePoint = averagePoint


#Dành cho mỗi dòng trong cái table của Form Student
class ResultSubject():
    def __init__(self, ID, name, money, processPoint, midPoint, labPoint, endPoint, averagePoint):
        self.ID = ID
        self.name = name
        self.money = money
        self.processPoint = processPoint
        self.midPoint = midPoint
        self.labPoint = labPoint
        self.endPoint = endPoint
        self.averagePoint = averagePoint


app = qtw.QApplication([])
#Chỗ phải thay đổi mới xem form muốn xem đc. Tại vì phải set điều kiển nhảy form cho button Log In ở form LogIn, sau đó dùng stack widgets để nhảy widget.
#Mấy cái table chưa có set read
#Mệt quá nên đi ngủ hoi
login = Teacher()
login.show()
app.exec_()