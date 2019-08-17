#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from sql import *
import util
import emoji
import config
import texts




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

    admins=Users.check_admin(user_id=user.id)
    if admins==2:
        admin_keyboard = [['ENLIGHT', 'MANAGE GROUPS'],
                          ['RECRUIT BELIEVERS', 'EXPEL BELIEVERS'],
                          ['HELP','PROFILE'],
                          ['CANCEL']]

        admin_markup = ReplyKeyboardMarkup(admin_keyboard, True,False)
        if chat_type == "private":
            context.bot.send_message(chat_id=chat_id,
                         text="Hi {}, Please select an option:\nENLIGHT - To select activity type.\n"
                              "MANAGE GROUPS - View and Delete groups.\nRECRUIT BELIEVERS - Adds a teacher.\n"
                              "EXPEL BELIEVERS - View and delete teachers.\n"
                              "HELP - Show this menu.\nPROFILE - View your user id & other details.".format(
                             user.first_name), reply_markup=admin_markup)
    elif admins==1:
        teacher_keyboard = [['ENLIGHT', 'HELP'],['PROFILE','CANCEL']]
        teacher_markup = ReplyKeyboardMarkup(teacher_keyboard, True, False)
        if chat_type == "private":
            context.bot.send_message(chat_id=chat_id,
                         text="Hi {}, Please select an option:\nENLIGHT - To select activity type.\n"
                              "HELP - Show this menu.\nPROFILE - View your user id & other details.".format(
                             user.first_name), reply_markup=teacher_markup)
    else:
        update.message.reply_text("Please get yourself registered as a teacher by @UnuaLibro.")



@util.send_typing_action
def user_rank_join(update, context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    username= util.get_username(update,context)
    if chat_type=="private":
        key_main = [[InlineKeyboardButton(emoji.emojize("Continue :thumbsup:",use_aliases=True), callback_data=f"done+{user.id}")]]
        main_markup = InlineKeyboardMarkup(key_main)
        buttons = []
        for k, v in config.LINKS.items():
            buttons.append(InlineKeyboardButton(k, url=v,))
        key_main = InlineKeyboardMarkup(util.build_menu(buttons, n_cols=3))
        update.message.reply_text(emoji.emojize(texts.JOIN_MSG.format(username),use_aliases=True),reply_markup=key_main)
        update.message.reply_text(f"Hey {username} press the button below after posting a review to proceed",reply_markup=main_markup)



@util.send_typing_action
def user_career(update, context):
    username = util.get_username(update, context)
    update.message.reply_text(f"Hey {username} press the [link](https://telegra.ph/Learning-creators-progression-ranks-08-15) to see all ranks and conditions to progress\n"
                              f"Press /progress to view your actual rank and requirements for next rank",parse_mode="Markdown")

