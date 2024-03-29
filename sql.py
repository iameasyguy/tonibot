from mongoengine import *
connect('main', host='localhost', port=27017)


class Users(Document):
    user_id = IntField(required=True, unique=True)
    username = StringField(required=True)
    role = IntField(required=True,default=0)

    @queryset_manager
    def check_user(self, queryset, user_id):
        try:
            if queryset.filter(user_id=user_id)[0]:
                return True
        except:
            return False
    @queryset_manager
    def check_admin(self,checkadmin,user_id):
        if checkadmin.filter(user_id=user_id,role=1):
            return 1
        elif checkadmin.filter(user_id=user_id,role=2):
            return 2
        else:
            return False

    @queryset_manager
    def set_role(self,set_role,user_id,role):
        set_role.filter(user_id=user_id)[0].update(role=role)
        return f"role updated to {role}"

    @queryset_manager
    def get_all_admins(self,queryset):

        return queryset.filter(role=2)

    @queryset_manager
    def delete_admin(self,queryset,user_id):
        queryset.filter(user_id=user_id).delete()




class Groups(Document):
    group_id = IntField(required=True,unique=True)
    group_title = StringField(required=True)
    group_language =StringField(null=True)
    user_id = IntField(required=True,unique=True)

    @queryset_manager
    def check_group_id(self, checka_group, group_id):
        try:
            if checka_group.filter(group_id=group_id)[0]:
                return True
        except:
            return False

    @queryset_manager
    def update_group_language(self, set_language, language,group_id,user_id):
        set_language.filter(group_id=group_id,user_id=user_id)[0].update(group_language=language)
        return f"language updated to {language}"

    @queryset_manager
    def get_group_adder(self,queryset, group_id):
        return queryset.filter(group_id=group_id)[0].user_id

    @queryset_manager
    def get_group_language(self,queryset, group_id):
        return queryset.filter(group_id=group_id)[0].group_language

    @queryset_manager
    def del_group(self,queryset, group_id):
        queryset.filter(group_id=group_id).delete()






class Answers(Document):
    user_id =IntField(required=True)
    username =StringField(null=True)
    correct = IntField(required=True,default=0)
    incorrect = IntField(required=True,default=0)
    answertype = StringField(null=True)
    group_id = IntField(null=True)


    @queryset_manager
    def check_user_answer(self,queryset , user_id,group_id,answertype):
        try:
            if queryset.filter(user_id=user_id,answertype=answertype)[0]:
                return queryset.filter(user_id=user_id,group_id=group_id,answertype=answertype)[0].user_id
        except:
            return False

    @queryset_manager
    def get_correct_incorrect(self,queryset ,user_id,answertype,group_id):
        incorrect =queryset.filter(user_id=user_id,answertype=answertype,group_id=group_id)[0].incorrect
        correct = queryset.filter(user_id=user_id, answertype=answertype,group_id=group_id)[0].correct
        return correct,incorrect

    @queryset_manager
    def update_correct(self,queryset,correct,answertype,user_id,group_id):

        return queryset.filter(user_id=user_id,answertype=answertype,group_id=group_id)[0].update(correct=correct)

    @queryset_manager
    def update_incorrect(self, queryset, incorrect, answertype, user_id,group_id):

        return queryset.filter(user_id=user_id,answertype=answertype,group_id=group_id)[0].update(incorrect=incorrect)

    @queryset_manager
    def get_all_points_by_group(self,queryset,user_id,group_id):
        try:
            total = queryset.filter(user_id=user_id, group_id=group_id).sum('correct')
            return total
        except IndexError:
            return 0


    @queryset_manager
    def get_all_users_points(self,queryset,group_id,user_id):
        return queryset.filter(user_id=user_id,group_id=group_id,)[0].username,queryset.filter(user_id=user_id,group_id=group_id,).sum('correct')


    @queryset_manager
    def get_all_apolo_by_group(self, queryset, user_id, group_id):
        try:
            apolo = queryset.filter(user_id=user_id, group_id=group_id, answertype='apolo')[0].correct
            return apolo
        except IndexError:
            return 0



    @queryset_manager
    def get_all_africa_by_group(self, queryset, user_id, group_id):
        try:
            africa = queryset.filter(user_id=user_id, group_id=group_id, answertype='africa')[0].correct
            return africa
        except IndexError:
            return 0


    @queryset_manager
    def get_all_seshat_by_group(self, queryset, user_id, group_id):
        try:
            seshat = queryset.filter(user_id=user_id, group_id=group_id, answertype='seshat')[0].correct
            return seshat
        except IndexError:
            return 0


    @queryset_manager
    def get_all_gaia_by_group(self, queryset, user_id, group_id):
        try:
            gaia = queryset.filter(user_id=user_id, group_id=group_id, answertype='gaia')[0].correct
            return gaia
        except IndexError:
            return 0


    @queryset_manager
    def get_all_sherlock_by_group(self, queryset, user_id, group_id):
        try:
            sherlock = queryset.filter(user_id=user_id, group_id=group_id, answertype='sherlock')[0].correct
            return sherlock
        except IndexError:
            return 0


    @queryset_manager
    def get_all_zamol_by_group(self, queryset, user_id, group_id):
        try:
            zamol = queryset.filter(user_id=user_id, group_id=group_id, answertype='zamol')[0].correct
            return zamol
        except IndexError:
            return 0






class Apolo(Document):
    user_id = IntField(required=True)
    username = StringField(required=True)
    question = StringField(null=True)
    answer = StringField(null=True)
    group_id = IntField(null=True)
    message_id = IntField(null=True)
    question_type= StringField(null=True)
    status = IntField(default=0)

    @queryset_manager
    def get_last_apolo_id(self,queryset, user_id):
        return queryset.filter(user_id=user_id).order_by('-id').first().id

    @queryset_manager
    def get_apolo_answer(self,queryset,user_id,answer):
        try:
            if queryset.filter(user_id=user_id, answer=answer)[0].answer is not None:
                return True
        except IndexError:
            return False

    @queryset_manager
    def get_apolo_answer_by_msg_id(self,queryset,msg_id):
        return queryset.filter(message_id =msg_id)[0].answer

    @queryset_manager
    def change_apolo_qstn_status(self,queryset,status,msg_id):
        return queryset.filter(message_id=msg_id)[0].update(status=status)

    @queryset_manager
    def get_apolo_question(self, queryset, qid):
        return queryset.filter(id =qid)[0].question

    @queryset_manager
    def get_apolo_qstn_status(self, queryset, msg_id):
        return queryset.filter(message_id=msg_id)[0].status

    @queryset_manager
    def change_apolo_qstn_group_id(self, queryset, group_id,qid,user_id):
        return queryset.filter(id=qid,user_id=user_id)[0].update(group_id=group_id)

    @queryset_manager
    def update_apolo_msgid_qstn_type(self,queryset,message_id,question_type,tbl_id,user_id):
        return queryset.filter(id=tbl_id, user_id=user_id)[0].update(message_id=message_id,question_type=question_type)

    @queryset_manager
    def get_apolo_question_type(self,queryset,msg_id):
        try:
            if queryset.filter(message_id=msg_id)[0].question_type is not None:
                return queryset.filter(message_id=msg_id)[0].question_type
        except IndexError:
            return False




class Seshat(Document):
    user_id = IntField(required=True)
    file_id= StringField(null=True)
    question = StringField(null=True)
    answer = StringField(null=True)
    group_id = IntField(null=True)
    message_id = IntField(null=True)
    question_type = StringField(null=True)
    status = IntField(default=0)

    @queryset_manager
    def get_last_seshat_id(self, queryset, user_id):
        return queryset.filter(user_id=user_id).order_by('-id').first().id

    @queryset_manager
    def change_seshat_qstn(self,queryset, question, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(question=question)

    @queryset_manager
    def change_seshat_answer(self,queryset, answer, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(answer=answer)

    @queryset_manager
    def change_seshat_group_id(self, queryset,group_id, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(group_id=group_id)

    @queryset_manager
    def get_seshat_question(self, queryset, qid,user_id):
        return queryset.filter(id=qid,user_id=user_id)[0].question,queryset.filter(id=qid,user_id=user_id)[0].file_id

    @queryset_manager
    def change_seshat_message_id(self,queryset, message_id, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(message_id=message_id)

    @queryset_manager
    def get_seshat_question_type(self,queryset,msg_id):
        try:
            if queryset.filter(message_id=msg_id)[0].question_type is not None:
                return queryset.filter(message_id=msg_id)[0].question_type
        except IndexError:
            return False


    @queryset_manager
    def get_seshat_answer_by_msg_id(self, queryset,msg_id):
        return queryset.filter(message_id=msg_id)[0].answer

    @queryset_manager
    def get_seshat_qstn_status(self, queryset, msg_id):
        return queryset.filter(message_id=msg_id)[0].status

    @queryset_manager
    def change_seshat_qstn_status(self,queryset, status, msg_id):
        return queryset.filter(message_id=msg_id)[0].update(status=status)


class Zamol(Document):
    user_id = IntField(required=True)
    file_id = StringField(null=True)
    question = StringField(null=True)
    answer = StringField(null=True)
    group_id = IntField(null=True)
    message_id = IntField(null=True)
    question_type = StringField(null=True)
    status = IntField(default=0)
    lang = StringField(null=True)

    @queryset_manager
    def get_last_zamol_id(self, queryset, user_id):
        return queryset.filter(user_id=user_id).order_by('-id').first().id

    @queryset_manager
    def get_zamol_qstn_lang(self, queryset, tbl_id, user_id):
        return queryset.filter(user_id=user_id,id=tbl_id)[0].lang

    @queryset_manager
    def change_zamol_fileid(self,queryset, file_id, question, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(file_id=file_id,question=question)

    @queryset_manager
    def get_zamol_question(self, queryset,tbl_id, user_id):
        query =queryset.filter(id=tbl_id,user_id=user_id)[0]
        return query.lang,query.question,query.file_id,query.group_id

    @queryset_manager
    def change_zamol_qstn_message_id(self,queryset, message_id, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(message_id=message_id)

    @queryset_manager
    def update_zamol_clip_qstn(self,queryset, question, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(question=question)
    @queryset_manager
    def get_zamol_question_type(self, queryset,msg_id):
        try:
            if queryset.filter(message_id=msg_id)[0].question_type is not None:
                return queryset.filter(message_id=msg_id)[0].question_type
        except IndexError:
            return False




    @queryset_manager
    def get_zamol_qstnsby_msgid(self,queryset, msg_id, group_id):
        return queryset.filter(message_id=msg_id,group_id=group_id)[0]
    @queryset_manager
    def get_zamol_qstn_status(self,queryset, msg_id):
        return queryset.filter(message_id=msg_id)[0].status
    @queryset_manager
    def change_zamol_qstn_status(self,queryset, status, msg_id):
        return queryset.filter(message_id=msg_id)[0].update(status=status)




class Gaia(Document):
    user_id = IntField(required=True)
    file_id = StringField(null=True)
    question = StringField(null=True)
    group_id = IntField(null=True)
    message_id = IntField(null=True)
    question_type = StringField(null=True)
    status = IntField(default=0)
    lang = StringField(null=True)

    @queryset_manager
    def get_last_gaia_id(self, queryset, user_id):
        return queryset.filter(user_id=user_id).order_by('-id').first().id
    @queryset_manager
    def get_gaia_qstn_lang(self,queryset, tbl_id, user_id):
        return queryset.filter(id=tbl_id, user_id=user_id)[0].lang

    @queryset_manager
    def change_gaia_fileid(self, queryset,file_id, question,  user_id,tbl_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(file_id=file_id, question=question)
    @queryset_manager
    def get_gaia_question(self,queryset, tbl_id, user_id):
        query = queryset.filter(id=tbl_id,user_id=user_id)[0]
        return query.lang, query.question, query.file_id, query.group_id
    @queryset_manager
    def change_gaia_qstn_message_id(self,queryset, message_id, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(message_id=message_id)

    @queryset_manager
    def update_gaia_clip_qstn(self,queryset, question, tbl_id, user_id):
        return queryset.filter(id=tbl_id, user_id=user_id)[0].update(question=question)

    @queryset_manager
    def get_gaia_question_type(self,queryset, msg_id):
        try:
            if queryset.filter(message_id=msg_id)[0].question_type is not None:
                return queryset.filter(message_id=msg_id)[0].question_type
        except IndexError:
            return False


    @queryset_manager
    def get_gaia_qstnsby_msgid(self,queryset, msg_id, group_id):
        query= queryset.filter(message_id=msg_id,group_id=group_id)[0]
        return query.lang,query.question
    @queryset_manager
    def get_gaia_qstn_status(self,queryset, msg_id):
        return queryset.filter(message_id=msg_id)[0].status
    @queryset_manager
    def change_gaia_qstn_status(self,queryset, status, msg_id):
        return queryset.filter(message_id=msg_id)[0].update(status=status)

class Sherlock(Document):
    user_id = IntField(required=True)
    file_id = StringField(default="0")
    question = StringField(null=True)
    group_id = IntField(null=True)
    message_id = IntField(null=True)
    question_type = StringField(null=True)
    status = IntField(default=0)
    lang = StringField(null=True)

    @queryset_manager
    def get_last_sherlock_id(self, queryset, user_id):
        return queryset.filter(user_id=user_id).order_by('-id').first().id

    @queryset_manager
    def change_sherlock_fileid(self, queryset, file_id,question,tbl_id,user_id):
        return queryset.filter(id=tbl_id, user_id=user_id)[0].update(file_id=file_id, question=question)

    @queryset_manager
    def change_sherlock_group_id(self, queryset, group_id, tbl_id, user_id):
        return queryset.filter(id=tbl_id, user_id=user_id)[0].update(group_id=group_id)

    @queryset_manager
    def change_sherlock_qstn_status(self, queryset, status,tbl_id,user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].update(status=status)

    @queryset_manager
    def change_sherlock_qstn_message_id(self, queryset, message_id,tbl_id,user_id):
        return queryset.filter(id=tbl_id, user_id=user_id)[0].update(message_id=message_id)

    @queryset_manager
    def get_sherlock_question(self, queryset, tbl_id, user_id):
        query = queryset.filter(id=tbl_id, user_id=user_id)[0]
        return query.question, query.file_id

    @queryset_manager
    def get_sherlock_qstn_file_id(self,queryset, tbl_id, user_id):
        return queryset.filter(id=tbl_id,user_id=user_id)[0].file_id

    @queryset_manager
    def get_sherlock_question_type(self, queryset, msg_id):
        try:
            if queryset.filter(message_id=msg_id)[0].question_type is not None:
                return queryset.filter(message_id=msg_id)[0].question_type
        except IndexError:
            return False

class Sherlockchance(Document):
    user_id = IntField(required=True)
    chances = IntField(default=0)
    group_id = IntField(required=True)

    @queryset_manager
    def get_user_chance(self, queryset, user_id, group_id):
        try:
            if queryset.filter(user_id=user_id,group_id=group_id)[0].chances is not None:
                return queryset.filter(user_id=user_id,group_id=group_id)[0].chances
        except IndexError:
            return False

    @queryset_manager
    def update_user_chance(self,queryset,user_id,chances):
        return queryset.filter(user_id=user_id)[0].update(chances=chances)


class Afrique(Document):
    question = StringField(null=True)
    answer = StringField(null=True)
    pickone =StringField(null=True)
    picktwo = StringField(null=True)
    pickthree = StringField(null=True)
    pickfour = StringField(null=True)
    group_id = IntField(null=True)
    message_id = IntField(null=True)
    question_type = StringField(null=True)

    @queryset_manager
    def get_allQuestion(self, queryset, msg_id,group_id):
        query = queryset.filter(message_id=msg_id,group_id=group_id).order_by('-id').first()
        # return query
        return query.question, query.answer, query.message_id, query.pickone, query.picktwo, query.pickthree, query.pickfour, query.group_id

class Africhance(Document):
    user_id = IntField(required=True)
    chances = IntField(default=0)
    group_id = IntField(required=True)

    @queryset_manager
    def get_user_chance(self, queryset, user_id, group_id):
        try:
            if queryset.filter(user_id=user_id,group_id=group_id)[0].chances is not None:
                return queryset.filter(user_id=user_id,group_id=group_id)[0].chances
        except IndexError:
            return False

    @queryset_manager
    def update_user_chance(self, queryset, user_id, chances):
        return queryset.filter(user_id=user_id)[0].update(chances=chances)






class Games(Document):
    admin_id =IntField(required=True)
    game_no = IntField(null=True)
    joined = IntField(default=0)
    status = IntField(default=0)
    group_id = IntField(null=True)

    @queryset_manager
    def get_game_no(self, queryset, game_no):
        try:
            if queryset.filter(game_no=game_no)[0].game_no is not None:
                return queryset.filter(game_no=game_no)[0].game_no
        except IndexError:
            return False

    @queryset_manager
    def get_game_admin(self, queryset, game_no):
        query = queryset.filter(game_no=game_no)[0]
        return query.admin_id

    @queryset_manager
    def get_last_game_id(self, queryset, group_id):
        return queryset.filter(group_id=group_id).order_by('-id').first().id

    @queryset_manager
    def get_game_no_from_id(self, queryset, tid):
        query = queryset.filter(id=tid)[0]
        return query.game_no

    @queryset_manager
    def update_joined(self, queryset, joined, game_no):
        return queryset.filter(game_no=game_no)[0].update(joined=joined)

    @queryset_manager
    def update_game_status(self, queryset, status, game_no):
        return queryset.filter(game_no=game_no)[0].update(status=status)

    @queryset_manager
    def get_game_status(self, queryset, game_no):
        query = queryset.filter(game_no=game_no)[0]
        return query.status

    @queryset_manager
    def get_game_joined(self, queryset, game_no):
        return queryset.filter(game_no=game_no)[0].joined


class Players(Document):
    game_no= IntField(required=True)
    user_id = IntField(null=True)
    chances = IntField(default=0)

    @queryset_manager
    def check_player(self, queryset, user_id,game_no):
        try:
            if queryset.filter(user_id=user_id,game_no=game_no)[0].user_id is not None:
                return True
        except IndexError:
            return False

    @queryset_manager
    def get_count(self,queryset,game_no):
        return queryset.filter(game_no=game_no).count()

    @queryset_manager
    def set_chance(self, queryset, chance,user_id,game_no):
        return queryset.filter(user_id=user_id,game_no=game_no)[0].update(chances=chance)

    @queryset_manager
    def get_chance(self, queryset, user_id,game_no):
        return queryset.filter(user_id=user_id,game_no=game_no)[0].chances


class Likes(Document):
    user_id =IntField(required=True)
    username =StringField(required=True)
    rank = StringField(required=True)
    group_id =IntField(required=True)
    likes = IntField(default=0)
    notify = IntField(default=0)

    @queryset_manager
    def check_likes(self, queryset, user_id, group_id,rank):
        try:
            if queryset.filter(user_id=user_id, group_id=group_id,rank=rank)[0].likes is not None:
                return True
        except IndexError:
            return False

    @queryset_manager
    def update_likes(self, queryset, user_id, likes, group_id,rank):
        return queryset.filter(user_id=user_id, group_id=group_id,rank=rank)[0].update(likes=likes)

    @queryset_manager
    def get_likes_count(self, queryset, user_id, group_id,rank):
        return queryset.filter(user_id=user_id, group_id=group_id,rank=rank)[0].likes

    @queryset_manager
    def get_notify_status(self, queryset, user_id, group_id, rank):
        return queryset.filter(user_id=user_id, group_id=group_id, rank=rank)[0].notify

    @queryset_manager
    def update_notify(self, queryset, user_id, notify, group_id, rank):
        return queryset.filter(user_id=user_id, group_id=group_id, rank=rank)[0].update(notify=notify)



class Likers(Document):
    user_id =IntField(required=True)
    liked = IntField(required=True)
    rank = StringField(required=True)
    group_id = IntField(required=True)

    @queryset_manager
    def check_liker(self, queryset, user_id, group_id, rank,liked):
        try:
            if queryset.filter(user_id=user_id, group_id=group_id, rank=rank,liked=liked)[0] is not None:
                return True
        except IndexError:
            return False

class Messages(Document):
    user_id = IntField(required=True)
    username = StringField(required=True)
    messages = IntField(default=0)
    group_id = IntField(required=True)


    @queryset_manager
    def update_messages(self,queryset,user_id,messages,group_id):
        return queryset.filter(user_id=user_id)[0].update(messages=messages,group_id=group_id)

    @queryset_manager
    def get_messages_count(self,queryset,user_id,group_id):
        try:
            if queryset.filter(user_id=user_id,group_id=group_id)[0].messages is not None:
                return queryset.filter(user_id=user_id,group_id=group_id)[0].messages
        except IndexError:
            return 0


    @queryset_manager
    def check_messages(self, queryset, user_id,group_id):
        try:
            if queryset.filter(user_id=user_id,group_id=group_id)[0].user_id is not None:
                return True
        except IndexError:
            return False

class Ranking(Document):
    user_id = IntField(required=True)
    status = IntField(default=0)

    @queryset_manager
    def check_ranking_status(self, queryset, user_id):
        try:
            if queryset.filter(user_id=user_id)[0].status is not None:
                return True
        except IndexError:
            return False