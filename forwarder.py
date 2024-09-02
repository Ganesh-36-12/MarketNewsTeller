import os
import requests
from Tele import *
from Database import *

try:
  API_KEY = os.environ["API_KEY"]
  chat_id = os.environ["METRICS_GROUP_ID"]
  from_id = os.environ["METRICS_CHANNEL_ID"]
except KeyError:
  logger.info("Token not available!")

base_url = f'https://api.telegram.org/bot{API_KEY}'

forward_msg(base_url,chat_id,from_id)
