import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
from Tele import send_msg

json_file = 'news_data.json'

raw_time = datetime.utcnow()+timedelta(hours=5,minutes=30)

current_time = raw_time.strftime("%H:%M")

current_hour = raw_time.strftime("%I %p")
current_date = raw_time.strftime("%b %d, %Y")

b_url ='https://www.businesstoday.in/markets/company-stock'

def create_json_file():
    if not os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump([], file)  
            
def load_json_data():
    with open(json_file, 'r') as file:
        return json.load(file)

def append_to_json(data):
    json_data = load_json_data()
    print(json_data)
    if json_data and  json_data[-1].values()==data.values():
        return
    json_data.append(data)
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent=4)

create_json_file()

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

r = requests.get(url=b_url,headers=headers)

if(r.status_code==200):
    soup = BeautifulSoup(r.content, 'html.parser')
    job_cards = soup.find_all('div', class_='widget-listing-content-section')
       
def web_scrape(l_news=None):
    title_list=[]
    for i in job_cards:
     span_tags = i.find('span')
     for k in span_tags:
         web_time = k.text[10:]
         if(web_time==current_date):
             title_card = i.find('h2').find_all('a')
             for j in title_card:
                 title = j.get('title')
                 if(title==l_news):
                     return title_list
                 else:
                     title_list.append(title)
    data = {}
    data[current_time]=title_list[0]
    append_to_json(data)
    return title_list

def hourly_news():
   json_data = load_json_data()
   if json_data:
       my_dict = json_data[-1]
       last_key, last_value = next(reversed(my_dict.items())) 
   else:
       last_value = None
   return last_value

old_news=hourly_news()
news = web_scrape(l_news=old_news)


def string_builder(news):
    final_string = current_hour+' News update\n'
    if news:
        for i in news:
            final_string = final_string + i +'\n\n'    
    else:
        final_string += 'No news update'
    return final_string
    
text = string_builder(news)
#send_msg(text,"bt_news.py")
