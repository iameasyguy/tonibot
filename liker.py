from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from sql import *
import util
import config
import emoji
import texts
def message_counter(update,context):
    group_id = update.message.chat.id
    msg = update.message
    chat_id = msg.chat.id
    user = update.message.from_user
    userid =user.id
    chat_type = update.message.chat.type
    username =util.get_username(update,context)
    followermsg = config.ACHIEVE['follower']['messages']
    followerpts = config.ACHIEVE['follower']['points']
    apprenticemsg= config.ACHIEVE['apprentice']['messages']
    apprenticepts= config.ACHIEVE['apprentice']['points']
    instructormsg= config.ACHIEVE['instructor']['messages']
    instructorpts= config.ACHIEVE['instructor']['points']
    mastermsg= config.ACHIEVE['master']['messages']
    masterpts= config.ACHIEVE['master']['points']
    titanmsg= config.ACHIEVE['titan']['messages']
    titanpts= config.ACHIEVE['titan']['points']
    if chat_type == "group" or chat_type == "supergroup":
        # if they joined then start recording
        if Ranking.check_ranking_status(user_id=user.id):
            if Messages.check_messages(user_id=user.id, group_id=group_id) == False:
                Messages(user_id=user.id, username=username, group_id=group_id).save()

            user_messages = Messages.get_messages_count(user_id=user.id, group_id=group_id)
            user_messages += 1
            Messages.update_messages(user_id=user.id, messages=user_messages, group_id=group_id)
            totalpts = Answers.get_all_points_by_group(user_id=userid,group_id=group_id)
            print(totalpts)

            #Check if the user's message are goe to required follower messages but are less than apprentice and points vice versa
            if (user_messages >=followermsg and user_messages < apprenticemsg ) and (totalpts>=followerpts and totalpts < apprenticepts):
                print("cretia passed")
                rank = config.RANKS[1]
                if Likes.check_likes(user_id=userid,group_id=group_id,rank=rank)==False:
                    Likes(user_id=userid,username=username,rank=rank,group_id=group_id).save()
                likes = Likes.get_likes_count(user_id=user.id,group_id=group_id,rank=rank)
                key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                      callback_data=f'like+{userid}+{rank}+{username}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                if Likes.get_notify_status(user_id=userid,group_id=group_id,rank=rank)==0:
                    print("cretia reached sending msg")
                    context.bot.send_message(chat_id=group_id, text=texts.ADVANCE.format(username, rank),
                                             reply_markup=main_markup)
                    try:
                        context.bot.send_photo(chat_id=userid,photo=config.LOGOS['follower'])
                        context.bot.send_message(chat_id=userid,text=texts.ACHIEVEMENT.format(username,rank,
                         config.ACHIEVE['follower']['messages'],config.ACHIEVE['follower']['points']))
                    except:
                        pass
                    Likes.update_notify(user_id=userid,notify=1,group_id=group_id,rank=rank)
                    print('updated waiting fot next')
            elif (user_messages >=apprenticemsg and user_messages < instructormsg ) and (totalpts>=apprenticepts and totalpts < instructorpts):
                print("cretia passed")
                rank = config.RANKS[2]
                if Likes.check_likes(user_id=userid,group_id=group_id,rank=rank)==False:
                    Likes(user_id=userid,username=username,rank=rank,group_id=group_id).save()
                likes = Likes.get_likes_count(user_id=user.id, group_id=group_id, rank=rank)
                key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                  callback_data=f'like+{userid}+{rank}+{username}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                if Likes.get_notify_status(user_id=userid,group_id=group_id,rank=rank)==0:
                    print("cretia reached sending msg")
                    context.bot.send_message(chat_id=group_id, text=texts.ADVANCE.format(username, rank),
                                             reply_markup=main_markup)
                    try:
                        context.bot.send_photo(chat_id=userid,photo=config.LOGOS['apprentice'])
                        context.bot.send_message(chat_id=userid,text=texts.ACHIEVEMENT.format(username,rank,
                         config.ACHIEVE['apprentice']['messages'],config.ACHIEVE['apprentice']['points']))
                    except:
                        pass
                    Likes.update_notify(user_id=userid,notify=1,group_id=group_id,rank=rank)
                    print('updated waiting fot next')
            elif (user_messages >=instructormsg and user_messages < mastermsg ) and (totalpts>=instructorpts and totalpts < masterpts):
                print("cretia passed")
                rank = config.RANKS[3]
                if Likes.check_likes(user_id=userid,group_id=group_id,rank=rank)==False:
                    Likes(user_id=userid,username=username,rank=rank,group_id=group_id).save()
                likes = Likes.get_likes_count(user_id=user.id, group_id=group_id, rank=rank)
                key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                  callback_data=f'like+{userid}+{rank}+{username}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                if Likes.get_notify_status(user_id=userid,group_id=group_id,rank=rank)==0:
                    print("cretia reached sending msg")
                    context.bot.send_message(chat_id=group_id, text=texts.ADVANCE.format(username, rank),
                                             reply_markup=main_markup)
                    try:
                        context.bot.send_photo(chat_id=userid,photo=config.LOGOS['instructor'])
                        context.bot.send_message(chat_id=userid,text=texts.ACHIEVEMENT.format(username,rank,
                         config.ACHIEVE['instructor']['messages'],config.ACHIEVE['instructor']['points']))
                    except:
                        pass
                    Likes.update_notify(user_id=userid,notify=1,group_id=group_id,rank=rank)
                    print('updated waiting fot next')
            elif (user_messages >=mastermsg and user_messages < titanmsg ) and (totalpts>=masterpts and totalpts < titanpts):
                print("cretia passed")
                rank = config.RANKS[4]
                if Likes.check_likes(user_id=userid,group_id=group_id,rank=rank)==False:
                    Likes(user_id=userid,username=username,rank=rank,group_id=group_id).save()
                likes = Likes.get_likes_count(user_id=user.id, group_id=group_id, rank=rank)
                key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                  callback_data=f'like+{userid}+{rank}+{username}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                if Likes.get_notify_status(user_id=userid,group_id=group_id,rank=rank)==0:
                    print("cretia reached sending msg")
                    context.bot.send_message(chat_id=group_id, text=texts.ADVANCE.format(username, rank),
                                             reply_markup=main_markup)
                    try:
                        context.bot.send_photo(chat_id=userid,photo=config.LOGOS['master'])
                        context.bot.send_message(chat_id=userid,text=texts.ACHIEVEMENT.format(username,rank,
                         config.ACHIEVE['master']['messages'],config.ACHIEVE['master']['points']))
                    except:
                        pass
                    Likes.update_notify(user_id=userid,notify=1,group_id=group_id,rank=rank)
                    print('updated waiting fot next')

            elif (user_messages >=titanmsg and totalpts>=titanpts):
                print("cretia passed")
                rank = config.RANKS[5]
                if Likes.check_likes(user_id=userid,group_id=group_id,rank=rank)==False:
                    Likes(user_id=userid,username=username,rank=rank,group_id=group_id).save()
                likes = Likes.get_likes_count(user_id=user.id, group_id=group_id, rank=rank)
                key_main = [[InlineKeyboardButton(emoji.emojize(f'like :heart: {likes}', use_aliases=True),
                                                  callback_data=f'like+{userid}+{rank}+{username}')]]
                main_markup = InlineKeyboardMarkup(key_main)
                if Likes.get_notify_status(user_id=userid,group_id=group_id,rank=rank)==0:
                    print("cretia reached sending msg")
                    context.bot.send_message(chat_id=group_id, text=texts.ADVANCE.format(username, rank),
                                             reply_markup=main_markup)
                    try:
                        context.bot.send_photo(chat_id=userid,photo=config.LOGOS['titan'])
                        context.bot.send_message(chat_id=userid,text=texts.ACHIEVEMENT.format(username,rank,
                         config.ACHIEVE['titan']['messages'],config.ACHIEVE['titan']['points']))
                    except:
                        pass
                    Likes.update_notify(user_id=userid,notify=1,group_id=group_id,rank=rank)
                    print('updated waiting fot next')






