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
from sql import *
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      ChatAction)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

speech = util.Speech()
sqls =db.DBHelper()
APOLO,GROUP,SESHAT,SESHATQSTN,SESHATANSW,ADMIN,ZAMOL,LANG,GAIA=range(9)

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


def jarvis(update,context):
    query = update.callback_query
    text = str(query.data)
    user = query.from_user
    # print(text)
    user_id = user.id
    if text.startswith('apolo'):
        context.bot.edit_message_text(
            text=f"Hi Admin {user.first_name}, please enter the phrase you want to post",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return APOLO
    elif text.startswith('lang'):
        language = text.split("+")[1]
        group_id = text.split("+")[2]
        Groups.update_group_language(language=language,group_id=group_id,user_id=user_id)
        context.bot.edit_message_text(
            text="The Group was saved as the official {} Group.".format(language),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
    elif text.startswith('apolq'):
        last_id = Apolo.get_last_apolo_id(user_id=user_id)
        group_id = text.split('+')[1]
        Apolo.change_apolo_qstn_group_id(group_id=group_id, qid=last_id, user_id=user_id)
        apolo_qstn = Apolo.get_apolo_question(qid=last_id)
        payload = context.bot.send_message(chat_id=group_id,
                         text=f"🧠 *Please long-press on Ro’s phrase, click reply and write the correct sentence.*\n\n📕 _{apolo_qstn}_", parse_mode=ParseMode.MARKDOWN)
        message_id = payload.message_id
        print(message_id)
        Apolo.update_apolo_msgid_qstn_type(message_id=message_id,question_type="apolo",tbl_id=last_id,user_id=user_id)
        context.bot.edit_message_text(
            text="The Message was successfully posted in the group\nTo post another message click the POST key",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ConversationHandler.END
    elif text.startswith("seshat"):
        context.bot.edit_message_text(
            text=f"Hi Admin {user.first_name}, Please use @g_ibot or @gif to get  content to post e.g @g_ibot cat or @gif dog\nor upload a picture",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return SESHAT
    elif text.startswith("qseshat"):
        print(text)
        # last_id = sqls.get_last_seshat_id(user_id)
        last_id =Seshat.get_last_seshat_id(user_id=user_id)
        group_id = text.split('+')[1]
        # sqls.change_seshat_group_id(group_id=group_id, tbl_id=last_id, user_id=user_id)
        Seshat.change_seshat_group_id(group_id=group_id, tbl_id=last_id, user_id=user_id)
        # sqls.change_qstn_status(status=2, tbl_id=tbl_id, user_id=user_id)
        # msg = sqls.get_seshat_question(last_id, user_id)
        msg = Seshat.get_seshat_question(qid=last_id,user_id=user_id)
        swali, file_id = msg
        try:
            payload = context.bot.send_photo(chat_id=group_id, photo=file_id,
                                     caption="*{}*\n\n🌴 _Please long-press on Ro’s sentence / word, click reply and write the missing / correct word(s)._".format(
                                         swali), parse_mode="Markdown")
        except:
            payload = context.bot.send_document(chat_id=group_id, document=file_id,
                                        caption="*{}*\n\n🌴 _Please long-press on Ro’s sentence / word, click reply and write the missing / correct word(s)._".format(
                                            swali), parse_mode="Markdown")

        message_id = payload.message_id
        print(message_id)
        # sqls.change_seshat_message_id(message_id=message_id, tbl_id=last_id, user_id=user_id)
        Seshat.change_seshat_message_id(message_id=message_id, tbl_id=last_id, user_id=user_id)
        context.bot.edit_message_text(
            text="The Message was successfully posted in the group\nTo post another message click the POST key",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ConversationHandler.END
    elif text.startswith('gdel'):
        g_id = text.split('+')[1]
        Groups.del_group(group_id=int(g_id))
        print(g_id)
        context.bot.edit_message_text(
            text="The group was deleted successfully!\nYou will not be able to post in the group anymore",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id, )
    elif text.startswith('usr'):
        admin_id = text.split('+')[1]
        # sqls.delete_admin(admin_id=admin_id)
        Users.delete_admin(user_id=admin_id)
        context.bot.edit_message_text(
            text="The Teacher was successfully deleted",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
    elif text.startswith('zamol'):
        # group = sqls.get_all_group_details()
        group =Groups.objects
        if len(group) > 0:

            for data in group:
                key_main = [[InlineKeyboardButton(f"{data.group_language} Group", callback_data=f'gzamol+{data.group_id}+{data.group_language}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                context.bot.edit_message_text(
                    text="Please select the group you want to post the Zamolxis trivia",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id, reply_markup=main_markup)
            # return ConversationHandler.END
        else:
            context.bot.edit_message_text(
                text="No Groups Available please add the bot to a group and make it admin",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)

            return ConversationHandler.END
    elif text.startswith('gzamol'):
        print(text)
        group_id = text.split('+')[1]
        language = text.split('+')[2]
        # sqls.add_zamol_question(user_id=user_id,group_id=group_id,language=language,questiontype='zamol')
        Zamol(user_id=user_id,group_id=group_id,language=language,questiontype='zamol').save()
        context.bot.edit_message_text(
            text=f"Please record your message in {language}",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ZAMOL
    elif text.startswith('yesz'):
        tbl_id = text.split('+')[1]
        # lang, qstn,file_id,g_id = sqls.get_zamol_question(tbl_id=tbl_id,user_id=user_id)
        lang, qstn, file_id, g_id = Zamol.get_zamol_question(tbl_id=tbl_id, user_id=user.id)
        payload = context.bot.send_voice(chat_id=g_id, voice=file_id,
                                 caption="🗣Please listen to Ro’s recording, then long-press, click reply and write what you heard!")
        message_id = payload.message_id
        print(message_id)
        sqls.change_zamol_qstn_message_id(message_id=message_id,tbl_id=tbl_id,user_id=user_id)
        context.bot.edit_message_text(
            text="The Message was successfully posted in the group\nTo post another message click the POST button",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ConversationHandler.END
    elif text.startswith("noz"):
        context.bot.edit_message_text(
            text="Please record you clip once again!",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ZAMOL
    elif text.startswith('edit'):
        context.bot.edit_message_text(
            text="Please enter the textual pronunciation",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return LANG
    elif text.startswith('gaia'):
        group = sqls.get_all_group_details()
        if len(group) > 0:

            for data in group:
                key_main = [[InlineKeyboardButton(f"{data[2]} Group", callback_data=f'cgaia+{data[1]}+{data[2]}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                context.bot.edit_message_text(
                    text="Please select the group you want to post the Gaia trivia",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id, reply_markup=main_markup)
            # return ConversationHandler.END
        else:
            context.bot.edit_message_text(
                text="No Groups Available please add the bot to a group and make it admin",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)

            return ConversationHandler.END
    elif text.startswith('cgaia'):
        print(text)
        group_id = text.split('+')[1]
        language = text.split('+')[2]

        sqls.add_gaia_question(user_id=user_id,group_id=group_id,language=language,questiontype='gaia')
        context.bot.edit_message_text(
            text=f"Please record your message in {language}",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return GAIA
    elif text.startswith('yesg'):
        tbl_id = text.split('+')[1]
        lang, qstn,file_id,g_id = sqls.get_gaia_question(tbl_id=tbl_id,user_id=user_id)
        payload = context.bot.send_voice(chat_id=g_id, voice=file_id,
                                 caption="🗣Please listen to Ro’s recording, then long-press, click reply and record what you heard!")
        message_id = payload.message_id
        print(message_id)
        sqls.change_gaia_qstn_message_id(message_id=message_id,tbl_id=tbl_id,user_id=user_id)
        context.bot.edit_message_text(
            text="The Message was successfully posted in the group\nTo post another message click the POST button",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ConversationHandler.END
    elif text.startswith("nog"):
        context.bot.edit_message_text(
            text="Please record you clip once again!",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return GAIA


@util.send_typing_action
def observer(update,context):
    bot_username = update.message.reply_to_message.from_user.username
    chat_type = update.message.chat.type
    user = update.message.from_user
    user_answer =update.message.text
    print(user_answer)
    if bot_username==config.BOT_USERNAME and (chat_type=="group" or chat_type=="supergroup"):

        sqls.set_user(user_id=user.id,username=user.username,role=0)
        message_id = update.message.reply_to_message.message_id
        qstn_type = util.question_type(message_id=message_id)
        print(qstn_type)
        if qstn_type=='apolo':
            sqls.add_user_answer(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type)
            answer = sqls.get_apolo_answer_by_msg_id(msg_id=message_id)
            correct, incorrect = sqls.get_correct_incorrect(user_id=user.id,answertype=qstn_type)
            if user_answer.lower()==answer.lower():
                status = sqls.get_apolo_qstn_status(msg_id=message_id)
                if status == 0:
                    sqls.change_apolo_qstn_status(status=1,msg_id=message_id)

                    # print(correct, incorrect)
                    correct =+1
                    sqls.update_correct(correct=correct,answertype=qstn_type,user_id=user.id)
                    update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                else:
                    # print(correct, incorrect)
                    update.message.reply_text("🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
            else:
                print(correct, incorrect)
                incorrect +=1
                sqls.update_incorrect(incorrect=incorrect,answertype=qstn_type,user_id=user.id)
                update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
        elif qstn_type=='seshat':
            sqls.add_user_answer(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type)
            answer = sqls.get_seshat_answer_by_msg_id(msg_id=message_id)
            correct, incorrect = sqls.get_correct_incorrect(user_id=user.id,answertype=qstn_type)
            if user_answer.lower() == answer.lower():
                status = sqls.get_seshat_qstn_status(msg_id=message_id)
                if status == 0:
                    sqls.change_seshat_qstn_status(status=1, msg_id=message_id)
                    # print(correct, incorrect)
                    correct = +1
                    sqls.update_correct(correct=correct, answertype=qstn_type, user_id=user.id)
                    update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                else:
                    print(correct, incorrect)
                    update.message.reply_text(
                        "🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
            else:
                # print(correct, incorrect)
                incorrect += 1
                sqls.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id)
                update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
        elif qstn_type=='zamol':
            group_id = update.message.chat.id
            sqls.add_user_answer(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type)
            correct, incorrect = sqls.get_correct_incorrect(user_id=user.id,answertype=qstn_type)
            data = sqls.get_zamol_qstnsby_msgid(msg_id=message_id,group_id=group_id)
            if user_answer.lower()==data[3].lower():
                status = sqls.get_zamol_qstn_status(msg_id=message_id)
                if status == 0:
                    sqls.change_zamol_qstn_status(status=1,msg_id=message_id)
                    print(correct, incorrect)
                    correct = +1
                    sqls.update_correct(correct=correct, answertype=qstn_type, user_id=user.id)
                    update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                else:
                    print(correct, incorrect)
                    update.message.reply_text("🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
            else:
                print(correct, incorrect)
                incorrect += 1
                sqls.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id)
                update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
        elif qstn_type=='gaia':
            try:
                group_id = update.message.chat.id
                sqls.add_user_answer(user_id=user.id, correct=0, incorrect=0, answertype=qstn_type)
                print(sqls.get_correct_incorrect(user_id=user.id, answertype=qstn_type))
                correct, incorrect = sqls.get_correct_incorrect(user_id=user.id, answertype=qstn_type)
                file_id = update.message.voice.file_id
                newFile = context.bot.get_file(file_id)
                newFile.download('answ_{}.ogg'.format(user.id))
                length = update.message.voice.duration
                if length < 10:
                    new = util.convert_ogg_to_wav("answ_{}.ogg".format(user.id), "stud_{}.wav".format(user.id))
                    speech.file = new
                    data = sqls.get_gaia_qstnsby_msgid(msg_id=message_id, group_id=group_id)
                    langue = util.language_select(language=data[7])
                    text = speech.to_text(lang=langue)
                    print(text)
                    if text == 401:
                        update.message.reply_text(
                            "Hi {}, I did not understand this, please try again".format(user.first_name))
                    elif text == 500:
                        update.message.reply_text(
                            "Sorry {}, I got a little light headed, please try again".format(user.first_name))
                    elif text.lower() == data[3].lower():
                        status = sqls.get_gaia_qstn_status(msg_id=message_id)
                        print(status)
                        if status == 0:
                            sqls.change_gaia_qstn_status(status=1, msg_id=message_id)
                            print(correct, incorrect)
                            correct = +1
                            sqls.update_correct(correct=correct, answertype=qstn_type, user_id=user.id)
                            update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                        else:
                            print(correct, incorrect)
                            update.message.reply_text("🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")

                    elif text.lower() != data[3].lower():
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
        entry_points=[CallbackQueryHandler(jarvis)],
        states={APOLO:[MessageHandler(Filters.text,apolo.save_apolo_question)],
                SESHAT: [MessageHandler(Filters.all, seshat.picture)],
                SESHATQSTN: [MessageHandler(Filters.text, seshat.save_qstn_ask_answ)],
                SESHATANSW: [MessageHandler(Filters.text, seshat.save_answ_get_group)],
                ZAMOL:[MessageHandler(Filters.voice,zamol.clip)],
                LANG:[MessageHandler(Filters.text,zamol.edit_clip)],
                GAIA: [MessageHandler(Filters.voice, gaia.clip)],
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
    dp.add_handler(CallbackQueryHandler(jarvis))
    dp.add_handler(MessageHandler(Filters.regex('^CANCEL$'), cancel))
    dp.add_handler(MessageHandler(Filters.regex('^MANAGE GROUPS$'), groups.groups_view))
    dp.add_handler(MessageHandler(Filters.regex('^REMOVE ADMINS$'), admins.manage_admin))
    dp.add_handler(MessageHandler(Filters.regex('^PROFILE$'), admins.profile))
    dp.add_handler(MessageHandler(Filters.regex('^HELP$'), commands.start))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, groups.add_group))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, groups.remove_from_group))
    dp.add_handler(MessageHandler(Filters.reply & (Filters.text | Filters.voice), observer))
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

