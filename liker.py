from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from sql import *
import util
import config
def message_counter(update,context):
    group_id = update.message.chat.id
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    chat_type = update.message.chat.type
    username =util.get_username(update,context)
    if chat_type == "group" or chat_type == "supergroup":
        print(Messages.check_messages(user_id=user.id,group_id=group_id))
        if Messages.check_messages(user_id=user.id,group_id=group_id)==False:
            Messages(user_id=user.id,username=username,group_id=group_id).save()

        user_messages = Messages.get_messages_count(user_id=user.id,group_id=group_id)
        user_messages+=1
        Messages.update_messages(user_id=user.id,messages=user_messages,group_id=group_id)
        if user_messages==config.RANK1:
            key_main = [[InlineKeyboardButton('like', callback_data=f'like+{user.id}+{username}')]]
            main_markup = InlineKeyboardMarkup(key_main)
            context.bot.send_message(chat_id=group_id,text=f"{username} Just advanced  to the next level",reply_markup=main_markup)


