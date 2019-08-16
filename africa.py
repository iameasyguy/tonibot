#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import emoji
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from mwt import MWT
import util
from sql import *

@MWT(timeout=60*60)
def get_admin_ids(context, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in context.bot.get_chat_administrators(chat_id)]



def trivia_file(language):
    # Open file
    fileHandler = open("data/{}.txt".format(language), "r", encoding="utf-8")
    # Get list of all lines in file
    listOfLines = fileHandler.readlines()
    # Close file
    fileHandler.close()
    data = []
    for x in listOfLines:
        data.append(x.strip().split(","))
    question, answer = random.choice(data)
    b, option1 = random.choice(data)
    c, option2 = random.choice(data)
    d, option3 = random.choice(data)

    pick = [answer, option1, option2, option3]
    random.shuffle(pick)
    # Random selection for the question

    return question, answer, pick


def trivia_game(update,context):
    try:
        group_id = update.callback_query.message.chat.id
        group_language = Groups.get_group_language(group_id=group_id)
        question, answer, pick = trivia_file(language=group_language)
        message_id = update.callback_query.message.message_id
        print(question, answer, message_id)
        Afrique(question=question.strip(), answer=answer.strip(), message_id=message_id, pickone=pick[0].strip(),
                         picktwo=pick[1].strip(), pickthree=pick[2].strip(), pickfour=pick[3].strip(),
                         group_id=group_id,question_type ='africa').save()

        Africhance.drop_collection()

        key_main = [[InlineKeyboardButton(pick[0], callback_data='A')],
                    [InlineKeyboardButton(pick[1], callback_data='B')],
                    [InlineKeyboardButton(pick[2], callback_data='C')],
                    [InlineKeyboardButton(pick[3], callback_data='D')]]
        main_markup = InlineKeyboardMarkup(key_main)
        context.bot.edit_message_text(
            text=emoji.emojize(f":man: AFRICA asks:What does *{question.upper()}* mean?",
                               use_aliases=True),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id, reply_markup=main_markup,
            parse_mode=ParseMode.MARKDOWN)
        context.bot.pin_chat_message(chat_id=update.callback_query.message.chat_id,
                             message_id=update.callback_query.message.message_id, disable_notification=True)
    except AttributeError:
        pass



def game(update,context):
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    chat_type = update.message.chat.type
    if chat_type!="private":
        if user.id in get_admin_ids(context,chat_id):
            key_main = [[InlineKeyboardButton("START GAME", callback_data='startgame'),
                         InlineKeyboardButton("STOP GAME", callback_data='stopgame')]
                , [InlineKeyboardButton("PAUSE GAME", callback_data='pausegame')]]
            main_markup = InlineKeyboardMarkup(key_main)
            context.bot.send_message(chat_id, "Hi Admin {},\nSELECT A TRIVIA GAME OPTION:".format(user.username), reply_markup=main_markup)
    else:
        pass





def stop_trivia(update,context):
    chat_id = update.callback_query.message.chat.id
    key_main = [[InlineKeyboardButton("Click here continue! (Only Admins)", callback_data="continue")]]
    main_markup = InlineKeyboardMarkup(key_main)
    context.bot.send_message(chat_id, emoji.emojize("GAME OVER :fist:", use_aliases=True), reply_markup=main_markup)
    context.bot.unpin_chat_message(chat_id)


def pause_trivia(update,context):
    """Stoping the Trivia Game"""
    chat_id = update.callback_query.message.chat.id
    key_main = [[InlineKeyboardButton("Click here continue! (Only Admins)", callback_data="continue")] ]
    main_markup = InlineKeyboardMarkup(key_main)
    context.bot.send_message(chat_id, emoji.emojize("GAME PAUSED :raised_hand:"), reply_markup=main_markup)
    context.bot.unpin_chat_message(chat_id)