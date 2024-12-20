import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
from Tele import send_msg,send_styled_msg
from Database import *

raw_time = datetime.utcnow()+timedelta(hours=5,minutes=30)
current_time = raw_time.strftime("%H:%M")
current_hour = raw_time.strftime("%I %p")
current_hour_unix = raw_time.strftime("%-I")
current_hour_windows = raw_time.strftime("%#I")
AM_PM = raw_time.strftime("%p")
current_date = raw_time.strftime("%d %b %Y")


def website(site_url):
    user_agents_list = ['Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
                        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',]
    old_news = fetch_old_news("BS_SCRAPED")
    print("Old news: ",old_news)
    r = requests.get(url=site_url,headers={'User-Agent': random.choice(user_agents_list)})
    status = r.status_code
    if status ==200:
        list_1 = web_crawl(r,old_news)
        return list_1
    else:
        print("Status code",status)

def web_crawl(r,l_news):
    soup = BeautifulSoup(r.content, 'html.parser')
    job_cards = soup.find_all('div', class_='listingstyle_cardlistlist__dfq57 cardlist')
    title_list =[]
    
    for jobs in job_cards:
        title = jobs.find('a').text
        time_cards = jobs.find_all('span',class_='listingstyle_updtText__lnZb7')
        for time in time_cards:
            time_stamp = time.span.text
            date = time_stamp[13:24]
            upload_time = time_stamp[26:35].strip()
            if date.startswith(current_date):
                if(title==l_news):
                    insert_data_into_db("BS_SCRAPED",title_list)
                    return title_list
                else:
                     title_list.append(title)
    insert_data_into_db("BS_SCRAPED",title_list)
    print("No of news: ",len(title_list))
    return title_list

def string_builder(news):
    final_string = current_hour+' News update\n'
    if news:
        for i in news:
            final_string = final_string + i +'\n\n'    
    else:
        final_string += 'No news update'
    return final_string

morning_emoji_list = ['🌄', '🌅', '🌇' , '🌻', '☀️', '🌞']
url = f"https://www.business-standard.com/markets/news"
news_list = website(url)

if current_hour == "09 AM":
  greeting = "*Good morning* " + random.choice(morning_emoji_list)
  send_styled_msg(greeting,"Business standard")

text = string_builder(news_list)
print(text)
send_msg(text,"Business standard")
