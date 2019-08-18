import operator

from sql import *
import config
# print(Answers.get_all_points_by_group(user_id=214196949,group_id=-1001278314934))

# data = []
#
# for user_id in Answers.objects.distinct('user_id'):
#     answ =Answers.get_all_users_points(user_id=user_id,group_id=-1001278314934)
#     data.append(answ)
#
# print(data[:1])
# #
# scoreboard = dict((x, y) for x, y in data)
# print(scoreboard)
#
# scoreboard_x = sorted(scoreboard.items(), key=operator.itemgetter(1), reverse=True)[:10]
# # points = Answers.get_all_points_by_group(user_id=214196949,group_id=-1001278314934)
# print(scoreboard_x)
# #
# # position = data.index(("Iameasyguy", points))
# # print(position+1)
# position = 0
# for each in scoreboard_x:
#     position +=1
#     print(f"{position}.  {each[0]} earned {each[1]} points")

def top_scoreboard(group_id):
    data = []
    for user_id in Answers.objects.distinct('user_id'):
        data.append(Answers.get_all_users_points(user_id=user_id, group_id=group_id))
    scoreboard = dict((x, y) for x, y in data)
    scoreboard_x = sorted(scoreboard.items(), key=operator.itemgetter(1), reverse=True)[:10]
    position = 0
    score = []
    for each in scoreboard_x:
        position += 1
        score.append(f"{position}.  {each[0]} earned {each[1]} points")
    return score


print("\n".join(top_scoreboard(-1001278314934)))
