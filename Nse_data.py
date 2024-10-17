
import requests
import json
from Tele import send_msg

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
}
def fiidii():
  site_url = 'https://www.nseindia.com/api/fiidiiTradeReact'
  r = requests.get(url=site_url,headers=headers).json()
  message = (f"{r[0]['date']}\n")
  for i in r:
      message += (f"category : {i['category']}\n")
      message += (f"Buy value : {i['buyValue']}\n")
      message +=(f"Sell value : {i['sellValue']}\n")
      message +=(f"Net value : {i['netValue']}\n\n")
  return message

def get_vix():
  site_url = 'https://www.nseindia.com/api/allIndices'
  response = requests.get(url=site_url,headers=headers).json()
  temp_list = response['data']
  for i in temp_list:
    if(i['index']=="INDIA VIX"):
      return i
    
def india_VIX():
  vix_data = get_vix()
  last= float(vix_data['last'])
  diff = last - float(vix_data['open'])
  vix_msg= (f"India VIX : {last:.2f} {diff:.2f} ({vix_data['percentChange']}%)")
  return vix_msg

try:
      msg = fiidii()
      vix = india_VIX()
      send_msg(msg,"nse_data.py")
      send_msg(vix,"nse_data.py")
except:
      print("error occured")
