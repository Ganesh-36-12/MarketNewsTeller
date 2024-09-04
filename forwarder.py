import os
import requests
from Tele import forward_msg
from Database import *

try:
  FORWARDER_API_KEY = os.environ["FORWARDER_API_KEY"]
  METRICS_GROUP_ID = os.environ["METRICS_GROUP_ID"]
  METRICS_CHANNEL_ID = os.environ["METRICS_CHANNEL_ID"]
except KeyError:
  print(KeyError) 

base_url = f'https://api.telegram.org/bot{FORWARDER_API_KEY}'

try:
  forward_msg(base_url,METRICS_GROUP_ID,METRICS_CHANNEL_ID)
except Exception as e:
  print(e)
