import requests
import os
import logging
import logging.handlers

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

def send_msg(text,from_file):  
    text_send = f'{base_url}/sendMessage?chat_id={group_id}&text={text}'
    r = requests.get(text_send)
    if r.status_code == 200:
        log_event(f"Message Sent Successfully through {from_file}")
    else:
        log_event(f"error occured with status code {r.status_code}")
def get_update():
    update = f'{base_url}/getUpdates'
    return update
