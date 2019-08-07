from threading import Thread
from queue import Queue
import sqlite3


class SingleThreadOnly(object):
    def __init__(self, db):
        self.cnx = sqlite3.Connection(db, check_same_thread=False)
        self.cursor = self.cnx.cursor()

    def execute(self, req, arg=None):
        self.cursor.execute(req, arg or tuple())

    def select(self, req, arg=None):
        self.execute(req, arg)
        for raw in self.cursor:
            yield raw

    def close(self):
        self.cnx.close()


class MultiThreadOK(Thread):
    def __init__(self, db):
        super(MultiThreadOK, self).__init__()
        self.db = db
        self.reqs = Queue()
        self.start()

    def run(self):
        cnx = sqlite3.Connection(self.db, check_same_thread=False)
        cursor = cnx.cursor()
        while True:
            req, arg, res = self.reqs.get()
            if req == '--close--': break
            cursor.execute(req, arg)
            if res:
                for rec in cursor:
                    res.put(rec)
                res.put('--no more--')
        cnx.close()

    def execute(self, req, arg=None, res=None):
        self.reqs.put((req, arg or tuple(), res))

    def select(self, req, arg=None):
        res = Queue()
        self.execute(req, arg, res)
        while True:
            rec = res.get()
            if rec == '--no more--': break
            yield rec

    def close(self):
        self.execute('--close--')


class DBHelper:

    def __init__(self, dbname="main.sqlite"):
        self.dbname = dbname



    def setup(self):
        self.c = MultiThreadOK(db=self.dbname)
        tbl_users = """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT 0,username VARCHAR DEFAULT NULL ,role INTEGER DEFAULT 0)"""
        tbl_apolo = """CREATE TABLE IF NOT EXISTS apolo(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT 0,question VARCHAR DEFAULT NULL ,answer VARCHAR DEFAULT NULL ,group_id INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,question_type VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_group = """CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY,group_id INTEGER DEFAULT 0,group_title VARCHAR DEFAULT NULL ,group_language VARCHAR DEFAULT NULL,user_id INTEGER DEFAULT 0)"""
        tbl_answers = """CREATE TABLE IF NOT EXISTS answers(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT 0,correct INTEGER DEFAULT 0,incorrect INTEGER DEFAULT 0,answertype VARCHAR DEFAULT NULL)"""
        tbl_seshat = """CREATE TABLE IF NOT EXISTS seshat(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT 0,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,group_id INTEGER DEFAULT 0,status INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,questiontype VARCHAR DEFAULT NULL)"""
        tbl_zamol = """CREATE TABLE IF NOT EXISTS zamol(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT NULL ,question VARCHAR DEFAULT NULL,group_id INTEGER DEFAULT 0,status INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,lang VARCHAR DEFAULT NULL,questiontype VARCHAR DEFAULT NULL)"""
        tbl_gaia = """CREATE TABLE IF NOT EXISTS gaia(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT NULL ,question VARCHAR DEFAULT NULL,group_id INTEGER DEFAULT 0,status INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,lang VARCHAR DEFAULT NULL,questiontype VARCHAR DEFAULT NULL)"""
        tbl_counter = """CREATE TABLE IF NOT EXISTS rank(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT NULL ,group_id INTEGER DEFAULT 0,messages INTEGER DEFAULT 0,rank INTEGER DEFAULT 0,answertype VARCHAR DEFAULT NULL)"""
        self.c.execute(tbl_answers)
        self.c.execute(tbl_apolo)
        self.c.execute(tbl_users)
        self.c.execute(tbl_group)
        self.c.execute(tbl_seshat)
        self.c.execute(tbl_zamol)
        self.c.execute(tbl_gaia)
        self.c.execute(tbl_counter)
        self.c.close()



    def check_user(self,user_id):
        self.c.execute("SELECT user_id from users WHERE user_id=?",(user_id,))
        user =self.c.fetchone()
        if user is not None:
            return int(user[0])
        else:
            return False