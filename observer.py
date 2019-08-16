from pyrogram import Client
from telegram import ParseMode
import util
from sql import *
import config
speech = util.Speech()



@util.send_typing_action
def observer(update,context):
    bot_username = update.message.reply_to_message.from_user.username
    chat_type = update.message.chat.type
    user = update.message.from_user
    user_answer =update.message.text
    group_id = update.message.chat.id

    chat_type = update.message.chat.type
    criminal_id = update.message.reply_to_message.from_user.id

    tickers = ['you are the criminal!','you are the criminal !','You are the criminal!','you are the criminal !','you are the criminal','You are the criminal']

    if user_answer in tickers:
        last_game_id = Games.get_last_game_id(group_id=group_id)
        game_no = Games.get_game_no_from_id(tid=last_game_id)
        game_stat = Games.get_game_status(game_no=game_no)
        if Users.check_user(user_id=user.id) == False:
            Users(user_id=user.id, username=user.username, role=0).save()

        if criminal_id == config.CRIME and (chat_type == "group" or chat_type == "supergroup"):

            if game_stat == 0:
                if Sherlockchance.get_user_chance(user_id=user.id,group_id=group_id)!="False":
                    chances = Sherlockchance.get_user_chance(user_id=user.id,group_id=group_id)
                    if int(chances) >= 2:
                        update.message.reply_text(config.NOCHANCE, parse_mode=ParseMode.MARKDOWN)
                    else:
                        answ = Answers.check_user_answer(user_id=user.id,group_id=group_id, answertype="sherlock")
                        
                        if answ == False:
                            Answers(user_id=user.id,username=user.username, correct=0, incorrect=0, answertype="sherlock",group_id=group_id).save()
                        app = Client("my_account", api_id=config.api_id, api_hash=config.api_hash)
                        with app as app:
                            app.send_message(chat_id=group_id, text=config.FOUND, parse_mode="markdown")

                        Games.update_game_status(status=1, game_no=game_no)
                        correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="sherlock",group_id=group_id)
                        correct += 10
                        Answers.update_correct(correct=correct, answertype="sherlock", user_id=user.id,group_id=group_id)
                        update.message.reply_text(config.CONGRATS.format(user.first_name))
                else:
                    answ = Answers.check_user_answer(user_id=user.id,group_id=group_id, answertype="sherlock")
                    
                    if answ == False:
                        Answers(user_id=user.id,username=user.username, correct=0, incorrect=0, answertype="sherlock",group_id=group_id).save()
                    app = Client("my_account", api_id=config.api_id, api_hash=config.api_hash)
                    with app as app:
                        app.send_message(chat_id=group_id, text=config.FOUND, parse_mode="markdown")
                        # update game status
                    Games.update_game_status(status=1, game_no=game_no)
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="sherlock",group_id=group_id)
                    correct += 10
                    Answers.update_correct(correct=correct, answertype="sherlock", user_id=user.id,group_id=group_id)
                    update.message.reply_text(config.CONGRATS.format(user.first_name),
                                              parse_mode=ParseMode.MARKDOWN)
            else:
                update.message.reply_text("*Opps too late for that!, the hunt is over, wait for the next one*",
                                          parse_mode=ParseMode.MARKDOWN)

        elif criminal_id != config.CRIME and (chat_type == "group" or chat_type == "supergroup"):
            answ = Answers.check_user_answer(user_id=user.id, group_id=group_id,answertype="sherlock")
            
            if answ == False:
                Answers(user_id=user.id,username=user.username, correct=0, incorrect=0, answertype="sherlock",group_id=group_id).save()
            if game_stat == 0:
                if Sherlockchance.get_user_chance(user_id=user.id,group_id=group_id)!="False":
                    chances = Sherlockchance.get_user_chance(user_id=user.id,group_id=group_id)
                    if int(chances) >= 2:
                        update.message.reply_text(config.NOCHANCE, parse_mode=ParseMode.MARKDOWN)

                    elif int(chances) == 1:

                        Sherlockchance.update_user_chance(user_id=user.id,chances=2)
                        correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="sherlock",group_id=group_id)
                        incorrect += 1
                        Answers.update_incorrect(incorrect=incorrect, answertype="sherlock", user_id=user.id,group_id=group_id)
                        update.message.reply_text(
                            "⛔ *Please don't accuse people without clear evidence! You have exhausted your chances, wait for the next hunt!*",
                            parse_mode=ParseMode.MARKDOWN)
                else:

                    Sherlockchance.update_user_chance(user_id=user.id, chances=1)
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype="sherlock",group_id=group_id)
                    incorrect += 1
                    Answers.update_incorrect(incorrect=incorrect, answertype="sherlock", user_id=user.id,group_id=group_id)
                    update.message.reply_text(
                        "⛔*Please don't accuse people without clear evidence! You have one last chance.*",
                        parse_mode=ParseMode.MARKDOWN)
            else:
                update.message.reply_text("*Opps too late for that!, the hunt is over, wait for the next one*",
                                          parse_mode=ParseMode.MARKDOWN)



    else:
        # pass

        if bot_username == config.BOT_USERNAME and (chat_type == "group" or chat_type == "supergroup"):

            if Users.check_user(user_id=user.id) == False:
                Users(user_id=user.id, username=user.username, role=0).save()
            message_id = update.message.reply_to_message.message_id
            qstn_type = util.question_type(message_id=message_id)
            if qstn_type == 'apolo':
                answ = Answers.check_user_answer(user_id=user.id,group_id=group_id,answertype=qstn_type)
                
                if answ == False:
                    Answers(user_id=user.id,username=user.username, correct=0, incorrect=0, answertype=qstn_type,group_id=group_id).save()


                answer = Apolo.get_apolo_answer_by_msg_id(msg_id=message_id)
                correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype=qstn_type,group_id=group_id)
                if user_answer.lower() == answer.lower():
                    status = Apolo.get_apolo_qstn_status(msg_id=message_id)
                    if status == 0:
                        Apolo.change_apolo_qstn_status(status=1, msg_id=message_id)
                        correct += 1
                        Answers.update_correct(correct=correct, answertype=qstn_type, user_id=user.id,group_id=group_id)
                        update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                    else:
                        update.message.reply_text(
                            "🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
                else:

                    incorrect += 1
                    Answers.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id,group_id=group_id)
                    update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
            elif qstn_type == 'seshat':
                answ = Answers.check_user_answer(user_id=user.id,group_id=group_id, answertype=qstn_type)

                if answ == False:
                    Answers(user_id=user.id,username=user.username, correct=0, incorrect=0, answertype=qstn_type,group_id=group_id).save()
                answer = Seshat.get_seshat_answer_by_msg_id(msg_id=message_id)
                correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype=qstn_type,group_id=group_id)
                if user_answer.lower() == answer.lower():
                    status = Seshat.get_seshat_qstn_status(msg_id=message_id)
                    if status == 0:

                        Seshat.change_seshat_qstn_status(status=1, msg_id=message_id)

                        correct += 1

                        Answers.update_correct(correct=correct, answertype=qstn_type, user_id=user.id,group_id=group_id)
                        update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                    else:
                        update.message.reply_text(
                            "🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
                else:
                    incorrect += 1
                    Answers.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id,group_id=group_id)
                    update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
            elif qstn_type == 'zamol':
                group_id = update.message.chat.id
                answ = Answers.check_user_answer(user_id=user.id,group_id=group_id, answertype=qstn_type)
                if answ == False:
                    Answers(user_id=user.id,username=user.username, correct=0, incorrect=0, answertype=qstn_type,group_id=group_id).save()
                correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype=qstn_type,group_id=group_id)
                data = Zamol.get_zamol_qstnsby_msgid(msg_id=message_id, group_id=group_id)

                if user_answer.lower() == data.question.lower():
                    status = Zamol.get_zamol_qstn_status(msg_id=message_id)
                    if status == 0:
                        Zamol.change_zamol_qstn_status(status=1, msg_id=message_id)

                        correct += 1
                        Answers.update_correct(correct=correct, answertype=qstn_type, user_id=user.id,group_id=group_id)
                        update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                    else:

                        update.message.reply_text(
                            "🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")
                else:

                    incorrect += 1
                    Answers.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id,group_id=group_id)
                    update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")

            elif qstn_type == 'gaia':
                try:
                    group_id = update.message.chat.id
                    answ = Answers.check_user_answer(user_id=user.id,group_id=group_id, answertype=qstn_type)

                    if answ == False:
                        Answers(user_id=user.id,username=user.username, correct=0, incorrect=0, answertype=qstn_type,group_id=group_id).save()
                    correct, incorrect = Answers.get_correct_incorrect(user_id=user.id, answertype=qstn_type,group_id=group_id)
                    file_id = update.message.voice.file_id
                    newFile = context.bot.get_file(file_id)
                    newFile.download('answ_{}.ogg'.format(user.id))
                    length = update.message.voice.duration
                    if length < 10:
                        new = util.convert_ogg_to_wav("answ_{}.ogg".format(user.id), "stud_{}.wav".format(user.id))
                        speech.file = new
                        lang, quiz = Gaia.get_gaia_qstnsby_msgid(msg_id=message_id, group_id=group_id)
                        langue = util.language_select(language=lang)
                        text = speech.to_text(lang=langue)
                        if text == 401:
                            update.message.reply_text(
                                "Hi {}, I did not understand this, please try again".format(user.first_name))
                        elif text == 500:
                            update.message.reply_text(
                                "Sorry {}, I got a little light headed, please try again".format(user.first_name))
                        elif text.lower() == quiz.lower():
                            status = Gaia.get_gaia_qstn_status(msg_id=message_id)

                            if status == 0:
                                Gaia.change_gaia_qstn_status(status=1, msg_id=message_id)

                                correct += 1
                                Answers.update_correct(correct=correct, answertype=qstn_type, user_id=user.id,group_id=group_id)
                                update.message.reply_text("🏆Your answer is correct!!! You earn 1 point.")
                            else:

                                update.message.reply_text(
                                    "🐢Your answer is correct! But unfortunately someone has already answered this question correctly; stay tuned for the next question.")

                        elif text.lower() != quiz.lower():

                            incorrect += 1
                            Answers.update_incorrect(incorrect=incorrect, answertype=qstn_type, user_id=user.id,group_id=group_id)

                            update.message.reply_text("🐔Sorry, your answer is wrong. Please try again!")
                        util.clear_student(user_id=user.id)
                except AttributeError:
                    update.message.reply_text(f"Hi {user.first_name}, wrong message or in the wrong format")

            else:
                update.message.reply_text(f"Hi {user.first_name}, you are replying to the wrong message or in the wrong format")