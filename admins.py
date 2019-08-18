from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
import emoji
import util
import db
import ra
from sql import *
import config

sqls= db.DBHelper()

@util.send_typing_action
def manage_admin(update,context):

    # admins = sqls.get_all_admins()
    admins = Users.get_all_admins
    user = update.message.from_user
    chat_type = update.message.chat.type
    # admin = sqls.check_admin(user.id)
    admin = Users.check_admin(user_id=user.id)
    if chat_type == "private":
        if admin == 2:
            if admins[0].username != 'None':
                update.message.reply_text("Hi Super admin click on the admin you want to delete")
                for data in admins:

                    key_main = [[InlineKeyboardButton("Delete", callback_data='usr+{}'.format(data.user_id))]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    context.bot.send_message(chat_id=user.id,
                                     text=f'Username: {data.username}\nUser ID: {data.user_id}',
                                     reply_markup=main_markup)
            else:
                context.bot.send_message(chat_id=user.id, text='No Teachers available, to Add a teacher click the ADD ADMIN button')


@util.send_typing_action
def admin(update,context):
    chat_type = update.message.chat.type
    user = update.message.from_user
    admins=Users.check_admin(user_id=user.id)
    if chat_type=="private":
        if admins == 2:
            update.message.reply_text(f"Hi Super Admin, ask the user you want to add as a teacher to open @{context.bot.username} and send /admin\n"
                f"you will receive a request to approve or decline")

        else:
            update.message.reply_text("You are not cleared to run this command")
            return ConversationHandler.END









@util.send_typing_action
def profile(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    if chat_type =="private":
        update.message.reply_text("First Name: {}\nUsername: {}\nUser ID: {}".format(user.first_name,util.get_username(update,context),user.id))


@util.send_typing_action
def request_add(update,context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    if chat_type == "private":
        update.message.reply_text(f"Hi {user.first_name} you request was sent to the admin for approval")
        key_main = [[InlineKeyboardButton("Approve", callback_data=f'approve+{user.id}+{util.get_username(update,context)}')],
                    [InlineKeyboardButton("Decline", callback_data=f'deny+{user.id}')]]
        main_markup = InlineKeyboardMarkup(key_main)
        context.bot.send_message(chat_id=865996339,text=f"The following user has requested to be a teacher\n*Name:* _{user.first_name}_\n*Username:* _{util.get_username(update,context)}_",reply_markup=main_markup,parse_mode="Markdown")

