import re
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from Tele import *
from googlesearch import *

def todayArticle(soup):
  raw_time = datetime.utcnow()+timedelta(hours=5,minutes=30)
  current_date = raw_time.strftime("%B %d, %Y")

  upload_date = soup.find('div',class_="article_schedule").span.text
  if current_date == upload_date:
    return True
  return False

def get_images(soup):
  image_cont = soup.find('div',{'id':'contentdata'})
  images = image_cont.find_all('img',{'width':"1281"})
  image_dict = {}
  image_dict["NIFTY 50"] = images[0].get('src')
  image_dict["Bank NIFTY"] = images[1].get('src')
  return image_dict

def number_extractor(data_list,r_s):
  count = 1
  temp_string = ''
  for i in data_list:
    cs = i.replace(",",'')
    if cs.isdigit():
      temp_string += f"*{r_s}{count}*: {cs} "
      count +=1
  return temp_string

def resistance_support(soup):
  resistance = soup.find_all('p',string=re.compile("^Resistance based on pivot points:"))
  nifty_r_data = resistance[0].text[34:].split()
  bank_nifty_r_data = resistance[1].text[34:].split()

  support = soup.find_all('p',string=re.compile("^Support based on pivot points:"))
  nifty_s_data = support[0].text[31:].split()
  bank_nifty_s_data = support[1].text[31:].split()

  content_dict ={"nifty":
                        {"resistance":{},
                        "support":{}
                        },
                  "bank_nifty":
                        {"resistance":{},
                        "support":{}
                        }
                }
  content_dict["nifty"]["resistance"] = number_extractor(nifty_r_data,"R")
  content_dict["bank_nifty"]["resistance"] = number_extractor(bank_nifty_r_data,"R")
  content_dict["nifty"]["support"] = number_extractor(nifty_s_data,"S")
  content_dict["bank_nifty"]["support"] = number_extractor(bank_nifty_s_data,"S")
  return content_dict

def f_o_ban(soup):
  retain = soup.find('p',string=re.compile("^Stocks retained in F&O ban:"))
  added = soup.find('p',string=re.compile("^Stocks added to F&O ban:"))
  ban_string = "*Stocks retained in F&O ban:*\n"
  for cmp in retain.text[28:].split(","):
    ban_string += cmp.strip() + "\n"
  for org in added.text[24:].split(","):
    ban_string += org.strip() + "\n"

  return ban_string

raw_time = datetime.utcnow()+timedelta(hours=5,minutes=30)
current_date = raw_time.strftime("%B %d, %Y")

query = "moneycontrol top 15 things to do latest"

results = search(query=query,num=1,stop=1)

link = [x for x in results]
mc_url = link[0]
headers = {
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
      }
mc_resp = requests.get(url=mc_url,headers=headers)
print(mc_resp.status_code)
mc_soup = BeautifulSoup(mc_resp.content, 'html.parser')

def string_builder(soup):
  content_dict = resistance_support(soup)
  final = f"{current_date}\nNIFTY\n"
  final += content_dict["nifty"]["resistance"] + "\n"
  final += content_dict["nifty"]["support"] + "\n\n"
  final += f"BANK NIFTY\n"
  final += content_dict["bank_nifty"]["resistance"] + "\n"
  final += content_dict["bank_nifty"]["support"] + "\n\n"
  return final

if todayArticle:
  print("latest news detected")
  final_string = string_builder(mc_soup) + f_o_ban(mc_soup)
  image_dict = get_images(mc_soup)
  send_styled_msg(final_string,"mc_extractor")
  send_photo(image_dict,"mc_extractor")
else:
  print("waiting for the latest update")
