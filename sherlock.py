from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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