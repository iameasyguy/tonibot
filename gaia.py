#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, ParseMode
from telegram.ext import ConversationHandler
from sql import *
from util import Speech,convert_ogg_to_wav, clear_teacher,clear_student,validate,language_select
import util
import db
import ro
sqls =db.DBHelper()
speech = Speech()

@util.send_typing_action
def clip(update,context):
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    chat_type = update.message.chat.type
    # tbl_id =sqls.get_last_gaia_id(user_id=user.id)
    tbl_id =Gaia.get_last_gaia_id(user_id=user.id)
    # user_id,language,file_id
    if chat_type=="private":
        file_id = update.message.voice.file_id
        newFile = context.bot.get_file(file_id)
        newFile.download('clip_{}.ogg'.format(user.id))
        length = update.message.voice.duration
        if length<10:
            new = convert_ogg_to_wav("clip_{}.ogg".format(user.id), "voi_{}.wav".format(user.id))
            speech.file = new

            # get_lang = sqls.get_gaia_qstn_lang(tbl_id=tbl_id,user_id=user.id)
            get_lang = Gaia.get_gaia_qstn_lang(tbl_id=tbl_id, user_id=user.id)
            print(get_lang)
            lan = language_select(language=get_lang)
            text = speech.to_text(lang=lan)
            print(text)
            if text==401:
                update.message.reply_text("Hi {}, I did not understand this, please try again".format(user.first_name))
                clear_teacher(user_id=user.id)
                return ro.GAIA
            elif text==500:
                update.message.reply_text("Sorry {}, I got a little light headed, please try again".format(user.first_name))
                clear_teacher(user_id=user.id)
                return ro.GAIA
            else:
                # sqls.change_gaia_fileid(file_id=file_id,question=text,user_id=user.id,tbl_id=tbl_id)
                Gaia.change_gaia_fileid(file_id=file_id, question=text, user_id=user.id, tbl_id=tbl_id)
                clear_teacher(user_id=user.id)
                key_main = [[InlineKeyboardButton("Correct👌", callback_data=f'yesg+{tbl_id}'),
                             InlineKeyboardButton("Repeat❌", callback_data="nog")]]
                main_markup = InlineKeyboardMarkup(key_main)
                loadpay = context.bot.send_message(chat_id=update.message.chat_id, text="Processing ...")
                messageid = loadpay.message_id
                context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
                context.bot.edit_message_text(
                    text=f"Did you say:-\n\n_{text.capitalize()}_\n\nSelect Correct👌 to post in group or Repeat❌ to record again. ",
                    chat_id=chat_id,
                    message_id=messageid,parse_mode=ParseMode.MARKDOWN,reply_markup=main_markup)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Your recording should be only 10 seconds or less, Please try again!")
            clear_teacher(user_id=user.id)
            return ro.GAIA




