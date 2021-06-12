import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

#Đây là khung đăng nhập
class SignUp(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        #Đổi background sang màu trắng, đổi tên form là WELCOME, thêm logo, đặt fixed size cho window sign in
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("WELCOME")
        self.setWindowIcon(qtg.QIcon('Logo.ico'))
        self.setFixedWidth(1000)
        self.setFixedHeight(650)
        self.move(400,100)

        #Cái thanh xanh xanh đầu form. Ok
        self.label2 = qtw.QLabel(self)
        self.label2.resize(1000, 50)
        self.label2.move(0, 0)
        self.label2.setStyleSheet("background-color: #296091;")

        #Logo UIT 
        self.label = qtw.QLabel(self)
        self.pixmap = qtg.QPixmap('uit.png')
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.label.move(420, 110)
        
        '''Mấy đoạn dưới là khung nhập username và password'''
        #Username nhập vào trong khung userLine
        #Password nhập vào trong khung passLine

        #Cái label để chèn cái hình username vào
        self.labelUser = qtw.QLabel(self)
        self.pixmap = qtg.QPixmap('user.png')
        self.labelUser.setPixmap(self.pixmap)
        self.labelUser.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.labelUser.move(300, 305)

        #userLine để nhập username
        self.userLine = qtw.QLineEdit(self)
        self.userLine.setGeometry(345, 300, 350, 50)
        self.userLine.setText("username")
        self.userLine.setFont(qtg.QFont('Sans Serif', 16))
        self.userLine.setStyleSheet("background-color: white; border-style: solid; border-width: 2px; border-radius: 15px; border-color: rgb(18,153,175); padding: 4px; color: #474747;")

        #Label hiển thị cái hình ổ khoá
        self.labelPass = qtw.QLabel(self)
        self.pixmap = qtg.QPixmap('pass.png')
        self.labelPass.setPixmap(self.pixmap)
        self.labelPass.resize(self.pixmap.width(),
                          self.pixmap.height())
        self.labelPass.move(300, 385)

        #passLine để nhập password
        self.passLine = qtw.QLineEdit(self)
        self.passLine.setGeometry(345, 380, 350, 50)
        self.passLine.setText("password")
        self.passLine.setEchoMode(qtw.QLineEdit.Password)
        self.passLine.setFont(qtg.QFont('Sans Serif', 16))
        self.passLine.setStyleSheet("background-color: white; border-style: solid; border-width: 2px; border-radius: 15px; border-color: rgb(18,153,175); padding: 4px; color: #474747;")

        #BUTTON SIGNIN
        self.button = qtw.QPushButton("Sign in", self)
        self.button.setGeometry(550, 460, 150, 60)
        self.button.setStyleSheet("background-color: rgb(18,153,175); border-style: outset; border-width: 2px; border-radius: 15px; border-color: white; padding: 4px; color:white")
        self.button.setFont(qtg.QFont('Sans Serif', 18))
        
        #Made by 54010n
        self.labelTeam = qtw.QLabel(self)
        self.labelTeam.setText("Made by 54010n")
        self.labelTeam.setFont(qtg.QFont('Sans Serif', 16))
        self.labelTeam.move(800, 600)

        #Show window as default
        self.show()



app = qtw.QApplication([])
mw = SignUp()

#Run the app
app.exec_()
