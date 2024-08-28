import os
from Tele import send_msg

arr = os.environ["TEST_ARRAY"]

for i in arr:
  send_msg(str(i),"test.py")
print("messages sent")
