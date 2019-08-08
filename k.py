from sql import *

last_id = Seshat.get_last_seshat_id(user_id=214196949)
msg = Seshat.get_seshat_question(qid=last_id,user_id=214196949)
admin = Users.check_admin(user_id=214196949)


