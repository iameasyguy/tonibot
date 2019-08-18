from pyrogram import Client
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

import util
import ra
import config
from sql import *
def confirm(update, context):
    user = update.message.from_user
    # tbl_id = sql.get_last_id(user_id=user.id)
    tbl_id =Sherlock.get_last_sherlock_id(user_id=user.id)
    plot = update.message.text
    # fileid = sql.get_qstn_file_id(tbl_id=tbl_id,user_id=user.id)
    fileid = Sherlock.get_sherlock_qstn_file_id(tbl_id=tbl_id,user_id=user.id)
    if fileid=="0":
        # sql.change_fileid_qstn(file_id=0, question=plot, tbl_id=tbl_id, user_id=user.id)
        Sherlock.change_sherlock_fileid(file_id="0", question=plot, tbl_id=tbl_id, user_id=user.id)
        key_main = [[InlineKeyboardButton("Confirm ✅️", callback_data='confirm')],
                    [InlineKeyboardButton("Cancel ❌", callback_data='cancel')]]
        main_markup = InlineKeyboardMarkup(key_main)
        update.message.reply_text('Please select Confirm to proceed or Cancel start again\n\n{}'.format(plot),
                                  reply_markup=main_markup)

    else:
        context.bot.send_photo(chat_id=user.id, photo=fileid)
        # sql.change_fileid_qstn(file_id=fileid, question=plot, tbl_id=tbl_id, user_id=user.id)
        Sherlock.change_sherlock_fileid(file_id=fileid, question=plot, tbl_id=tbl_id, user_id=user.id)
        key_main = [[InlineKeyboardButton("Confirm ✅️", callback_data='confirm')],
                    [InlineKeyboardButton("Cancel ❌", callback_data='cancel')]]
        main_markup = InlineKeyboardMarkup(key_main)
        update.message.reply_text('Please select Confirm to proceed or Cancel start again\n\n{}'.format(plot),
                                  reply_markup=main_markup)




@util.send_typing_action
def picture(update, context):
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    # tbl_id = sql.get_last_id(user_id=user.id)
    tbl_id = Sherlock.get_last_sherlock_id(user_id=user.id)
    if len(update.effective_message.photo) > 0:
        file_id = update.effective_message.photo[-1].file_id
        # sql.change_fileid_qstn(file_id=file_id,question="",tbl_id=tbl_id,user_id=user.id)
        Sherlock.change_sherlock_fileid(file_id=file_id,question="",tbl_id=tbl_id,user_id=user.id)
        # bot.send_photo(chat_id=chat_id, photo=file_id)
        update.message.reply_text("Please enter the rules and scenario(plot) you want to post")
        return ra.SHERLOCK


def poster(update, context):
    msg = update.message
    chat_id = msg.chat.id
    text = update.message.text

    config.LIST[chat_id]=text
    if text!="CANCEL":
        group = Groups.objects
        if len(group) > 0:

            for data in group:
                key_main = [[InlineKeyboardButton(f"{data.group_language} Group",
                                                  callback_data=f'phint {data.group_id}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                context.bot.send_message(
                    text="Please select the group you want to post the hint",
                    chat_id=chat_id,reply_markup=main_markup)
            # return ConversationHandler.END
        else:
            context.bot.send_message(
                text="No Groups Available please add the bot to a group and make it admin",
                chat_id=chat_id)

            return ConversationHandler.END
    else:
        return ra.cancel(update, context)



#########JARVIS################
@util.send_typing_action
def travis(update,context):
    bot_username = update.message.reply_to_message.from_user.username
    chat_type = update.message.chat.type
    user = update.message.from_user
    msg = update.message
    chat_id = msg.chat.id
    text = update.message.text
    game_no = update.message.reply_to_message.message_id
    # game_stat = sql.get_game_status(game_no)
    game_stat =Games.get_game_status(game_no=game_no)
    # t_joined = sql.get_game_joined(game_no=game_no)
    t_joined = Games.get_game_joined(game_no=game_no)
    print(type(t_joined))
    # check_player = sql.check_player(user_id=user.id, game_no=game_no)
    check_player = Players.check_player(user_id=user.id, game_no=game_no)
    # game_avail = sql.get_game_no(game_no)
    game_avail =Games.get_game_no(game_no=game_no)
    # game_admin = sql.get_game_admin(game_no=game_no)
    game_admin =Games.get_game_admin(game_no=game_no)
    print(game_no)
    print(text)
    #check game status
    #check if user already joined the game
    #check if the number of users are enough to start the game
    #check if the user used 'join'
    #check if game id is available in db
    if bot_username == config.BOT_USERNAME and (chat_type == "group" or chat_type == "supergroup"):
        # check if the user used 'join'
        if text=="/join":
            print("text = join")
            #check if game id is available in db
            if game_avail !=False:
                print("game_avail = true")
                # check game status is on or won
                # game_stat
                if game_stat ==0:
                    print("game_stat = 0")
                    #check if the user has been wrong more than twice
                    if user.id in config.CHANCE:
                        print("user in chance")
                        chances = config.CHANCE[user.id]
                        if int(chances)>=2:
                            print("user chances >2")
                            update.message.reply_text(config.NOCHANCE,parse_mode=ParseMode.MARKDOWN)
                    else:
                    # # check if user already joined the game
                        if check_player != True:
                            print("player not in the game")
                            # check if the number of users are enough to start the game
                            if int(t_joined)<config.HUNTERS:
                                print("those joined are less")
                                # sql.add_player(game_no=game_no,user_id=user.id)
                                Players(game_no=game_no,user_id=user.id).save()
                                # count =sql.get_count(game_no)
                                count = Players.get_count(game_no=game_no)
                                # sql.update_joined(joined=count,game_no=game_no)
                                Games.update_joined(joined=count,game_no=game_no)
                                # c_joined = sql.get_game_joined(game_no=game_no)
                                c_joined =Games.get_game_joined(game_no=game_no)
                                update.message.reply_text(config.JOINED.format(user.first_name),parse_mode=ParseMode.MARKDOWN)
                                togo = config.HUNTERS - int(c_joined)
                                print(togo)
                                if togo==0:
                                    context.bot.send_message(chat_id,config.HUNTON,parse_mode=ParseMode.MARKDOWN)
                                        #notify admin
                                    context.bot.send_message(chat_id=game_admin,text="Enough users have joined the game, start sending hints")
                                else:
                                    context.bot.send_message(chat_id, "{} user(s) to go".format(togo))
                            elif t_joined>=config.HUNTERS and t_joined<=config.MAX:
                                # sql.add_player(game_no=game_no, user_id=user.id)
                                Players(game_no=game_no, user_id=user.id).save()
                                count = Players.get_count(game_no=game_no)
                                Games.update_joined(joined=count,game_no=game_no)
                                c_joined =Games.get_game_joined(game_no=game_no)
                                cogo = config.MAX - int(c_joined)
                                update.message.reply_text(config.JOINED.format(user.first_name))
                                if cogo==0:
                                    context.bot.send_message(chat_id, "Maximum number of hunters achieved! ")
                                else:
                                    context.bot.send_message(chat_id, "{} user(s) to reach the maximum number of hunters allowed".format(cogo))


                            elif t_joined>=config.MAX:
                                update.message.reply_text("Hi {}, enough hunters have joined this hunt! Wait for the next hunt!".format(user.first_name))

                        else:
                                update.message.reply_text("Hi {}, you already joined this hunt.".format(user.first_name))

                else:
                    update.message.reply_text("Hi {}, this hunt is over, please wait for the next one".format(user.first_name))

            else:
                update.message.reply_text("Hi {} please reply with '/join' on the correct message".format(user.first_name))
        else:
            update.message.reply_text("Hi {} please use '/join' to join the hunt".format(user.first_name))


