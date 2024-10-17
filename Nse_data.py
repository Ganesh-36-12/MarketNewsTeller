
import requests
import json
from Tele import send_msg

headers = {
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
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
  
    
msg = fiidii()
vix = india_VIX()

send_msg(msg,"nse_data.py")
send_msg(vix,"nse_data.py")
