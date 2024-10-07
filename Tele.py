import requests
import os
import logging
import logging.handlers
from Database import *
from datetime import datetime, timedelta


class ISTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Convert the time to IST
        record_time = datetime.fromtimestamp(record.created) + timedelta(hours=5, minutes=30)
        return record_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')

def log_event(msg):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    
    formatter = ISTFormatter("%(asctime)s - %(message)s")
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

def send_styled_msg(news_string,from_file):
    s_url = f'{base_url}/sendMessage'
    params = {
      'chat_id':group_id,
      'text': news_string,
      'parse_mode': 'MarkdownV2'
    }
    msg_resp = requests.get(url=s_url,params = params)
    if msg_resp.status_code == 200:
        log_event(f"Styled Message Sent Successfully through {from_file}")
        meta_data_collector(msg_resp)
    else:
        log_event(f"error occured with status code {msg_resp.status_code}")
        print(msg_resp.text)

def send_photo(data_dict,from_file):
    p_url = f'{base_url}/sendPhoto'
    for k,v in data_dict.items():
        params = {
            'chat_id':group_id,
            'caption': k,
            'photo': v,
            'parse_mode': 'MarkdownV2'
        }
        photo_resp = requests.get(url=p_url,params = params)
        if photo_resp.status_code == 200:
            log_event(f"Photo Sent Successfully through {from_file}")
            meta_data_collector(photo_resp)
        else:
            log_event(f"error occured with status code {photo_resp.status_code}")
            print(photo_resp.text)
            
def get_update():
    update = f'{base_url}/getUpdates'
    return update


