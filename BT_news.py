import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
from Tele import send_msg
from Database import *


raw_time = datetime.utcnow()+timedelta(hours=5,minutes=30)

current_time = raw_time.strftime("%H:%M")
current_hour = raw_time.strftime("%I %p")
current_date = raw_time.strftime("%b %d, %Y")

b_url ='https://www.businesstoday.in/markets/company-stock'

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
                     insert_data_into_db("scraped",title_list)
                     return title_list
                 else:
                     title_list.append(title)
    insert_data_into_db("scraped",title_list)
    return title_list

old_news=fetch_old_news("scraped")
news = web_scrape(l_news=old_news)


def string_builder(news):
    final_string = current_hour+' News update\n'
    if news:
        for i in news:
            final_string = final_string + i +'\n\n'    
    else:
        final_string += 'No news update'
    return final_string

cursor.close()
text = string_builder(news)
print(text)
send_msg(text,"Business Today")
