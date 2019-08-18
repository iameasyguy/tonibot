#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import operator
import  random
from functools import wraps
from telegram import ChatAction
import speech_recognition as sr
import os
import subprocess
# Enable logging
import db
from sql import *
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

sqls =db.DBHelper()

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def randomize(word):
    x = word.split(" ")
    z = sorted(x, key=lambda k: random.random())
    return " ".join(z)



def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def question_type(message_id):
    # apolo_qstn_type = sqls.get_apolo_question_type(msg_id=message_id)
    try:
        apolo_qstn_type = Apolo.get_apolo_question_type(msg_id=message_id)
        seshat_qstn_type = Seshat.get_seshat_question_type(msg_id=message_id)
        zamol_qstn_type = Zamol.get_zamol_question_type(msg_id=message_id)
        gaia_qstn_type = Gaia.get_gaia_question_type(msg_id=message_id)
        sherlock_qstn_type = Sherlock.get_sherlock_question_type(msg_id=message_id)
    except IndexError:
        pass
    if apolo_qstn_type != False:
        qstn_type = apolo_qstn_type
        return qstn_type
    elif seshat_qstn_type != False:
        qstn_type = seshat_qstn_type
        return qstn_type
    elif zamol_qstn_type != False:
        qstn_type = zamol_qstn_type
        return qstn_type
    elif gaia_qstn_type != False:
        qstn_type = gaia_qstn_type
        return qstn_type
    elif sherlock_qstn_type != False:
        qstn_type = sherlock_qstn_type
        return qstn_type



def validate(s):
    try:
        if len(s)>7 and int(s):
            return True
        else:
            return False
    except ValueError:
        return False


def convert_ogg_to_wav(ogg_file, wav_file):
    """
    :return: convert ogg file to wav file
    """
    src_filename = ogg_file
    dest_filename = wav_file
    exists = os.path.isfile(wav_file)
    if exists:
        os.remove(wav_file)

    process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
    print(process)
    if process.returncode != 0:
        raise Exception("Something went wrong")
    return dest_filename

def clear_teacher(user_id):
    try:
        os.remove("voi_{}.wav".format(user_id))
        os.remove("clip_{}.ogg".format(user_id))
    except:
        pass
    return True


def clear_student(user_id):
    try:
        os.remove("stud_{}.wav".format(user_id))
        os.remove("answ_{}.ogg".format(user_id))
    except:
        pass
    return True

def language_select(language):
    if language=="English":
        return "en-GB"
    elif language=="French":
        return  "fr-FR"
    elif language =="Spanish":
        return "es-ES"
    elif language =="Arabic":
        return "ar-AE"
    elif language =="German":
        return "de-DE"
    elif language =="Italian":
        return "it-IT"
    elif language =="Portuguese":
        return "pt-PT"
    elif language =="Polish":
        return "pl-PL"
    elif language =="Romanian":
        return "ro-RO"


class Speech():

    def __init__(self, file = ""):
        self.r = sr.Recognizer()
        self._file = file

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value


    def to_text(self,lang):
        try:
            harvard = sr.AudioFile(self._file)
            # print(self.file + "******" * 100)
            with harvard as source:
                audio = self.r.record(source)
                # print(audio)
            return self.r.recognize_google(audio, language=lang)
        except sr.WaitTimeoutError:
            return 500
        except sr.UnknownValueError:
            return 401


def get_username(update,context):
    user = update.message.from_user
    if user.username ==None:
        return user.first_name
    else:
        return user.username

def get_user_position(user_id,username,group_id):
    try:
        data = []
        for userid in Answers.objects.distinct('user_id'):
            data.append(Answers.get_all_users_points(user_id=userid, group_id=group_id))
        scoreboard = dict((x, y) for x, y in data)
        scoreboard_x = sorted(scoreboard.items(), key=operator.itemgetter(1), reverse=True)
        points = Answers.get_all_points_by_group(user_id=user_id, group_id=group_id)
        position = scoreboard_x.index((username, points))
        position += 1
        return position
    except :
        return "Not on scoreboard!"

def top_scoreboard(group_id):
    data = []
    for user_id in Answers.objects.distinct('user_id'):
        data.append(Answers.get_all_users_points(user_id=user_id, group_id=group_id))
    scoreboard = dict((x, y) for x, y in data)
    scoreboard_x = sorted(scoreboard.items(), key=operator.itemgetter(1), reverse=True)[:10]
    position = 0
    score = []
    for each in scoreboard_x:
        position += 1
        score.append(f"*{position}*.  *@{each[0]}* earned *{each[1]}* points")
    return score