from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from pyrogram import Client
import config
import ra
from sql import *
def jarvis(update,context):
    query = update.callback_query
    text = str(query.data)
    user = query.from_user
    print(text)
    user_id = user.id
    if text.startswith('apolo'):
        context.bot.edit_message_text(
            text=f"Hi Admin {user.first_name}, please enter the phrase you want to post",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ra.APOLO
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
        return ra.SESHAT
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
        Zamol(user_id=user_id,group_id=group_id,lang=language,question_type='zamol').save()
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
                                 caption="🗣Please listen to Ro’s recording, then long-press, click reply and write what you heard!")
        message_id = payload.message_id
        print(message_id)
        Zamol.change_zamol_qstn_message_id(message_id=message_id,tbl_id=tbl_id,user_id=user_id)
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
                key_main = [[InlineKeyboardButton(f"{data.group_language} Group", callback_data=f'cgaia+{data.group_id}+{data.group_language}')]]
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
        Gaia(user_id=user_id,group_id=group_id,lang=language,question_type='gaia').save()
        context.bot.edit_message_text(
            text=f"Please record your message in {language}",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)
        return ra.GAIA
    elif text.startswith('yesg'):
        tbl_id = text.split('+')[1]
        # lang, qstn,file_id,g_id = sqls.get_gaia_question(tbl_id=tbl_id,user_id=user_id)
        lang, qstn,file_id,g_id = Gaia.get_gaia_question(tbl_id=tbl_id,user_id=user_id)
        payload = context.bot.send_voice(chat_id=g_id, voice=file_id,
                                 caption="🗣Please listen to Ro’s recording, then long-press, click reply and record what you heard!")
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
            message_id=update.callback_query.message.message_id,reply_markup=main_markup)
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
        Sherlock(user_id=user_id,question_type='sherlock').save()
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
        tbl_id =Sherlock.get_last_sherlock_id(user_id=user.id)
        # sql.change_qstn_group_id(group_id=g_id, tbl_id=tbl_id, user_id=user_id)
        Sherlock.change_sherlock_group_id(group_id=g_id,tbl_id=tbl_id,user_id=user_id)
        # sql.change_qstn_status(status=2, tbl_id=tbl_id, user_id=user_id)
        # msg = sql.get_question(tbl_id, user_id)
        msg =Sherlock.get_sherlock_question(tbl_id=tbl_id,user_id=user_id)
        swali,file_id = msg
        if file_id =="0":
            config.CHANCE.clear()
            payload = context.bot.send_message(chat_id=g_id, text="{}\n\n\n{}".format(swali, config.RULES),
                                       parse_mode=ParseMode.MARKDOWN)
            message_id = payload.message_id
            print(message_id)
            # sql.change_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
            Sherlock.change_sherlock_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
            # add game
            # sql.add_game(admin=user_id,game_no=message_id,group_id=g_id)#
            Games(admin_id=user_id,game_no=message_id,group_id=g_id).save()
            context.bot.edit_message_text(
                text="The Message was successfully posted in the group\nTo post another message click the POST key",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id)
            return ConversationHandler.END
        else:
            context.bot.send_photo(chat_id=g_id,photo=file_id)
            payload = context.bot.send_message(chat_id=g_id, text="{}\n\n\n{}".format(swali, config.RULES),parse_mode=ParseMode.MARKDOWN)
            message_id = payload.message_id
            print(message_id)
            # sql.change_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
            Sherlock.change_sherlock_qstn_message_id(message_id=message_id, tbl_id=tbl_id, user_id=user_id)
            Games(admin=user_id, game_no=message_id, group_id=g_id).save()
            # sql.add_game(admin=user_id, game_no=message_id,group_id=g_id)#
            config.CHANCE.clear()
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
        app = Client("my_account",api_id=config.api_id,api_hash=config.api_hash)
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
        admin =Users.check_admin(user_id=user_id)
        print(admin)
        if admin is not None:
            context.bot.edit_message_text(
                text=f"{user_name} is already an admin!",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id, )
            context.bot.send_message(chat_id=user_id,text=f"Hi {user_name} you are already an admin")

        else:
            Users(user_id=int(user_id), username=user_name, role=1).save()
            context.bot.edit_message_text(
                text=f"{user_name} was added as an admin!",
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,)
    elif text.startswith('deny'):
        user_id = text.split('+')[1]
        context.bot.edit_message_text(
            text="The request was declined!",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id, )
        context.bot.send_message(chat_id=user_id, text=f"Hi, your request was declined!")

    elif text.startswith('done'):
        context.bot.edit_message_text(
            text=f"Thanks {user.first_name},Open this [link](https://telegra.ph/User-Ranks-08-15) to see all ranks and conditions to progress or send /career",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,parse_mode="Markdown")

