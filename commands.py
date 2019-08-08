#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from telegram import ReplyKeyboardMarkup
from sql import *
import util
import db
import config
sqls = db.DBHelper()




@util.send_typing_action
def get_id(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type

    if chat_type !="private":
        group_id = update.message.chat.id
        update.message.reply_text("The group's ID is : {}".format(group_id))
    else:
        update.message.reply_text("Your User ID is : {}".format(user.id))


@util.send_typing_action
def start(update, context):
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    chat_type = update.message.chat.type
    # admins = sqls.check_admin(user.id)
    admins=Users.check_admin(user_id=user.id)
    if int(admins)==2:
        admin_keyboard = [['POST', 'MANAGE GROUPS'],
                          ['ADD ADMIN', 'REMOVE ADMINS'],
                          ['HELP','PROFILE'],
                          ['CANCEL']]

        admin_markup = ReplyKeyboardMarkup(admin_keyboard, True,False)
        if chat_type == "private":
            context.bot.send_message(chat_id=chat_id,
                         text="Hi {}, Please select an option:\nPOST - To select activity type.\n"
                              "MANAGE GROUPS - View and Delete groups.\nADD ADMIN - Adds a teacher.\n"
                              "REMOVE ADMINS - View and delete teachers.\n"
                              "HELP - Show this menu.\nPROFILE - View your user id & other details.".format(
                             user.first_name), reply_markup=admin_markup)
    elif int(admins)==1:
        teacher_keyboard = [['POST', 'HELP'],['PROFILE','CANCEL']]
        teacher_markup = ReplyKeyboardMarkup(teacher_keyboard, True, False)
        if chat_type == "private":
            context.bot.send_message(chat_id=chat_id,
                         text="Hi {}, Please select an option:\nPOST - To select activity type.\n"
                              "HELP - Show this menu.\nPROFILE - View your user id & other details.".format(
                             user.first_name), reply_markup=teacher_markup)
    else:
        update.message.reply_text("Please get yourself registered as a teacher by @UnuaLibro.")

