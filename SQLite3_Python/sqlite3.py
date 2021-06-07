import sqlite3
from sqlite3 import Error


def connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
       # print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create(conn, sql):
    # -- tasks table
#     CREATE TABLE IF NOT EXISTS teacher (
#         id integer PRIMARY KEY,
#         name text NOT NULL,
#         priority integer,
#         project_id integer NOT NULL,
#         status_id integer NOT NULL,
#         begin_date text NOT NULL,
#         end_date text NOT NULL,
#         FOREIGN KEY (project_id) REFERENCES projects (id)
#     );

    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def insert(conn, student):

    sql = ''' INSERT INTO student(Name,Math,English)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, student) #project = ('Dat',10, 9.9) 
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

def select_by_id(conn, id):

    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE id=?", (id,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

if __name__ == '__main__':

    conn = connect(r"db\pythonsqlite.db")


    sql= """CREATE TABLE IF NOT EXISTS student (
    id integer PRIMARY KEY,
    Name text NOT NULL,
    Math float,
    English float
    );
    """
    create(conn,sql)

    # student = ('Dat',10, 9.9) ;
    # try :
    #     insert(conn,student)
    # except Error as e:
    #     print("Can't insert ! ERROR ",e)


    # student = (1,'Dat',8,9) ;

    # try :
    #     update(conn,student)
    # except Error as e:
    #     print("Can't update ! ERROR ",e)

    # delete_by_id(conn,1)

    # try:
    #     select_by_id(conn,2)
    # except Error as e :
    #     print("Cant select ! ERROR ", e)
    
