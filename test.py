import os
from Tele import send_msg,get_update

arr = os.environ["TEST_ARRAY"]

for i in arr:
  send_msg(str(i),"test.py")
print("messages sent")

context = get_update()
print(context)
