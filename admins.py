from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

import util
import db
import ra
from sql import *


sqls= db.DBHelper()

@util.send_typing_action
def manage_admin(update,context):

    # admins = sqls.get_all_admins()
    admins = Users.get_all_admins
    user = update.message.from_user
    chat_type = update.message.chat.type
    # admin = sqls.check_admin(user.id)
    admin = Users.check_admin(user_id=user.id)
    print(admin)
    if chat_type == "private":
        if admin == 2:
            if len(admins) > 0:
                update.message.reply_text("Hi Super admin click on the admin you want to delete")
                for data in admins:

                    key_main = [[InlineKeyboardButton("{}".format(data.user_id), callback_data='usr+{}'.format(data.user_id))]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=user.id,
                                     text='<--------Click to delete-------->',
                                     reply_markup=main_markup)
            else:
                context.bot.send_message(chat_id=user.id, text='No Teachers available, to Add a teacher click the ADD ADMIN button')


@util.send_typing_action
def admin(update,context):
    chat_type = update.message.chat.type
    user = update.message.from_user
    # admins = sqls.check_admin(user.id)
    admins=Users.check_admin(user_id=user.id)
    if chat_type=="private":
        if admins == 2:
            update.message.reply_text(
                "Hi Super Admin, please send the user ID of the person you wish to add as an admin")
            return ra.ADMIN
        else:
            update.message.reply_text("You are not cleared to run this command")
            return ConversationHandler.END




@util.send_typing_action
def save_admin(update,context):
    admin_user = update.message.text
    if util.validate(admin_user):
        # sqls.set_user(user_id=admin_user, username=None, role=1)
        Users(user_id=int(admin_user),username="None",role=1).save()
        # sqls.set_role(int(1),int(admin_user))
        Users.set_role(role=1,user_id=int(admin_user))
        update.message.reply_text("The user was added successfully as an admin\nSelect the REMOVE ADMIN menu to view and delete teachers")
        return ConversationHandler.END
    elif admin_user=="CANCEL":
        update.message.reply_text("Your cancelled our conversation!.")
        return ConversationHandler.END
    else:
        update.message.reply_text("Invalid data entered")
        return ra.ADMIN





@util.send_typing_action
def profile(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    if chat_type =="private":
        update.message.reply_text("First Name: {}\nUsername: {}\nUser ID: {}".format(user.first_name,user.username,user.id))


