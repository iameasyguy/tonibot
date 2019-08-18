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
                              f"Press /progress inside the group to view your actual rank and requirements for next rank",parse_mode="Markdown")


@util.send_typing_action
def progress(update,context):
    username = util.get_username(update, context)
    user = update.message.from_user
    chat_type = update.message.chat.type
    followermsg = config.ACHIEVE['follower']['messages']
    followerpts = config.ACHIEVE['follower']['points']
    apprenticemsg = config.ACHIEVE['apprentice']['messages']
    apprenticepts = config.ACHIEVE['apprentice']['points']
    instructormsg = config.ACHIEVE['instructor']['messages']
    instructorpts = config.ACHIEVE['instructor']['points']
    mastermsg = config.ACHIEVE['master']['messages']
    masterpts = config.ACHIEVE['master']['points']
    titanmsg = config.ACHIEVE['titan']['messages']
    titanpts = config.ACHIEVE['titan']['points']
    if chat_type == "private":

        if Ranking.check_ranking_status(user_id=user.id):
            update.message.reply_text(f"Hi {username}, please send this command inside an LC group")
        else:
            update.message.reply_text(f"Hi {username}, please send /join to register for the points program")
    else:
        if Ranking.check_ranking_status(user_id=user.id):
            group_id = update.message.chat.id
            group_title = update.message.chat.title
            apolo = Answers.get_all_apolo_by_group(user_id=user.id,group_id=group_id)
            africa = Answers.get_all_africa_by_group(user_id=user.id,group_id=group_id)
            gaia = Answers.get_all_gaia_by_group(user_id=user.id,group_id=group_id)
            sheshat = Answers.get_all_seshat_by_group(user_id=user.id,group_id=group_id)
            sherlock =Answers.get_all_sherlock_by_group(user_id=user.id,group_id=group_id)
            zamol = Answers.get_all_zamol_by_group(user_id=user.id,group_id=group_id)
            totalpts = Answers.get_all_points_by_group(user_id=user.id,group_id=group_id)
            user_messages = Messages.get_messages_count(user_id=user.id, group_id=group_id)
            update.message.reply_text("Psss! check your pm")

            if (user_messages >= followermsg and user_messages < apprenticemsg) and (totalpts >= followerpts and totalpts < apprenticepts):
                position = util.get_user_position(user_id=user.id,username=username,group_id=group_id)


                rank = config.RANKS[1]
                message = f"Hi {username},Below are your standings in the *{group_title} Group*\n" \
                    f"*Rank*: {rank}\n*Current position: {position}*\n*↓Vocabulary ~ Africa:* {africa}\n*↓ Syntax ~ Apollo:* {apolo}\n*↓ Pronunciation ~ Gaia:* {gaia}\n*↓ Grammar ~ Seshat:* {sheshat}\n" \
                    f"*↓ Focus ~ Sherlock:* {sherlock}\n*↓ Spelling ~ Zalmoxis:* {zamol}\n\n*Total: {totalpts}*\n" \
                    f"*Messages Sent: {user_messages}*"

                context.bot.send_message(chat_id=user.id,text=message,parse_mode="Markdown")
            elif (user_messages >=apprenticemsg and user_messages < instructormsg ) and (totalpts>=apprenticepts and totalpts < instructorpts):
                print("cretia passed")
                rank = config.RANKS[2]
                position = util.get_user_position(user_id=user.id, username=username, group_id=group_id)
                message = f"Hi {username},Below are your standings in the *{group_title} Group*\n" \
                    f"*Rank*: {rank}\n*Current position: {position}*\n*↓Vocabulary ~ Africa:* {africa}\n*↓ Syntax ~ Apollo:* {apolo}\n*↓ Pronunciation ~ Gaia:* {gaia}\n*↓ Grammar ~ Seshat:* {sheshat}\n" \
                    f"*↓ Focus ~ Sherlock:* {sherlock}\n*↓ Spelling ~ Zalmoxis:* {zamol}\n\n*Total: {totalpts}*\n" \
                    f"*Messages Sent: {user_messages}*"

                context.bot.send_message(chat_id=user.id, text=message, parse_mode="Markdown")
            elif (user_messages >=instructormsg and user_messages < mastermsg ) and (totalpts>=instructorpts and totalpts < masterpts):
                print("cretia passed")
                position = util.get_user_position(user_id=user.id, username=username, group_id=group_id)
                rank = config.RANKS[3]
                message = f"Hi {username},Below are your standings in the *{group_title} Group*\n" \
                    f"*Rank*: {rank}\n*Current position: {position}*\n*↓Vocabulary ~ Africa:* {africa}\n*↓ Syntax ~ Apollo:* {apolo}\n*↓ Pronunciation ~ Gaia:* {gaia}\n*↓ Grammar ~ Seshat:* {sheshat}\n" \
                    f"*↓ Focus ~ Sherlock:* {sherlock}\n*↓ Spelling ~ Zalmoxis:* {zamol}\n\n*Total: {totalpts}*\n" \
                    f"*Messages Sent: {user_messages}*"

                context.bot.send_message(chat_id=user.id, text=message, parse_mode="Markdown")
            elif (user_messages >=mastermsg and user_messages < titanmsg ) and (totalpts>=masterpts and totalpts < titanpts):
                print("cretia passed")
                position = util.get_user_position(user_id=user.id, username=username, group_id=group_id)
                rank = config.RANKS[4]
                message = f"Hi {username},Below are your standings in the *{group_title} Group*\n" \
                    f"*Rank*: {rank}\n*Current position: {position}*\n*↓Vocabulary ~ Africa:* {africa}\n*↓ Syntax ~ Apollo:* {apolo}\n*↓ Pronunciation ~ Gaia:* {gaia}\n*↓ Grammar ~ Seshat:* {sheshat}\n" \
                    f"*↓ Focus ~ Sherlock:* {sherlock}\n*↓ Spelling ~ Zalmoxis:* {zamol}\n\n*Total: {totalpts}*\n" \
                    f"*Messages Sent: {user_messages}*"

                context.bot.send_message(chat_id=user.id, text=message, parse_mode="Markdown")
            elif (user_messages >= titanmsg and totalpts >= titanpts):
                rank = config.RANKS[5]
                position = util.get_user_position(user_id=user.id, username=username, group_id=group_id)
                message = f"Hi {username},Below are your standings in the *{group_title} Group*\n" \
                    f"*Rank*: {rank}\n*Current position: {position}*\n*↓Vocabulary ~ Africa:* {africa}\n*↓ Syntax ~ Apollo:* {apolo}\n*↓ Pronunciation ~ Gaia:* {gaia}\n*↓ Grammar ~ Seshat:* {sheshat}\n" \
                    f"*↓ Focus ~ Sherlock:* {sherlock}\n*↓ Spelling ~ Zalmoxis:* {zamol}\n\n*Total: {totalpts}*\n" \
                    f"*Messages Sent: {user_messages}*"

                context.bot.send_message(chat_id=user.id, text=message, parse_mode="Markdown")
            else:
                rank = config.RANKS[1]
                position = util.get_user_position(user_id=user.id, username=username, group_id=group_id)
                message = f"Hi {username},Below are your standings in the *{group_title} Group*\n" \
                    f"*Rank*: {rank}\n*Current position: {position}*\n*↓Vocabulary ~ Africa:* {africa}\n*↓ Syntax ~ Apollo:* {apolo}\n*↓ Pronunciation ~ Gaia:* {gaia}\n*↓ Grammar ~ Seshat:* {sheshat}\n" \
                    f"*↓ Focus ~ Sherlock:* {sherlock}\n*↓ Spelling ~ Zalmoxis:* {zamol}\n\n*Total: {totalpts}*\n" \
                    f"*Messages Sent: {user_messages}*"

                context.bot.send_message(chat_id=user.id, text=message, parse_mode="Markdown")


        else:
            update.message.reply_text(f"Hi {username}, please open @{context.bot.username} send /join to register for the points program")