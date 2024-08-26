import requests
import os

API_KEY = os.environ("API_KEY")

base_url = f'https://api.telegram.org/bot{API_KEY}'

group_id = os.environ("GROUP_ID")

def send_msg(text):  
    text_send = f'{base_url}/sendMessage?chat_id={group_id}&text={text}'
    r = requests.get(text_send)
    print(r.status_code)
    print('message sent')

