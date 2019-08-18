import operator

import emoji
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from pyrogram import Client
import config
import ra
import africa
import util
import texts
from sql import *
condition = True

def jarvis(update,context):
    query = update.callback_query
    text = str(query.data)
    user = query.from_user
    chat_type =query.message.chat.type
    user_id = user.id
    chat_id =query.message.chat.id
    if chat_type =='private':
        if text.startswith('apolo'):
            context.bot.edit_message_text(
                text=f"Hi Admin {user.first_name}, please enter the phrase you want to post",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)
            return ra.APOLO
        elif text.startswith('lang'):
            language = text.split("+")[1]
            group_id = text.split("+")[2]
            Groups.update_group_language(language=language, group_id=group_id, user_id=user_id)
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
                                               text=f"🧠 *Please long-press on Ra’s phrase, click reply and write the correct sentence.*\n\n📕 _{apolo_qstn}_",
                                               parse_mode=ParseMode.MARKDOWN)
            message_id = payload.message_id
            print(message_id)
            Apolo.update_apolo_msgid_qstn_type(message_id=message_id, question_type="apolo", tbl_id=last_id,
                                               user_id=user_id)
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
            return ra.SESHAT
        elif text.startswith("qseshat"):
            print(text)
            # last_id = sqls.get_last_seshat_id(user_id)
            last_id = Seshat.get_last_seshat_id(user_id=user_id)
            group_id = text.split('+')[1]
            # sqls.change_seshat_group_id(group_id=group_id, tbl_id=last_id, user_id=user_id)
            Seshat.change_seshat_group_id(group_id=group_id, tbl_id=last_id, user_id=user_id)
            # sqls.change_qstn_status(status=2, tbl_id=tbl_id, user_id=user_id)
            # msg = sqls.get_seshat_question(last_id, user_id)
            msg = Seshat.get_seshat_question(qid=last_id, user_id=user_id)
            swali, file_id = msg
            try:
                payload = context.bot.send_photo(chat_id=group_id, photo=file_id,
                                                 caption="*{}*\n\n🌴 _Please long-press on Ra’s sentence / word, click reply and write the missing / correct word(s)._".format(
                                                     swali), parse_mode="Markdown")
            except:
                payload = context.bot.send_document(chat_id=group_id, document=file_id,
                                                    caption="*{}*\n\n🌴 _Please long-press on Ra’s sentence / word, click reply and write the missing / correct word(s)._".format(
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
            group = Groups.objects
            if len(group) > 0:

                for data in group:
                    key_main = [[InlineKeyboardButton(f"{data.group_language} Group",
                                                      callback_data=f'gzamol+{data.group_id}+{data.group_language}')]]
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
            Zamol(user_id=user_id, group_id=group_id, lang=language, question_type='zamol').save()
            context.bot.edit_message_text(
                text=f"Please record your message in {language}",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)
            return ra.ZAMOL
        elif text.startswith('yesz'):
            tbl_id = text.split('+')[1]
            # lang, qstn,file_id,g_id = sqls.get_zamol_question(tbl_id=tbl_id,user_id=user_id)
            lang, qstn, file_id, g_id = Zamol.get_zamol_question(tbl_id=tbl_id, user_id=user.id)
            payload = context.bot.send_voice(chat_id=g_id, voice=file_id,
                                             caption="🗣Please listen to Ra’s recording, then long-press, click reply and write what you heard!")
            message_id = payload.message_id
            print(message_id)
            Zamol.change_zamol_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
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
            return ra.ZAMOL
        elif text.startswith('edit'):
            context.bot.edit_message_text(
                text="Please enter the textual pronunciation",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)
            return ra.LANG
        elif text.startswith('gaia'):
            # group = sqls.get_all_group_details()
            group = Groups.objects
            if len(group) > 0:

                for data in group:
                    key_main = [[InlineKeyboardButton(f"{data.group_language} Group",
                                                      callback_data=f'cgaia+{data.group_id}+{data.group_language}')]]
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

            # sqls.add_gaia_question(user_id=user_id,group_id=group_id,language=language,questiontype='gaia')
            Gaia(user_id=user_id, group_id=group_id, lang=language, question_type='gaia').save()
            context.bot.edit_message_text(
                text=f"Please record your message in {language}",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)
            return ra.GAIA
        elif text.startswith('yesg'):
            tbl_id = text.split('+')[1]
            # lang, qstn,file_id,g_id = sqls.get_gaia_question(tbl_id=tbl_id,user_id=user_id)
            lang, qstn, file_id, g_id = Gaia.get_gaia_question(tbl_id=tbl_id, user_id=user_id)
            payload = context.bot.send_voice(chat_id=g_id, voice=file_id,
                                             caption="🗣Please listen to Ra’s recording, then long-press, click reply and record what you heard!")
            message_id = payload.message_id
            print(message_id)
            # sqls.change_gaia_qstn_message_id(message_id=message_id,tbl_id=tbl_id,user_id=user_id)
            Gaia.change_gaia_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
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
            return ra.GAIA
        elif text.startswith('sherlock'):
            key_main = [[InlineKeyboardButton("Post new", callback_data='post')],
                        [InlineKeyboardButton("Post hint", callback_data='hint')]]
            main_markup = InlineKeyboardMarkup(key_main)
            context.bot.edit_message_text(
                text="Please select an option to proceed",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id, reply_markup=main_markup)
        elif text.startswith('post'):
            key_main = [[InlineKeyboardButton("Only text📜", callback_data='words')]
                , [InlineKeyboardButton("Image 📷 & Text📜️", callback_data='image')]]
            main_markup = InlineKeyboardMarkup(key_main)
            context.bot.edit_message_text(
                text=f"Hi Admin {user.first_name}, please select the type of scenario(plot) you want to post",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id, reply_markup=main_markup)

        elif text.startswith('hint'):
            context.bot.edit_message_text(
                text=f"Hi Admin {user.first_name}, please send the hint you want to post",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id, parse_mode=ParseMode.MARKDOWN)
            return ra.HINT

        elif text.startswith('words'):
            Sherlock(user_id=user_id, question_type='sherlock').save()
            context.bot.edit_message_text(
                text="Please enter the rules and scenario(plot) you want to post - _Text only!_",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id, parse_mode=ParseMode.MARKDOWN)
            return ra.SHERLOCK
        elif text.startswith('image'):
            Sherlock(user_id=user_id, question_type='sherlock').save()
            context.bot.edit_message_text(
                text="Please send the image for the scenario(plot)",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)
            return ra.SHERPIC
        elif text.startswith('confirm'):
            group = Groups.objects
            if len(group) > 0:

                for data in group:
                    key_main = [[InlineKeyboardButton(f"{data.group_language} Group",
                                                      callback_data=f'psher+{data.group_id}+{data.group_language}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.edit_message_text(
                        text="Please select the group you want to post the Crime trivia",
                        chat_id=update.callback_query.message.chat_id,
                        message_id=update.callback_query.message.message_id, reply_markup=main_markup)
                # return ConversationHandler.END
            else:
                context.bot.edit_message_text(
                    text="No Groups Available please add the bot to a group and make it admin",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id)

                return ConversationHandler.END
        elif text.startswith('psher'):
            g_id = text.split('+')[1]
            tbl_id = Sherlock.get_last_sherlock_id(user_id=user.id)
            # sql.change_qstn_group_id(group_id=g_id, tbl_id=tbl_id, user_id=user_id)
            Sherlock.change_sherlock_group_id(group_id=g_id, tbl_id=tbl_id, user_id=user_id)
            # sql.change_qstn_status(status=2, tbl_id=tbl_id, user_id=user_id)
            # msg = sql.get_question(tbl_id, user_id)
            msg = Sherlock.get_sherlock_question(tbl_id=tbl_id, user_id=user_id)
            swali, file_id = msg
            if file_id == "0":
                key_main = [[InlineKeyboardButton("👣 Join",callback_data='join')]]
                main_markup = InlineKeyboardMarkup(key_main)

                Sherlockchance.drop_collection()
                payload = context.bot.send_message(chat_id=g_id, text="{}\n\n\n{}".format(swali, texts.RULES),
                                                   parse_mode=ParseMode.MARKDOWN,reply_markup=main_markup)
                message_id = payload.message_id
                print(message_id)
                # sql.change_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
                Sherlock.change_sherlock_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
                # add game
                # sql.add_game(admin=user_id,game_no=message_id,group_id=g_id)#
                Games(admin_id=user_id, game_no=message_id, group_id=g_id).save()
                context.bot.edit_message_text(
                    text="The Message was successfully posted in the group\nTo post another message click the POST key",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id)
                return ConversationHandler.END
            else:
                key_main = [[InlineKeyboardButton("👣 Join", callback_data='join')]]
                main_markup = InlineKeyboardMarkup(key_main)
                context.bot.send_photo(chat_id=g_id, photo=file_id)
                payload = context.bot.send_message(chat_id=g_id, text="{}\n\n\n{}".format(swali, texts.RULES),
                                                   parse_mode=ParseMode.MARKDOWN,reply_markup=main_markup)
                message_id = payload.message_id
                print(message_id)
                # sql.change_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
                Sherlock.change_sherlock_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
                Games(admin=user_id, game_no=message_id, group_id=g_id).save()
                # sql.add_game(admin=user_id, game_no=message_id,group_id=g_id)#
                Sherlockchance.drop_collection()
                context.bot.edit_message_text(
                    text="The Message was successfully posted in the group\nTo post another message click the POST key",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id)
                return ConversationHandler.END
        elif text.startswith('cancel'):
            context.bot.edit_message_text(
                text="Your Canceled our conversation! You can always start again.",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)
            return ConversationHandler.END
        elif text.startswith('phint'):
            print(text)
            print(text.split(' '))
            grp_id = text.split(' ')[1]
            message = config.LIST.get(user_id)
            app = Client("my_account", api_id=config.api_id, api_hash=config.api_hash)
            with app as app:

                app.send_message(chat_id=grp_id, text=message)
            context.bot.edit_message_text(
                text="The hint was posted successfully!",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id, )
            return ConversationHandler.END

        elif text.startswith('approve'):
            user_id = text.split('+')[1]
            user_name = text.split('+')[2]
            admin = Users.check_admin(user_id=user_id)
            print(admin)
            if admin !=False:
                context.bot.edit_message_text(
                    text=f"{user_name} is already an admin!",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id, )
                context.bot.send_message(chat_id=user_id, text=f"Hi {user_name} you are already an admin")

            else:
                Users(user_id=int(user_id), username=user_name, role=1).save()
                context.bot.edit_message_text(
                    text=f"{user_name} was added as an admin!",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id, )
                context.bot.send_message(chat_id=user_id, text=f"Hi,{user_name} your request was approved!")
        elif text.startswith('deny'):
            user_id = text.split('+')[1]
            context.bot.edit_message_text(
                text="The request was declined!",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id, )
            context.bot.send_message(chat_id=user_id, text=f"Hi, your request was declined!")

        elif text.startswith('done'):
            user_id = text.split('+')[1]
            if Ranking.check_ranking_status(user_id=user_id):
                context.bot.edit_message_text(
                    text=f"Hi {user.first_name},You already joined Press /progress to view your actual rank and requirements for next rank",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id, parse_mode="Markdown")
            else:
                Ranking(user_id=user_id,status=1).save()
                context.bot.edit_message_text(
                    text=f"Thanks {user.first_name},Open this [link](https://telegra.ph/Learning-creators-progression-ranks-08-15) to see all ranks and conditions to progress or send /career",
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id, parse_mode="Markdown")
    # group
    else:
        global condition
        print(text)
        if text=="startgame" and (user_id in africa.get_admin_ids(context,chat_id)):
            condition = True
            return africa.trivia_game(update,context)

        elif text =="stopgame" and user_id in africa.get_admin_ids(context,chat_id):
            condition = False
            return africa.stop_trivia(update,context)
        elif text == "continue" and user_id in africa.get_admin_ids(context, chat_id):
            condition = True
            return africa.trivia_game(update,context)
        elif text == "pausegame" and user_id in africa.get_admin_ids(context, chat_id):
            condition = False
            return africa.pause_trivia(update,context)
        elif text == "A" and condition == True:
            message_id = update.callback_query.message.message_id
            
            question, answer, message_id, pickone, picktwo, pickthree, pickfour, group_id = Afrique.get_allQuestion(msg_id=message_id,
                group_id=chat_id)

            if Africhance.get_user_chance(user_id=user_id,group_id=chat_id)==False:
                Africhance(user_id=user_id,group_id=group_id).save()
                
                if pickone == answer:
                    context.bot.edit_message_text(emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          parse_mode=ParseMode.MARKDOWN)
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text=emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),show_alert=True)
                    # sql.add_tlgrm_user(tlgrm_id=user_id, username=user.username)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)
                    # points = sql.get_points(tlgrm_id=user.id)
                    correct += 1
                    Answers.update_correct(correct=correct, answertype="africa", user_id=user.id, group_id=group_id)
                    africa.trivia_game(update,context)
                    Africhance.drop_collection()
                else:
                    # user failed
                    # CHANCE[user.id] = 1
                    Africhance.update_user_chance(user_id=user_id,chances=1)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)

                    incorrect += 1

                    Answers.update_incorrect(incorrect=incorrect,answertype='africa',user_id=user_id,group_id=group_id)
                    context.bot.send_message(chat_id, emoji.emojize(
                        f":turtle: Sorry {user.username}, but your answer is wrong. Better next time",
                        use_aliases=True))

            else:
                context.bot.answer_callback_query(update.callback_query.id,
                                                  text=texts.NOCHANCE, parse_mode=ParseMode.MARKDOWN)
                

        elif text == "B" and condition == True:
            message_id = update.callback_query.message.message_id
            
            question, answer, message_id, pickone, picktwo, pickthree, pickfour, group_id = Afrique.get_allQuestion(
                msg_id=message_id,
                group_id=chat_id)
            if Africhance.get_user_chance(user_id=user_id, group_id=chat_id) ==False:
                Africhance(user_id=user_id, group_id=group_id).save()
               
                if picktwo == answer:
                    context.bot.edit_message_text(emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),
                        chat_id=update.callback_query.message.chat_id,
                        message_id=update.callback_query.message.message_id,
                        parse_mode=ParseMode.MARKDOWN)
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text=emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),show_alert=True)
                    # sql.add_tlgrm_user(tlgrm_id=user_id, username=user.username)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)
                    # points = sql.get_points(tlgrm_id=user.id)
                    correct += 1
                    Answers.update_correct(correct=correct, answertype="africa", user_id=user.id, group_id=group_id)
                    africa.trivia_game(update, context)
                    Africhance.drop_collection()
                else:
                    # user failed
                    # CHANCE[user.id] = 1
                    Africhance.update_user_chance(user_id=user_id, chances=1)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)

                    incorrect += 1

                    Answers.update_incorrect(incorrect=incorrect, answertype='africa', user_id=user_id,
                                             group_id=group_id)
                    context.bot.send_message(chat_id, emoji.emojize(
                        f":turtle: Sorry {user.username}, but your answer is wrong. Better next time",
                        use_aliases=True))

            else:
                context.bot.answer_callback_query(update.callback_query.id,
                                                  text=texts.NOCHANCE, parse_mode=ParseMode.MARKDOWN)

        elif text == "C" and condition == True:
            message_id = update.callback_query.message.message_id
            
            question, answer, message_id, pickone, picktwo, pickthree, pickfour, group_id = Afrique.get_allQuestion(
                msg_id=message_id,
                group_id=chat_id)
            if Africhance.get_user_chance(user_id=user_id, group_id=chat_id) ==False:
                Africhance(user_id=user_id, group_id=group_id).save()
                
                if pickthree == answer:
                    context.bot.edit_message_text(emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),
                        chat_id=update.callback_query.message.chat_id,
                        message_id=update.callback_query.message.message_id,
                        parse_mode=ParseMode.MARKDOWN)
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text=emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),show_alert=True)
                    # sql.add_tlgrm_user(tlgrm_id=user_id, username=user.username)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)
                    # points = sql.get_points(tlgrm_id=user.id)
                    correct += 1
                    Answers.update_correct(correct=correct, answertype="africa", user_id=user.id, group_id=group_id)
                    africa.trivia_game(update, context)
                    Africhance.drop_collection()
                else:
                    # user failed
                    # CHANCE[user.id] = 1
                    Africhance.update_user_chance(user_id=user_id, chances=1)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)

                    incorrect += 1

                    Answers.update_incorrect(incorrect=incorrect, answertype='africa', user_id=user_id,
                                             group_id=group_id)
                    context.bot.send_message(chat_id, emoji.emojize(
                        f":turtle: Sorry {user.username}, but your answer is wrong. Better next time",
                        use_aliases=True))

            else:
                context.bot.answer_callback_query(update.callback_query.id,
                                                  text=texts.NOCHANCE, parse_mode=ParseMode.MARKDOWN)

        elif text == "D" and condition == True:
            message_id = update.callback_query.message.message_id
            
            question, answer, message_id, pickone, picktwo, pickthree, pickfour, group_id = Afrique.get_allQuestion(
                msg_id=message_id,
                group_id=chat_id)
            if Africhance.get_user_chance(user_id=user_id, group_id=chat_id) ==False:
                Africhance(user_id=user_id, group_id=group_id).save()
                
                if pickfour == answer:
                    context.bot.edit_message_text(emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),
                        chat_id=update.callback_query.message.chat_id,
                        message_id=update.callback_query.message.message_id,
                        parse_mode=ParseMode.MARKDOWN)
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text=emoji.emojize(
                        f":trophy: Congratulations {user.username}, your answer is correct!!! You got 1 point.\nThe correct answer was {answer}",
                        use_aliases=True),show_alert=True)
                    # sql.add_tlgrm_user(tlgrm_id=user_id, username=user.username)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)
                    # points = sql.get_points(tlgrm_id=user.id)
                    correct += 1
                    Answers.update_correct(correct=correct, answertype="africa", user_id=user.id, group_id=group_id)
                    africa.trivia_game(update, context)
                    Africhance.drop_collection()
                else:
                    # user failed
                    # CHANCE[user.id] = 1
                    Africhance.update_user_chance(user_id=user_id, chances=1)
                    answ = Answers.check_user_answer(user_id=user.id, group_id=group_id, answertype="africa")
                    
                    if answ == False:
                        Answers(user_id=user.id, username=user.username, correct=0, incorrect=0, answertype="africa",
                                group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="africa",
                                                                       group_id=group_id)

                    incorrect += 1

                    Answers.update_incorrect(incorrect=incorrect, answertype='africa', user_id=user_id,
                                             group_id=group_id)
                    context.bot.send_message(chat_id, emoji.emojize(
                        f":turtle: Sorry {user.username}, but your answer is wrong. Better next time",
                        use_aliases=True))

            else:
                context.bot.answer_callback_query(update.callback_query.id,
                                                  text=texts.NOCHANCE, parse_mode=ParseMode.MARKDOWN)

        elif text.startswith('like'):
            user_id = text.split('+')[1]
            rank = text.split('+')[2]
            username =text.split('+')[3]

            if Ranking.check_ranking_status(user_id=user.id):
                if Likers.check_liker(user_id=user.id, group_id=chat_id, rank=rank, liked=user_id):
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text="You already liked this achievement")
                else:
                    Likers(user_id=user.id, group_id=chat_id, rank=rank, liked=user_id).save()
                    likes = Likes.get_likes_count(user_id=user_id, group_id=chat_id, rank=rank)
                    likes += 1
                    Likes.update_likes(user_id=user_id, likes=likes, group_id=chat_id, rank=rank)
                    key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{user_id}+{rank}+{username}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.edit_message_text(text=texts.ADVANCE.format(username, rank),
                                                  chat_id=update.callback_query.message.chat_id,
                                                  message_id=update.callback_query.message.message_id,
                                                  reply_markup=main_markup)

            else:
                context.bot.answer_callback_query(update.callback_query.id,
                                                  text="Please register to be able to like achievements! ")

        elif text.startswith('stats'):
            score ="\n".join(util.top_scoreboard(group_id=chat_id))
            context.bot.edit_message_text(text=emoji.emojize(f":smiley: *TOP 10 SCOREBOARD* :trophy:\n\n{score}", use_aliases=True),
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,parse_mode="Markdown")






        elif text.startswith('join'):
            print(chat_id)
            game_no =query.message.message_id
            game_stat = Games.get_game_status(game_no=game_no)
            t_joined = Games.get_game_joined(game_no=game_no)
            check_player = Players.check_player(user_id=user.id, game_no=game_no)
            game_avail = Games.get_game_no(game_no=game_no)
            game_admin = Games.get_game_admin(game_no=game_no)
            if game_avail != False:

                # check game status is on or won
                # game_stat
                if game_stat == 0:
                    print(game_stat)

                    # check if the user has been wrong more than twice
                    if Sherlockchance.get_user_chance(user_id=user.id,group_id=chat_id)!=False:
                        Sherlockchance(user_id=user_id, group_id=chat_id).save()
                        print("user in chance")
                        chances = Sherlockchance.get_user_chance(user_id=user.id,group_id=chat_id)
                        print(chances)
                        if int(chances) >= 2:
                            print("user chances >2")

                            context.bot.answer_callback_query(update.callback_query.id,
                                                              text=texts.NOCHANCE,
                                                              show_alert=True)
                    else:
                        # # check if user already joined the game
                        if check_player != True:
                            print("player not in the game")
                            # check if the number of users are enough to start the game
                            if int(t_joined) < config.HUNTERS:
                                print("those joined are less")
                                # sql.add_player(game_no=game_no,user_id=user.id)
                                Players(game_no=game_no, user_id=user.id).save()
                                # count =sql.get_count(game_no)
                                count = Players.get_count(game_no=game_no)
                                # sql.update_joined(joined=count,game_no=game_no)
                                Games.update_joined(joined=count, game_no=game_no)
                                # c_joined = sql.get_game_joined(game_no=game_no)
                                c_joined = Games.get_game_joined(game_no=game_no)
                                # update.message.reply_text(texts.JOINED.format(user.first_name),
                                #                           parse_mode=ParseMode.MARKDOWN)
                                context.bot.answer_callback_query(update.callback_query.id,
                                                                  text=texts.JOINED.format(user.first_name),show_alert=True )
                                togo = config.HUNTERS - int(c_joined)
                                print(togo)
                                if togo == 0:
                                    context.bot.send_message(chat_id, texts.HUNTON, parse_mode=ParseMode.MARKDOWN)

                                    # notify admin
                                    context.bot.send_message(chat_id=game_admin,
                                                             text="Enough users have joined the game, start sending hints")
                                else:
                                    context.bot.send_message(chat_id, "{} user(s) to go".format(togo))
                            elif t_joined >= config.HUNTERS and t_joined <= config.MAX:
                                # sql.add_player(game_no=game_no, user_id=user.id)
                                Players(game_no=game_no, user_id=user.id).save()
                                count = Players.get_count(game_no=game_no)
                                Games.update_joined(joined=count, game_no=game_no)
                                c_joined = Games.get_game_joined(game_no=game_no)
                                cogo = config.MAX - int(c_joined)
                                context.bot.answer_callback_query(update.callback_query.id,
                                                                  text=texts.JOINED.format(user.first_name),
                                                                  show_alert=True)
                                if cogo == 0:
                                    # context.bot.send_message(chat_id, "Maximum number of hunters achieved! ")
                                    context.bot.edit_message_text(text="Maximum number of hunters achieved! ",
                                                                  chat_id=update.callback_query.message.chat_id,
                                                                  message_id=update.callback_query.message.message_id,
                                                                  parse_mode=ParseMode.MARKDOWN)
                                else:
                                    context.bot.send_message(chat_id,f"{cogo} user(s) to reach the maximum number of hunters allowed")


                            elif t_joined >= config.MAX:
                                context.bot.answer_callback_query(update.callback_query.id,
                                                                  text=f"Hi {user.first_name}, enough hunters have joined this hunt! Wait for the next hunt!",show_alert=True )

                        else:

                            context.bot.answer_callback_query(update.callback_query.id,
                                                              text=f"Hi {user.first_name}, you already joined this hunt.!",show_alert=True )

                else:
                    context.bot.answer_callback_query(update.callback_query.id,
                                                      text=f"Hi {user.first_name}, this hunt is over, please wait for the next one!",show_alert=True )

