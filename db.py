#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

class DBHelper:

    def __init__(self, dbname="main.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.c = self.conn.cursor()

    def setup(self):
        tbl_users = """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT 0,username VARCHAR DEFAULT NULL ,role INTEGER DEFAULT 0)"""
        tbl_apolo = """CREATE TABLE IF NOT EXISTS apolo(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT 0,question VARCHAR DEFAULT NULL ,answer VARCHAR DEFAULT NULL ,group_id INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,question_type VARCHAR DEFAULT NULL,status INTEGER DEFAULT 0)"""
        tbl_group = """CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY,group_id INTEGER DEFAULT 0,group_title VARCHAR DEFAULT NULL ,group_language VARCHAR DEFAULT NULL,user_id INTEGER DEFAULT 0)"""
        tbl_answers ="""CREATE TABLE IF NOT EXISTS answers(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT 0,correct INTEGER DEFAULT 0,incorrect INTEGER DEFAULT 0,answertype VARCHAR DEFAULT NULL)"""
        tbl_seshat ="""CREATE TABLE IF NOT EXISTS seshat(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT 0,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,group_id INTEGER DEFAULT 0,status INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,questiontype VARCHAR DEFAULT NULL)"""
        tbl_zamol = """CREATE TABLE IF NOT EXISTS zamol(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT NULL ,question VARCHAR DEFAULT NULL,group_id INTEGER DEFAULT 0,status INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,lang VARCHAR DEFAULT NULL,questiontype VARCHAR DEFAULT NULL)"""
        tbl_gaia = """CREATE TABLE IF NOT EXISTS gaia(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT NULL ,question VARCHAR DEFAULT NULL,group_id INTEGER DEFAULT 0,status INTEGER DEFAULT 0,message_id INTEGER DEFAULT 0,lang VARCHAR DEFAULT NULL,questiontype VARCHAR DEFAULT NULL)"""
        tbl_counter = """CREATE TABLE IF NOT EXISTS rank(id INTEGER PRIMARY KEY ,user_id INTEGER DEFAULT NULL,file_id VARCHAR DEFAULT NULL ,group_id INTEGER DEFAULT 0,messages INTEGER DEFAULT 0,rank INTEGER DEFAULT 0,answertype VARCHAR DEFAULT NULL)"""
        self.c.execute(tbl_users)
        self.c.execute(tbl_gaia)
        self.c.execute(tbl_apolo)
        self.c.execute(tbl_group)
        self.c.execute(tbl_seshat)
        self.c.execute(tbl_zamol)
        self.c.execute(tbl_answers)
        self.c.execute(tbl_counter)
        self.conn.commit()
        
################# USERS######################
    def set_user(self,user_id,username,role):
        if self.check_user(user_id=user_id)==False:
            self.c.execute("INSERT INTO users (user_id,username,role) VALUES (?,?,?)",(user_id,username,role))
            self.conn.commit()
            

    def check_user(self,user_id):
        self.c.execute("SELECT user_id from users WHERE user_id=?",(user_id,))
        user =self.c.fetchone()
        if user is not None:
            return int(user[0])
        else:
            return False

    def set_role(self,role,user_id):
        if self.check_user(user_id=user_id) != False:
            self.c.execute("UPDATE users SET role=? WHERE  user_id=? ", (role,user_id))
            self.conn.commit()
            

    def check_admin(self,user_id):
        self.c.execute("SELECT role from users WHERE user_id=?", (user_id,))
        role = self.c.fetchone()
        if role is not None:
            return role[0]
        else:
            return False

    def get_all_admins(self):
        data = []
        for user in self.c.execute("SELECT user_id from users WHERE  role=1"):
            data.append(user[0])
        return data

    def delete_admin(self, admin_id):
        self.c.execute("DELETE FROM users WHERE user_id=?", (admin_id,))
        self.conn.commit()
        


####################END USERS################################

#################### apolo ###################################

    def set_apolo_question(self, question,answer,user_id):
        self.c.execute("INSERT INTO apolo(question,answer,user_id) VALUES (?,?,?)",
                       (question,answer,user_id))
        self.conn.commit()
        

    def get_last_apolo_id(self, user_id):
        self.c.execute("SELECT MAX(id) FROM apolo WHERE user_id=?", (user_id,))
        insta_user = self.c.fetchone()
        return int(insta_user[0])

    def get_apolo_answer(self,qstn,user_id):
        self.c.execute("SELECT answer FROM apolo WHERE answer=? and user_id=?", (qstn,user_id))
        user = self.c.fetchone()
        if user is not None:
            return True
        else:
            return False

    def get_apolo_answer_by_msg_id(self,msg_id):
        self.c.execute("SELECT answer FROM apolo WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def get_apolo_qstn_status(self,msg_id):
        self.c.execute("SELECT status FROM apolo WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def change_apolo_qstn_status(self,status,msg_id):
        self.c.execute("UPDATE apolo SET status=? WHERE  message_id=? ", (status,msg_id))
        self.conn.commit()
        






    def get_apolo_question(self,qid):
        self.c.execute("SELECT question FROM apolo WHERE id=?", (qid,))
        qstn = self.c.fetchone()
        if qstn is not None:
            return qstn[0]
        else:
            return False
    def change__apolo_qstn_group_id(self,group_id,qid,user_id):
        self.c.execute("UPDATE apolo SET group_id=? WHERE id=? AND user_id=? ", (group_id,qid,user_id))
        self.conn.commit()
        


    def update_apolo_msgid_qstn_type(self,message_id,question_type,tbl_id,user_id):
        self.c.execute("UPDATE apolo SET message_id=?,question_type=? WHERE id=? and user_id=?", (message_id,question_type,tbl_id,user_id))
        self.conn.commit()
        

    def get_apolo_question_type(self,msg_id):
        self.c.execute("SELECT question_type FROM apolo WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False
########################END APOLO##################################

#####################SESHAT########################################

    def add_seshat_question(self, user_id, file_id,questiontype):
        self.c.execute("INSERT INTO seshat(user_id,file_id,questiontype) VALUES (?,?,?)", ( user_id,file_id,questiontype))
        self.conn.commit()
        


    def get_last_seshat_id(self, user_id):
        self.c.execute("SELECT MAX(id) FROM seshat WHERE user_id=?", (user_id,))
        insta_user = self.c.fetchone()
        return int(insta_user[0])


    def change_seshat_qstn(self,question,tbl_id,user_id):
        self.c.execute("UPDATE seshat SET question=? WHERE id=? and user_id=?", (question,tbl_id,user_id))
        self.conn.commit()
        

    def change_seshat_answer(self,answer,tbl_id,user_id):
        self.c.execute("UPDATE seshat SET answer=? WHERE id=? and user_id=?", (answer,tbl_id,user_id))
        self.conn.commit()
        

    def change_seshat_group_id(self,group_id,tbl_id,user_id):
        self.c.execute("UPDATE seshat SET group_id=? WHERE id=? and user_id=?", (group_id,tbl_id,user_id))
        self.conn.commit()
        


    def get_seshat_question(self, tbl_id, user_id):
        self.c.execute("SELECT question,file_id FROM seshat WHERE id=? and user_id=?", (tbl_id, user_id))
        ques = self.c.fetchone()
        if ques is not None:
            return ques

    def change_seshat_message_id(self,message_id,tbl_id,user_id):
        self.c.execute("UPDATE seshat SET message_id=? WHERE id=? and user_id=?", (message_id,tbl_id,user_id))
        self.conn.commit()
        

    def get_seshat_question_type(self,msg_id):
        self.c.execute("SELECT questiontype FROM seshat WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def get_seshat_answer_by_msg_id(self,msg_id):
        self.c.execute("SELECT answer FROM seshat WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def get_seshat_qstn_status(self,msg_id):
        self.c.execute("SELECT status FROM seshat WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False


    def change_seshat_qstn_status(self,status,msg_id):
        self.c.execute("UPDATE seshat SET status=? WHERE  message_id=? ", (status,msg_id))
        self.conn.commit()
        
#####################END SESHAT ###################################
###########START ZAMOL#############################################
    def add_zamol_question(self, user_id,group_id,language,questiontype):
        self.c.execute("INSERT INTO zamol(user_id,group_id,lang,questiontype) VALUES (?,?,?,?)", ( user_id,group_id,language,questiontype))
        self.conn.commit()
        


    def get_last_zamol_id(self, user_id):
        self.c.execute("SELECT MAX(id) FROM zamol WHERE user_id=?", (user_id,))
        insta_user = self.c.fetchone()
        return int(insta_user[0])

    def get_zamol_qstn_lang(self,tbl_id,user_id):
        self.c.execute("SELECT lang FROM zamol WHERE id=? and user_id=?", (tbl_id, user_id))
        ques = self.c.fetchone()
        if ques is not None:
            return ques[0]

    def change_zamol_fileid(self,file_id,question,tbl_id,user_id):
        self.c.execute("UPDATE zamol SET file_id=?,question=? WHERE id=? and user_id=?", (file_id,question,tbl_id,user_id))
        self.conn.commit()
        

    def get_zamol_question(self, tbl_id,user_id):
        self.c.execute("SELECT lang,question,file_id,group_id FROM zamol WHERE id=? and user_id=?", (tbl_id,user_id))
        ques = self.c.fetchone()
        if ques is not None:
            return ques

    def change_zamol_qstn_message_id(self,message_id,tbl_id,user_id):
        self.c.execute("UPDATE zamol SET message_id=? WHERE id=? and user_id=?", (message_id,tbl_id,user_id))
        self.conn.commit()
        

    def update_zamol_clip_qstn(self,question,tbl_id,user_id):
        self.c.execute("UPDATE zamol SET question=? WHERE id=? and user_id=?",(question,tbl_id,user_id))
        self.conn.commit()
        

    def get_zamol_question_type(self,msg_id):
        self.c.execute("SELECT questiontype FROM zamol WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def get_zamol_qstnsby_msgid(self, msg_id,group_id):
        self.c.execute("SELECT * from zamol WHERE  message_id=? and group_id=?",(msg_id,group_id))
        ques = self.c.fetchone()
        if ques is not None:
            return ques

    def get_zamol_qstn_status(self,msg_id):
        self.c.execute("SELECT status FROM zamol WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False
    def change_zamol_qstn_status(self,status,msg_id):
        self.c.execute("UPDATE zamol SET status=? WHERE  message_id=? ", (status,msg_id))
        self.conn.commit()
        


    #################END ZAMOL###################

    ####################START GAIA###################
    def add_gaia_question(self, user_id,group_id,language,questiontype):
        self.c.execute("INSERT INTO gaia(user_id,group_id,lang,questiontype) VALUES (?,?,?,?)", ( user_id,group_id,language,questiontype))
        self.conn.commit()
        

    def get_last_gaia_id(self, user_id):
        self.c.execute("SELECT MAX(id) FROM gaia WHERE user_id=?", (user_id,))
        insta_user = self.c.fetchone()
        return int(insta_user[0])

    def get_gaia_qstn_lang(self,tbl_id,user_id):
        self.c.execute("SELECT lang FROM gaia WHERE id=? and user_id=?", (tbl_id, user_id))
        ques = self.c.fetchone()
        if ques is not None:
            return ques[0]

    def change_gaia_fileid(self,file_id,question,tbl_id,user_id):
        self.c.execute("UPDATE gaia SET file_id=?,question=? WHERE id=? and user_id=?", (file_id,question,tbl_id,user_id))
        self.conn.commit()
        

    def get_gaia_question(self, tbl_id,user_id):
        self.c.execute("SELECT lang,question,file_id,group_id FROM gaia WHERE id=? and user_id=?", (tbl_id,user_id))
        ques = self.c.fetchone()
        if ques is not None:
            return ques

    def change_gaia_qstn_message_id(self,message_id,tbl_id,user_id):
        self.c.execute("UPDATE gaia SET message_id=? WHERE id=? and user_id=?", (message_id,tbl_id,user_id))
        self.conn.commit()
        

    def update_gaia_clip_qstn(self,question,tbl_id,user_id):
        self.c.execute("UPDATE gaia SET question=? WHERE id=? and user_id=?",(question,tbl_id,user_id))
        self.conn.commit()
        

    def get_gaia_question_type(self,msg_id):
        self.c.execute("SELECT questiontype FROM gaia WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def get_gaia_qstnsby_msgid(self, msg_id,group_id):
        self.c.execute("SELECT * from gaia WHERE  message_id=? and group_id=?",(msg_id,group_id))
        ques = self.c.fetchone()
        if ques is not None:
            return ques

    def get_gaia_qstn_status(self,msg_id):
        self.c.execute("SELECT status FROM gaia WHERE message_id=?", (msg_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False
    def change_gaia_qstn_status(self,status,msg_id):
        self.c.execute("UPDATE gaia SET status=? WHERE  message_id=? ", (status,msg_id))
        self.conn.commit()
        
    #################END GAIA################
    #################GROUPS######################
    def check_group_id(self, group_id):
        self.c.execute("SELECT group_id FROM groups WHERE group_id=?", (group_id,))
        user = self.c.fetchone()
        if user is not None:
            return True
        else:
            return False

    def add_group(self, group_id, group_title, user_id):
        if self.check_group_id(group_id) == False:
            self.c.execute("INSERT INTO groups (group_id,group_title,user_id) VALUES (?,?,?)",
                               (group_id, group_title, user_id))
            self.conn.commit()
            
        else:
            return False

    def update_group_language(self,language,group_id,user_id):
        self.c.execute("UPDATE groups SET group_language=? WHERE group_id=? and  user_id=? ", (language,group_id,user_id))
        self.conn.commit()
        

    def get_group_adder(self, group_id):
        self.c.execute("SELECT user_id FROM groups WHERE group_id=?", (group_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def get_group_language(self, group_id):
        self.c.execute("SELECT group_language FROM groups WHERE group_id=?", (group_id,))
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return False

    def del_group(self, group_id):
        if self.check_group_id(group_id) == True:
            self.c.execute("DELETE FROM groups WHERE group_id=?", (group_id,))
            self.conn.commit()
            

    def get_all_group_details(self):
        data = []
        for user in self.c.execute("SELECT id,group_id,group_language FROM groups"):
            data.append(user)
        return data

########## END GROUPS ######################

##############ANSWERS##############

    def add_user_answer(self,user_id,correct,incorrect,answertype):
        if self.check_user_answer(user_id=user_id,answertype=answertype) == False:
            self.c.execute("INSERT INTO answers (user_id,correct,incorrect,answertype) VALUES (?,?,?,?)", (user_id,correct,incorrect,answertype))
            self.conn.commit()
            


    def check_user_answer(self,user_id,answertype):
        self.c.execute("SELECT user_id from answers WHERE user_id=? AND answertype=?",(user_id,answertype))
        user =self.c.fetchone()
        if user is not None:
            return int(user[0])
        else:
            return False

    def get_correct_incorrect(self,user_id,answertype):
        self.c.execute("SELECT correct,incorrect from answers WHERE user_id=? and answertype=?", (user_id,answertype))
        user = self.c.fetchone()
        if user is not None:
            return user
        else:
            return False

    def update_correct(self,correct,answertype,user_id):
        self.c.execute("UPDATE answers SET correct=?,answertype=? WHERE user_id=?",(correct,answertype,user_id))
        self.conn.commit()
        

    def update_incorrect(self,incorrect,answertype,user_id):
        self.c.execute("UPDATE answers SET incorrect=?,answertype=? WHERE user_id=?",(incorrect,answertype,user_id))
        self.conn.commit()
        

#################END ANSWERS##########################