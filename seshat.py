#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
import config
import util
import db
import ra
from sql import *


sqls =db.DBHelper()

# save the pic ask for question
@util.send_typing_action
def picture(update,context):
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    try:
        if len(update.effective_message.photo) > 0:
            file_id = update.effective_message.photo[-1].file_id
            # sqls.add_seshat_question(user_id=user.id, file_id=file_id,questiontype='seshat')
            Seshat(user_id=user.id, file_id=file_id,question_type='seshat').save()
            # bot.send_photo(chat_id=chat_id, photo=file_id)
            context.bot.send_message(text=f"Hi Admin {user.first_name}, Please enter a question for the picture e.g 'What is this?'",
                chat_id=chat_id)

            return ra.SESHATQSTN

        elif update.effective_message.document != "None":
            file_id = update.effective_message.document.file_id
            # sqls.add_seshat_question(user_id=user.id, file_id=file_id,questiontype="seshat")
            Seshat(user_id=user.id, file_id=file_id, question_type='seshat').save()
            context.bot.send_message(text=f"Hi Admin {user.first_name}, Please enter a question for the gif e.g 'What is this?'",
                chat_id=chat_id,)

            return ra.SESHATQSTN
        elif update.message.text == "CANCEL":
            return ra.cancel(update, context)
        else:
            context.bot.send_message(
                text=f"Hi Admin {user.first_name}, Please use @g_ibot or @gif to get  content to post e.g @g_ibot cat or @gif dog\nor upload a picture'",chat_id=chat_id)

            return ra.SESHAT
    except:
        if update.message.text == "CANCEL":
            return ra.cancel(update, context)
        else:
            context.bot.send_message(
                text=f"Hi Admin {user.first_name}, Please use @g_ibot or @gif to get  content to post e.g @g_ibot cat or @gif dog\nor upload a picture'",chat_id=chat_id)
            return ra.SESHAT


# save qstn ask answer
@util.send_typing_action
def save_qstn_ask_answ(update,context):
    quest = update.message.text
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    # tbl_id =sqls.get_last_seshat_id(user.id)
    tbl_id = Seshat.get_last_seshat_id(user_id=user.id)
    # sqls.change_seshat_qstn(question=quest,tbl_id=tbl_id,user_id=user.id)
    Seshat.change_seshat_qstn(question=quest,tbl_id=tbl_id,user_id=user.id)
    update.message.reply_text("Please enter an answer you expect from the students")
    return ra.SESHATANSW
#
#
@util.send_typing_action
def save_answ_get_group(update,context):
    answer = update.message.text
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    tbl_id = Seshat.get_last_seshat_id(user_id=user.id)
    # tbl_id = sqls.get_last_seshat_id(user.id)
    # sqls.change_seshat_answer(answer=answer,tbl_id=tbl_id,user_id=user.id)
    Seshat.change_seshat_answer(answer=answer,tbl_id=tbl_id,user_id=user.id)
    # group = sqls.get_all_group_details()
    group = Groups.objects
    if len(group) > 0:
        update.message.reply_text('Please select the group you want to post the Seshat trivia')
        for data in group:
            key_main = [[InlineKeyboardButton(f"{data.group_language} Group", callback_data=f'qseshat+{data.group_id}')]]
            main_markup = InlineKeyboardMarkup(key_main)
            update.message.reply_text('<-------👇---------->', reply_markup=main_markup)
        return ConversationHandler.END
    else:
        update.message.reply_text('No Groups Available please add the bot to a group and make it admin')
        return ConversationHandler.END
