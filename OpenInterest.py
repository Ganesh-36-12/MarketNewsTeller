import os
import time
import glob
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def send_photo(data_dict,fromfile):
    api = os.environ["API_KEY"]
    base_url = f"https://api.telegram.org/bot{api}"
    p_url = f'{base_url}/sendPhoto'
    for k,v in data_dict.items():
        p_path = v
        with open(p_path, 'rb') as photo:
          # Prepare the payload
          payload = {
              'chat_id': -4590021123,
              'caption': k
          }
          files = {
              'photo': photo
          }
          response = requests.post(p_url, data=payload, files=files)
          print(response.json())
    print("message sent from",fromfile)

login_url = 'https://opstra.definedge.com/ssologin'

OI_USERNAME = os.environ["OI_USERNAME"]
OI_PASSWORD = os.environ["OI_PASSWORD"]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
capabilities = {}
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
options.set_capability('cloud:options', capabilities)
prefs = {
    "download.default_directory": "./content/",
    "download.prompt_for_download": False,
    "profile.default_content_settings.popups": 0,
    "directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 5)

try:
    driver.get(login_url)
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )

    username_field.send_keys(OI_USERNAME)
    password_field.send_keys(OI_PASSWORD)

    login_button = driver.find_element(By.ID, 'kc-login')
    login_button.click()

    time.sleep(2)

    success_url = 'https://opstra.definedge.com/openinterest'

    driver.get(success_url)

    time.sleep(2)

    def get_image(filename):
        svg_element = driver.find_element(By.CSS_SELECTOR,"svg.highcharts-root")
        driver.set_window_size(750,800)
        time.sleep(2)
        svg_element.screenshot(f"{filename}.png")

    def ticker_selector(text):
      option_selector_template = """
      window.scrollTo(0, document.body.scrollHeight);
      const elements = document.getElementsByClassName('v-list__tile__title');
      for (let element of elements) {
          if (element.textContent.trim() === 'replace') {
              element.click();
              break;
          }
      }
      """
      option_selector = option_selector_template.replace("replace",text)
      driver.execute_script(option_selector)
      get_image(text)


    ticker_selector("NIFTY")
    ticker_selector("BANKNIFTY")
    ticker_selector("FINNIFTY")

    print("Images download")
    png_f= (glob.glob("*.png"))
    img_dict = {}
    for i in png_f:
      f_name = i.rstrip(".png")
      img_dict[f_name]=i
    send_photo(img_dict,"Openinterest")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    png_f= (glob.glob("*.png"))
    for file in png_f:
        os.remove(file)
        print(f'Removed file: {file}')
