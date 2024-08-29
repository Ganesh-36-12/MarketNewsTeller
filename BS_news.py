import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
from Tele import send_msg
import sqlite3 as sq

raw_time = datetime.utcnow()+timedelta(hours=5,minutes=30)
current_time = raw_time.strftime("%H:%M")
current_hour = raw_time.strftime("%I %p")
current_hour_unix = raw_time.strftime("%-I")
current_hour_windows = raw_time.strftime("%#I")
AM_PM = raw_time.strftime("%p")
current_date = raw_time.strftime("%d %b %Y")

# try:
#     conn = sq.connect('info_collector_BS.db')
#     cursor = conn.cursor()
#     create_command = """
#     CREATE TABLE IF NOT EXISTS 
#     SCRAPED (NEWS STRING NOT NULL);
#     """
#     cursor.execute(create_command)
# except Exception as e:
#     print(e)
    
def insert_data_into_db(n_list):
    try:
        insert_command = """
        INSERT INTO SCRAPED (NEWS) VALUES(?);
        """
        last = (n_list[0],)
        cursor.execute(insert_command,last)
        conn.commit()
    except Exception as e:
        print(e)


def website(site_url):
  headers = {
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
      }

  r = requests.get(url=site_url,headers=headers)
  status = r.status_code
  if status ==200:
    dict_1 = web_crawl(r)
    return dict_1

def web_crawl(r):
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
      if (upload_time.startswith(current_hour_unix)) and upload_time.endswith(AM_PM) and date.startswith(current_date):
        title_list.append(title)
  return title_list

def string_builder(news):
    final_string = current_hour+' News update\n'
    if news:
        for i in news:
            final_string = final_string + i +'\n\n'    
    else:
        final_string += 'No news update'
    return final_string


news_list =[]
for i in range(1,4):
  url = f"https://www.business-standard.com/markets/news/page-{i}"
  temp = website(url)
  news_list.extend(temp)

text = string_builder(news_list)
print(text)
send_msg(text,"BS_news.py")
