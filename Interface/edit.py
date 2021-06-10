import sqlite3
from sqlite3 import Error
import hashlib as h

#Database Server
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

    def selectTeacher(self, username):
        self.cur.execute("SELECT * FROM TEACHER WHERE TeacherID=?", (username,))
        row = self.cur.fetchone()
        return row

    def checkSign(self, passCheck, passInput):
        hash_passCheck = h.sha1(bytes(passCheck, 'utf-8')).hexdigest()
        hash_passInput = h.sha1(bytes(passInput, 'utf-8')).hexdigest()
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

class Stress():
    def __init__(self):
        super().__init__()
        self.username = "anv"
        self.password = "1566556675"
        a = self.username
        b = self.password
        server = Server()
        check = server.checkUserPass(a,b)
        print(check)

stress = Stress()
