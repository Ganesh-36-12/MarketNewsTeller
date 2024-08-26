import requests
from bs4 import BeautifulSoup




b_url ='https://www.businesstoday.in/markets/company-stock'

to_find = 'class="widget-listing-thumb"'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url=b_url,headers=headers)
print(r.status_code)

soup = BeautifulSoup(r.content, 'html5lib')
job_cards = soup.find_all('div', class_='widget-listing-thumb')

for i in job_cards:
 title_card = i.find_all('a')
 for j in title_card:
     
     print('          ',j.get("title"))
 #print(title_card.get('title'))
 