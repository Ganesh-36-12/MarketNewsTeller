import requests

API_KEY = '7415761715:AAH9FEYkjn02fghc8g0kIJ6xwEveUe3MhWM'

base_url = f'https://api.telegram.org/bot{API_KEY}'

group_id = -4590021123

def send_msg(text):  
    text_send = f'{base_url}/sendMessage?chat_id={group_id}&text={text}'
    r = requests.get(text_send)
    print(r.status_code)
    print('message sent')

