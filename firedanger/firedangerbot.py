import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import tweepy
import threading
import configparser

config = configparser.RawConfigParser()
configFilePath = r'secret.config'
config.read(configFilePath)

consumer_key = config.get('key','twitter_consumer_key')
consumer_secret = config.get('key','twitter_consumer_secret')
access_token = config.get('key','twitter_access_token')
access_token_secret = config.get('key','twitter_access_secret')

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)




def firedanger():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time == '13:00:00':
            print('yes')
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            #chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument(f"--window-size=1920,1800")
            chrome_options.add_argument("--hide-scrollbars")
            browser = webdriver.Chrome(options=chrome_options)
            browser.get('https://portal.ct.gov/DEEP/Forestry/Forest-Fire/Forest-Fire-Danger-Report')
            time.sleep(3)
            element = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/main/section[2]')
            time.sleep(3)
            element.screenshot('.\FireDanger.png')
            size = element.size
            print(size)
            print(size['height'])
            # Setting the points for cropped image
            left = 800
            top = 100
            right = 1520
            bottom = 300
            # Opens a image in RGB mode
            im = Image.open(r"FireDanger.png")
            #im.show()
            im1 = im.crop((left, top, right, bottom))
            #im1.show()
            im1.save(".\FireDangercrop.png", 'PNG')
            browser.close()
            img = r".\FireDangercrop.png"
            screenshot = '.\FireDanger.png'
            api.update_status_with_media("Todays Fire Danger PER CT-DEEP https://portal.ct.gov/DEEP/Forestry/Forest-Fire/Forest-Fire-Danger-Report #QuietCornerAlerts",img)
        else:
            print("Fire Danger Current Time =", current_time)
            time.sleep(1)