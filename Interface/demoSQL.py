import sqlite3
from sqlite3 import Error
import hashlib as h


def connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
       # print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create(conn, sql):

    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def insert_student(conn, student):

    sql = ''' INSERT INTO STUDENT(StudentID,Fullname,Sex,Year,Faculty,Phone,Email,PublicKey)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, student) #student = ('19521336','Nguyen Le Quoc Dat','Nam','K14','MMT&TT','0976828232','19521336@gm.uit.edu.vn','ascascascasc' ) 
    conn.commit()
    return cur.lastrowid

def insert_teacher(conn, teacher):

    sql = ''' INSERT INTO TEACHER(TeacherID,Fullname,Sex,Faculty,Phone,Email,PrivateKey)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, teacher) #teacher = ('1952',' Quoc Dat','Nam','MMT&TT','0976828232','19521336@gm.uit.edu.vn','gessing' ) 
    conn.commit()
    return cur.lastrowid

def insert_result(conn, result):

    sql = ''' INSERT INTO RESULT(StudentID,ModuleID,ProcessPoint,MidPoint,LabPoint,EndPoint,AveragePoint,Note)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, result ) #result = ('19521336','NT216.ATTT.L21','10','10','10','10','gessing' ) 
    conn.commit()
    return cur.lastrowid

def insert_module(conn, module):
    sql = """INSERT INTO MODULE(ModuleID,NameSubject,TeacherID,Semester,SchoolYear) 
                        VALUES(?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, module) #module = ('NT216.ATTT.L21','Mat ma hoc','1952','1','2020-2021' ) 
    conn.commit()
    return cur.lastrowid

def update(conn, student):

    sql = ''' UPDATE student
              SET Name = ? ,
                  Math = ? ,
                  English = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()

def delete_by_id(conn, id):
    sql = 'DELETE FROM student WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def selectStudent(conn, username):

    cur = conn.cursor()
    cur.execute("SELECT * FROM STUDENT WHERE StudentID=?", (username,))

    row = cur.fetchone()
    return row

def selectTeacher(conn, username):

    cur = conn.cursor()
    cur.execute("SELECT * FROM TEACHER WHERE TeacherID=?", (username,))

    row = cur.fetchone()
    return row

def check(passCheck, passInput):
    hash_passCheck = h.sha1(bytes(passCheck, 'utf-8')).hexdigest()
    hash_passInput = h.sha1(bytes(passInput, 'utf-8')).hexdigest()
    if(hash_passCheck == hash_passInput):
        print("Chuc mung!")
    else:
        print("Password sai roy!")


def checkPass(conn, username, passInput):
    infor = selectStudent(conn, username)

    if(infor == None):
        infor = selectTeacher(conn, username)
        
        if (infor == None):
            print("Username sai roy!")
        else:
            check(infor[7], passInput)
            print("Ban la giao vien!")
    else:
        check(infor[7], passInput)
        print("Ban la hoc sinh!")


if __name__ == '__main__':

    conn = connect(r"ECCapp.db")
    username = "19521336"
    password = "simpboiz"
    checkPass(conn,username,password)
    '''cur = conn.cursor()
    cur.execute("""SELECT * FROM STUDENT""")
    print(cur.fetchone()[7])'''



    '''sql= """CREATE TABLE IF NOT EXISTS student (
    id integer PRIMARY KEY,
    Name text NOT NULL,
    Math float,
    English float
    );
    """
    create(conn,sql)
    
    student = ('19521336','Nguyen Le Quoc Dat','Nam','K14','MMT&TT','0976828232','19521336@gm.uit.edu.vn','ascascascasc' ) 
    teacher = ('19521336','Nguyen Le Quoc Dat','Nam','MMT&TT','0976828232','19521336@gm.uit.edu.vn','gessingcxxc' ) 
    module = ('NT216.ATTT.L21','Mat ma hoc','1952','Hoc ky 1','2020-2021' )
    result = ('19521336','NT216.ATTT.L21','10','10','10','10','gessingxs' ) 


    try:

        insert_student(conn,student)
    except Error as e:
        print(e)

    try:
        insert_teacher(conn,teacher)
    except Error as e:
        print(e)

    try:
        insert_module(conn,module)
    except Error as e:
        print(e)
    try:
        insert_result(conn,result)
    except Error as e:
        print(e)'''
    
    