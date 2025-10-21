
import json
import requests
from bs4 import BeautifulSoup
from datetime import date
from Tele import *

today = date.today()
current_date = today.strftime("%B %d, %Y")

url ="https://api.moneycontrol.com/mcapi/v1/premarket/article?slug=trade-setup&limit=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'If-None-Match': 'W/"7496-cxUlVxxa+MZPaUO9jDHj93Ds60Q"',
    'Priority': 'u=0, i',
}

r =  requests.get(url,headers=headers)

try:
  data = r.json()
  article = json.loads(data['data']['trade_setup'][0]['article_data'])
  post_url = article['posturl']

  news = article['body'].replace("\r","").replace(",","")

  soup = BeautifulSoup(news,'html.parser')
except Exception as e:
  print(f"Excepton {e} occured ")

def get_images():
  image_dict ={}
  img = soup.find_all('img')
  image_dict["NIFTY 50"] = img[0].get('src')
  image_dict["Bank NIFTY"] = img[1].get('src')
  return image_dict

def number_extractor(points_list,r_s):
    count = 1
    temp_string = ''
    for point in points_list:
        if point.isdigit():
            temp_string += f"*{r_s}{count}*: {point} "
            count +=1
    return temp_string

def resistance_support():
    splitted = news.split("\n")
    resistance_data = []
    support_data = []
    for lines in splitted:
        if lines.startswith("Resistance based on pivot points:"):
            resistance_data.append(lines.split(": ")[1])
        if lines.startswith("Support based on pivot points:"):
            support_data.append(lines.split(": ")[1])
        
    nifty_r_data = resistance_data[0].split()
    bank_nifty_r_data = resistance_data[1].split()

    nifty_s_data = support_data[0].split()
    bank_nifty_s_data = support_data[1].split()

    content_dict = {"nifty":{"resistance":{},"support":{}},
                "bank_nifty":{"resistance":{},"support":{}}}
    
    content_dict["nifty"]["resistance"] = number_extractor(nifty_r_data,"R")
    content_dict["bank_nifty"]["resistance"] = number_extractor(bank_nifty_r_data,"R")
    content_dict["nifty"]["support"] = number_extractor(nifty_s_data,"S")
    content_dict["bank_nifty"]["support"] = number_extractor(bank_nifty_s_data,"S")
    return content_dict


def f_o_ban():
  f_o = news.replace("&amp;","&").split("\n")
  ban_string = "*Stocks retained in F&O ban:*\n"
  for i in f_o:
      if i.startswith("Stocks added") or i.startswith("Stocks retained"):
          banned = i.split(": ")[1]
          if banned != "Nil":
              ban_string += banned

  return ban_string


def string_builder():
  content_dict = resistance_support()
  final = f"{current_date}\nNIFTY\n"
  final += content_dict["nifty"]["resistance"] + "\n"
  final += content_dict["nifty"]["support"] + "\n\n"
  final += f"BANK NIFTY\n"
  final += content_dict["bank_nifty"]["resistance"] + "\n"
  final += content_dict["bank_nifty"]["support"] + "\n\n"
  
  return final

try:
  print("today's link: ",post_url)
  final_string = string_builder() + f_o_ban()
  send_styled_msg(final_string,"mc_extractor")
  print(final_string)
  image_dict = get_images()
  print(image_dict)
  send_photo(image_dict,"mc_extractor")
except Exception as e:
  print(e)
