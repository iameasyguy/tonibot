from sql import *
import util
last_id = Seshat.get_last_seshat_id(user_id=214196949)
msg = Seshat.get_seshat_question(qid=last_id,user_id=214196949)
admin = Users.check_admin(user_id=214196949)
apolo_qstn_type = Apolo.get_apolo_question_type(msg_id=1067)
qstn_type = util.question_type(message_id=1067)
data = Zamol.get_zamol_qstnsby_msgid(msg_id=1115,group_id=-1001278314934)
print(Players.check_player(user_id=214196949,game_no=1171))