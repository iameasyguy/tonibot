#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import util
import db
from sql import *
import config
sqls = db.DBHelper()

# ######################ADD GROUP ###################




@util.send_typing_action
def add_group(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    if (chat_type == "group" or chat_type=="supergroup"):
        group_id = update.message.chat.id
        user_id = user.id
        group_title = update.message.chat.title
        for i in update.message.new_chat_members:
            if i.username == config.BOT_USERNAME:
                if Groups.check_group_id(group_id) == False:
                    Groups(group_id=group_id, group_title=group_title, user_id=user_id).save()
                    languages = config.LANGUAGES
                    buttons = []
                    for x in languages:
                        buttons.append(InlineKeyboardButton(x, callback_data="lang+{}+{}".format(x,group_id)))

                    reply_markup = InlineKeyboardMarkup(util.build_menu(buttons, n_cols=3))
                    context.bot.send_message(user_id,"I was added successfully to {}, please make me an admin in the group and select the default language".format(update.message.chat.title),reply_markup=reply_markup)
                else:
                    context.bot.send_message(user_id,"I am already a member of {},just make me and admin if you haven't yet".format(update.message.chat.title))


@util.send_typing_action
def remove_from_group(update,context):

    user = update.message.from_user
    chat_type = update.message.chat.type

    if chat_type != "private":
        # print(update)
        group_id = update.message.chat.id
        user_name = user.username
        bot_username = update.message.left_chat_member.username

        if bot_username == config.BOT_USERNAME:
            adder = Groups.get_group_adder(group_id=group_id)

            Groups.del_group(group_id=group_id)
            context.bot.send_message(adder, "I was removed from {} by @{}".format(update.message.chat.title, user_name))



@util.send_typing_action
def groups_view(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    add_det = Groups.objects
    admins = Users.check_admin(user_id=user.id)
    # print(len(add_det))
    if chat_type == "private":
        if admins==2:
            if len(add_det)>0:
                for data in add_det:
                    key_main = [[InlineKeyboardButton("Delete", callback_data='gdel+{}'.format(data.group_id))]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    update.message.reply_text('Group name: {}\nGroup ID: {}'.format(data.group_title, data.group_id), reply_markup=main_markup)
            else:
                update.message.reply_text('No Groups Available, add the bot to the group and make it admin')

#################END GROUP MANAGEMNT#####################
