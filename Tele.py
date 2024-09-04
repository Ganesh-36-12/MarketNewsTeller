import requests
import os
import logging
import logging.handlers
from Database import *

def log_event(msg):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)
    logger.info(msg)

try:
    API_KEY = os.environ["API_KEY"]
    group_id = os.environ["GROUP_ID"]
except KeyError:
    log_event("Token not available!")

base_url = f'https://api.telegram.org/bot{API_KEY}'

def meta_data_collector(response):
  json_data = response.json()
  Message_id = json_data["result"]["message_id"]
  Group_id = json_data["result"]["chat"]["id"]
  temp = (Message_id, Group_id)
  insert_data_into_db("meta_data",temp)

def send_msg(text,from_file):  
    text_send = f'{base_url}/sendMessage'
    params = {
        'chat_id' : group_id,
        'text' : text
    }
    r = requests.get(url = text_send, params =params)
    if r.status_code == 200:
        log_event(f"Message Sent Successfully through {from_file}")
        meta_data_collector(r)
    else:
        log_event(f"error occured with status code {r.status_code}")

def get_update():
    update = f'{base_url}/getUpdates'
    return update


