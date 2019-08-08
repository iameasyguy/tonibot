#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from sql import *
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db
import util
import ra

# sqls = db.DBHelper()

@util.send_typing_action
def save_apolo_question(update,context):
    add_det = Groups.objects
    chat_type = update.message.chat.type
    user = update.message.from_user
    answer = update.message.text
    qstn = util.randomize(answer)
    validate =Apolo.get_apolo_answer(user_id=user.id,answer=answer)

    # id, group_id, group_title
    if chat_type == "private":
        if validate!=True:
            if len(add_det)>0:
                Apolo(question=qstn, answer=answer, username=user.username,user_id=user.id).save()

                update.message.reply_text('Please select the group you want to post the Apolo trivia')
                for data in add_det:
                    key_main = [[InlineKeyboardButton(f"{data.group_language} Group", callback_data=f'apolq+{data.group_id}')]]
                    main_markup = InlineKeyboardMarkup(key_main)
                    update.message.reply_text('<-------👇---------->', reply_markup=main_markup)
                return ra.GROUP
            else:
                update.message.reply_text('No Groups Available please add the bot to a group and make it admin')
                return ConversationHandler.END
        else:
            update.message.reply_text('This question already exists!!! Share another one')
            return ra.APOLO