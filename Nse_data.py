from nsepython import *
from Tele import send_msg

def fiidii():
    list_1=nse_fiidii("list")
   
    message = (f"{list_1[0]['date']}\n")
    for i in list_1:
        message += (f"category : {i['category']}\n")
        message += (f"Buy value : {i['buyValue']}\n")
        message +=(f"Sell value : {i['sellValue']}\n")
        message +=(f"Net value : {i['netValue']}\n\n")
    return message
    
def india_VIX():
    vix_data = nse_get_index_quote('INDIA VIX')
        
    last= float(vix_data['last'])
    diff = last - float(vix_data['open'])
    vix_msg= (f"India VIX : {last:.2f} {diff:.2f} ({vix_data['percChange']}%)")
    return vix_msg
    
try:
      msg = fiidii()
      send_msg(msg,"nse_data.py")
except:
    try:
        print("FII DII Retrying....")
        msg = fiidii()
        send_msg(msg,"nse_data.py")
    except:
        print(" FII DII retry failed")
try:
      vix = india_VIX()
      send_msg(vix,"nse_data.py")
except:
    try:
      print("VIX Retrying....")
      vix = india_VIX()
      send_msg(vix,"nse_data.py")
    except:
        print("VIX retry failed")
