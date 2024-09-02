import requests
import os
import logging
import logging.handlers
from Database import *

create_tables()

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
    logger.info("Token not available!")

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

def forward_msg():
    last_id = fetch_last_id("last_id")
    chat_id = os.environ["METRICS_GROUP_ID"]
    from_id = os.environ["METRICS_CHANNEL_ID"]
    messages = fetch_all_id(last_id[0])
    converted = json.dumps(messages)

    params = {
      'chat_id' : chat_id,
      'from_chat_id' : from_id,
      'message_ids' : converted,
      'protect_content' : True
    }
    forward = f"{base_url}/forwardMessages"
    response = requests.get(url = forward, params = params)
    
    if response.status_code==200:
        log_event(f"Message forwarded Successfully")
    else:
        log_event(f"error occured with status code {r.status_code}")
