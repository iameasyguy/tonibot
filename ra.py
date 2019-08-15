#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gaia
import groups
import commands
import util
import observer
import config
import texts
import liker
import apolo
import admins
import seshat
import zamol
import sherlock
import cbhandler
from sql import *
from telegram import (ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)


speech = util.Speech()

APOLO,GROUP,SESHAT,SESHATQSTN,SESHATANSW,ADMIN,ZAMOL,LANG,GAIA,SHERLOCK,SHERPIC,HINT=range(12)

@util.send_typing_action
def activity_select(update, context):
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    chat_type = update.message.chat.type

    key_main = [[InlineKeyboardButton("Word Mixer", callback_data='apolo'),
                 InlineKeyboardButton("Listen & Write", callback_data="zamol")],
                [InlineKeyboardButton("Listen & Record", callback_data='gaia'),
                 InlineKeyboardButton("View and write", callback_data="seshat")],
                [InlineKeyboardButton("Crime Buster", callback_data='sherlock')]]
    main_markup = InlineKeyboardMarkup(key_main)
    #check user role
    role = Users.check_admin(user_id=user.id)
    print(role)

    if chat_type=='private':
        if role >0:

            context.bot.send_message(chat_id=chat_id, text=texts.ACTIVITY_SELECT.format(user.first_name),
                                     reply_markup=main_markup)
        else:
            context.bot.send_message(chat_id=chat_id, text=texts.NONE_ADMIN.format(user.first_name))
    else:
        context.bot.send_message(chat_id=chat_id,text=texts.COMMAND_NOT_ALLOWED)






@util.send_typing_action
def cancel(update,context):
    end = ConversationHandler.END
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    chat_type = update.message.chat.type
    admins = Users.check_admin(user.id)
    if int(admins) == 2:
        admin_keyboard = [['POST', 'MANAGE GROUPS'],
                          ['ADD ADMIN', 'REMOVE ADMINS'],
                          ['HELP', 'PROFILE'],
                          ['CANCEL']]

        admin_markup = ReplyKeyboardMarkup(admin_keyboard, True, False)
        if chat_type == "private":
            update.message.reply_text("Your cancelled our conversation!.")
            context.bot.send_message(chat_id=chat_id,
                                     text="Hi {}, Please select an option:\nPOST - To select activity type.\n"
                                          "MANAGE GROUPS - View and Delete groups.\nADD ADMIN - Adds a teacher.\n"
                                          "REMOVE ADMINS - View and delete teachers.\n"
                                          "HELP - Show help menu.\nPROFILE - View your user id & other details.".format(
                                         user.first_name), reply_markup=admin_markup)
    elif int(admins) == 1:
        teacher_keyboard = [['POST', 'HELP'], ['PROFILE', 'CANCEL']]
        teacher_markup = ReplyKeyboardMarkup(teacher_keyboard, True, False)
        if chat_type == "private":
            update.message.reply_text("Your cancelled our conversation!.")
            context.bot.send_message(chat_id=chat_id,
                                     text="Hi {}, Please select an option:\nPOST - To select activity type.\n"
                                          "HELP - Show help menu.\nPROFILE - View your user id & other details.".format(
                                         user.first_name), reply_markup=teacher_markup)
    else:
        update.message.reply_text("Please get yourself registered as a teacher by @UnuaLibro.")


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.TOKEN,use_context=True)

    # Get the dispatcher to register handlers CallbackQueryHandler(language)
    dp = updater.dispatcher

    apolo_convo = ConversationHandler(
        entry_points=[CallbackQueryHandler(cbhandler.jarvis)],
        states={APOLO:[MessageHandler(Filters.text,apolo.save_apolo_question)],
                SESHAT: [MessageHandler(Filters.all, seshat.picture)],
                SESHATQSTN: [MessageHandler(Filters.text, seshat.save_qstn_ask_answ)],
                SESHATANSW: [MessageHandler(Filters.text, seshat.save_answ_get_group)],
                ZAMOL:[MessageHandler(Filters.voice,zamol.clip)],
                LANG:[MessageHandler(Filters.text,zamol.edit_clip)],
                GAIA: [MessageHandler(Filters.voice, gaia.clip)],
                SHERLOCK: [MessageHandler(Filters.text, sherlock.confirm)],
                SHERPIC: [MessageHandler(Filters.photo, sherlock.picture)],
                HINT: [MessageHandler(Filters.all, sherlock.poster)],
                },
        fallbacks=[CommandHandler('start',commands.start)],
        allow_reentry=True)

    dp.add_handler(apolo_convo)
    # dp.add_handler(seshat_convo)
    dp.add_handler(MessageHandler(Filters.regex('^RECRUIT BELIEVERS$'), admins.admin))
    dp.add_handler(CommandHandler('start', commands.start))
    dp.add_handler(CommandHandler('join', commands.user_rank_join))
    dp.add_handler(CommandHandler('career', commands.user_career))
    dp.add_handler(CommandHandler('gid', commands.get_id))
    dp.add_handler(MessageHandler(Filters.regex('^ENLIGHT$'), activity_select))
    dp.add_handler(CallbackQueryHandler(cbhandler.jarvis))
    dp.add_handler(MessageHandler(Filters.regex('^CANCEL$'), cancel))
    dp.add_handler(MessageHandler(Filters.regex('^MANAGE GROUPS$'), groups.groups_view))
    dp.add_handler(MessageHandler(Filters.regex('^EXPEL BELIEVERS$'), admins.manage_admin))
    dp.add_handler(MessageHandler(Filters.regex('^PROFILE$'), admins.profile))
    dp.add_handler(MessageHandler(Filters.regex('^HELP$'), commands.start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, groups.add_group))
    dp.add_handler(MessageHandler(Filters.all,liker.message_counter))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, groups.remove_from_group))
    dp.add_handler(MessageHandler(Filters.reply & (Filters.text | Filters.voice), observer.observer))
    dp.add_handler((MessageHandler(Filters.reply & Filters.command, sherlock.travis)))

    # dp.add_handler(MessageHandler(Filters.text & Filters.reply, sherlock.criminal))
    dp.add_handler(CommandHandler('admin',admins.request_add))
    # log all errors
    dp.add_error_handler(util.error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

