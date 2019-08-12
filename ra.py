#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gaia
import groups
import commands
import util
import db
import config
import texts
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
from pyrogram import Client,InputPhoneContact

speech = util.Speech()
sqls =db.DBHelper()
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
def observer(update,context):
    bot_username = update.message.reply_to_message.from_user.username
    chat_type = update.message.chat.type
    user = update.message.from_user
    user_answer =update.message.text
    print(user_answer)
    if bot_username==config.BOT_USERNAME and (chat_type=="group" or chat_type=="supergroup"):

        # sqls.set_user(user_id=user.id,username=user.username,role=0)
        print(Users.check_user(user_id=user.id))
        if Users.check_user(user_id=user.id)==False:
            Users(user_id=user.id,username=user.username,role=0).save()
        message_id = update.message.reply_to_message.message_id
        qstn_type = util.question_type(message_id=message_id)
        print(qstn_type)
        if qstn_type=='apolo':
            answ = Answers.check_user_answer(user_id=user.id,answertype=qstn_type)
            print(answ)
            if answ==False:
                Answers(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type).save()


            # answer = sqls.get_apolo_answer_by_msg_id(msg_id=message_id)
            answer = Apolo.get_apolo_answer_by_msg_id(msg_id=message_id)
            # correct, incorrect = sqls.get_correct_incorrect(user_id=user.id,answertype=qstn_type
            correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype=qstn_type)
            if user_answer.lower()==answer.lower():
                print(message_id)
                print(correct, incorrect)
                # status = sqls.get_apolo_qstn_status(msg_id=message_id)
                status = Apolo.get_apolo_qstn_status(msg_id=message_id)
                print(status)
                if status == 0:
                    # sqls.change_apolo_qstn_status(status=1,msg_id=message_id)
                    Apolo.change_apolo_qstn_status(status=1,msg_id=message_id)
                    # print(correct, incorrect)
                    correct +=1
                    Answers.update_correct(correct=correct,answertype=qstn_type,user_id=user.id)
                    update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                else:
                    # print(correct, incorrect)
                    update.message.reply_text("🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
            else:
                print(correct, incorrect)
                incorrect +=1
                Answers.update_incorrect(incorrect=incorrect,answertype=qstn_type,user_id=user.id)
                update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
        elif qstn_type=='seshat':
            answ = Answers.check_user_answer(user_id=user.id, answertype=qstn_type)
            print("Answer",answ)
            if answ == False:
                Answers(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type).save()
            # sqls.add_user_answer(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type)
            # answer = sqls.get_seshat_answer_by_msg_id(msg_id=message_id)
            answer =Seshat.get_seshat_answer_by_msg_id(msg_id=message_id)
            correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype=qstn_type)
            if user_answer.lower() == answer.lower():
                # status = sqls.get_seshat_qstn_status(msg_id=message_id)
                status =Seshat.get_seshat_qstn_status(msg_id=message_id)
                if status == 0:
                    # sqls.change_seshat_qstn_status(status=1, msg_id=message_id)
                    Seshat.change_seshat_qstn_status(status=1, msg_id=message_id)
                    # print(correct, incorrect)
                    correct +=1
                    # sqls.update_correct(correct=correct, answertype=qstn_type, user_id=user.id)
                    Answers.update_correct(correct=correct, answertype=qstn_type, user_id=user.id)
                    update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                else:
                    print(correct, incorrect)
                    update.message.reply_text(
                        "🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
            else:
                # print(correct, incorrect)
                incorrect += 1
                Answers.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id)
                update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
        elif qstn_type=='zamol':
            group_id = update.message.chat.id
            answ = Answers.check_user_answer(user_id=user.id, answertype=qstn_type)
            print("Answer", answ)
            if answ == False:
                Answers(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type).save()
            # sqls.add_user_answer(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type)
            correct, incorrect = Answers.get_correct_incorrect(user_id=user.id,answertype=qstn_type)
            data = Zamol.get_zamol_qstnsby_msgid(msg_id=message_id,group_id=group_id)

            if user_answer.lower()==data.question.lower():
                status = Zamol.get_zamol_qstn_status(msg_id=message_id)
                if status == 0:
                    Zamol.change_zamol_qstn_status(status=1,msg_id=message_id)
                    print(correct, incorrect)
                    correct +=1
                    Answers.update_correct(correct=correct, answertype=qstn_type, user_id=user.id)
                    update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                else:
                    print(correct, incorrect)
                    update.message.reply_text("🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
            else:
                print(correct, incorrect)
                incorrect += 1
                Answers.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id)
                update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
        elif qstn_type=='gaia':
            try:
                group_id = update.message.chat.id
                answ = Answers.check_user_answer(user_id=user.id, answertype=qstn_type)
                print("Answer", answ)
                if answ == False:
                    Answers(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type).save()
                # sqls.add_user_answer(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type)
                # print(sqls.get_correct_incorrect(user_id=user.id, answertype=qstn_type))
                correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype=qstn_type)
                file_id = update.message.voice.file_id
                newFile = context.bot.get_file(file_id)
                newFile.download('answ_{}.ogg'.format(user.id))
                length = update.message.voice.duration
                if length < 10:
                    new = util.convert_ogg_to_wav("answ_{}.ogg".format(user.id), "stud_{}.wav".format(user.id))
                    speech.file = new
                    lang,quiz = Gaia.get_gaia_qstnsby_msgid(msg_id=message_id, group_id=group_id)
                    langue = util.language_select(language=lang)
                    text = speech.to_text(lang=langue)
                    print(text)
                    if text == 401:
                        update.message.reply_text(
                            "Hi {}, I did not understand this, please try again".format(user.first_name))
                    elif text == 500:
                        update.message.reply_text(
                            "Sorry {}, I got a little light headed, please try again".format(user.first_name))
                    elif text.lower() == quiz.lower():
                        status = Gaia.get_gaia_qstn_status(msg_id=message_id)
                        print(status)
                        if status == 0:
                            Gaia.change_gaia_qstn_status(status=1, msg_id=message_id)
                            print(correct, incorrect)
                            correct  +=1
                            Answers.update_correct(correct=correct, answertype=qstn_type, user_id=user.id)
                            update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                        else:
                            print(correct, incorrect)
                            update.message.reply_text("🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")

                    elif text.lower() != quiz.lower():
                        print(correct, incorrect)
                        incorrect += 1
                        sqls.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id)
                        update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
                    util.clear_student(user_id=user.id)
            except AttributeError:
                update.message.reply_text(f"Hi {user.first_name}, you are replying to the wrong message or in the wrong format")
            # except TypeError:
            #     pass
        else:
            update.message.reply_text(f"Hi {user.first_name}, you are replying to the wrong message or in the wrong format")






@util.send_typing_action
def cancel(update,context):
    end = ConversationHandler.END
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    chat_type = update.message.chat.type
    admins = sqls.check_admin(user.id)
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
    admin_conv = ConversationHandler(entry_points=[MessageHandler(Filters.regex('^ADD ADMIN$'), admins.admin)],
                                     states={
                                         ADMIN: [MessageHandler(Filters.text, admins.save_admin)],

                                     }, fallbacks=[CommandHandler('start', commands.start)], allow_reentry=True)
    dp.add_handler(apolo_convo)
    # dp.add_handler(seshat_convo)
    dp.add_handler(admin_conv)
    dp.add_handler(CommandHandler('start', commands.start))
    dp.add_handler(MessageHandler(Filters.regex('^POST$'), activity_select))
    dp.add_handler(CommandHandler('gid', commands.get_id))
    dp.add_handler(CallbackQueryHandler(cbhandler.jarvis))
    dp.add_handler(MessageHandler(Filters.regex('^CANCEL$'), cancel))
    dp.add_handler(MessageHandler(Filters.regex('^MANAGE GROUPS$'), groups.groups_view))
    dp.add_handler(MessageHandler(Filters.regex('^REMOVE ADMINS$'), admins.manage_admin))
    dp.add_handler(MessageHandler(Filters.regex('^PROFILE$'), admins.profile))
    dp.add_handler(MessageHandler(Filters.regex('^HELP$'), commands.start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, groups.add_group))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, groups.remove_from_group))
    dp.add_handler(MessageHandler(Filters.reply & (Filters.text | Filters.voice), observer))
    dp.add_handler((MessageHandler(Filters.reply & Filters.command, sherlock.travis)))
    dp.add_handler(MessageHandler(Filters.text & Filters.reply, sherlock.criminal))
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

