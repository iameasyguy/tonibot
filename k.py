from sql import *

print(len(Groups.objects))

for data in Groups.objects:
    print(data)

