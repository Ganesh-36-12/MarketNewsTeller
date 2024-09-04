import os
import requests
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

def forward_msg(f_url,chat_id,from_id):
  last_id = fetch_last_id("last_id")
  if last_id:
    id = last_id[0]
  else:
    id = 128
  messages = fetch_all_id(id)
  converted = json.dumps(messages)
    
  params = {
      'chat_id' : chat_id,
      'from_chat_id' : from_id,
      'message_ids' : converted,
      'protect_content' : True
  }
  forward = f"{f_url}/forwardMessages"
  response = requests.get(url = forward, params = params)
    
  if response.status_code==200:
    log_event(f"Message forwarded Successfully")
    final_commit()
  else:
    log_event(f"error occured with status code {r.status_code}")
    
try:
  FORWARDER_API_KEY = os.environ["FORWARDER_API_KEY"]
  METRICS_GROUP_ID = os.environ["METRICS_GROUP_ID"]
  METRICS_CHANNEL_ID = os.environ["METRICS_CHANNEL_ID"]
except KeyError:
  print(KeyError) 

try:
  base_url = f'https://api.telegram.org/bot{FORWARDER_API_KEY}'
  forward_msg(base_url,METRICS_GROUP_ID,METRICS_CHANNEL_ID)
except Exception as e:
  print(e)
