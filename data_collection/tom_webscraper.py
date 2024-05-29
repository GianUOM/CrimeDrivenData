import os
import re
import sys
import signal
import requests
import pandas as pd
from time import sleep
from selenium import webdriver
from ws_methods import WebScraper
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By

m = WebScraper(folder_name='times_of_malta')

def signal_handler(sig,frame):
    print('SIG Received - Saving..')
    pd.DataFrame(columns=columns,
            data=data).to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False)
    driver.quit()
    sys.exit()

def get_img_ext(img_link):
    if img_link.endswith('.jpeg'):
        return '.jpeg'
    elif img_link.endswith('.jpg'):
        return '.jpg'
    elif img_link.endswith('.png'):
        return '.png'
    else: return ""

service = webdriver.ChromeService()
service = webdriver.ChromeService(executable_path=m.CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Opening required website to scrape content 
driver.get('https://timesofmalta.com/news/crime')

#Closing pop-ups
print('Closing initial pop-ups: ',end='')
driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]').click()
print('[OK]')


data = []
img_count = 0
pg_article_sz = 17

num_pgs = 100  # 17 articles per page
save_every = 5
assert num_pgs%save_every == 0

columns = ['Title','Author','Body','URL']

#^C Handler to save on signal.
signal.signal(signal.SIGINT, signal_handler)

next_page = 'https://timesofmalta.com/news/crime'

for pg_idx in range(num_pgs+1):

    print("\n -- Next Page: " + next_page + " --")
    driver.get(next_page)
    #Find (next) page
    next_page = driver.find_element(By.XPATH,"//a[@class='page-link' and @rel='next']").get_attribute("href")


    try:
        #Remove donation message
        try: driver.find_element(By.XPATH,'//*[@id="eng-accept"]').click()
        except: pass

        #Get links to all articles in page
        links = [i.find_element(By.TAG_NAME,'a').get_attribute('href') 
                for i in driver.find_elements(By.CLASS_NAME,"li-ListingArticles_sub")]

        for a in links:
            print("\nLink: " + a)
            #Go to article
            driver.get(a)

            #Get Title
            sleep(0.5)
            title = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/h1').text
            print(f'Extracting: {title[:30]}... ',end='')
            
            #Get Author
            try:    author = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/div[2]/div[1]/span[2]/span/a').text
            except: author = driver.find_element(By.XPATH,'//*[@id="article-head"]/div/div[2]/div[1]/span[2]/span').text

            #Get URL
            url = driver.current_url

            #Get Body
            text_content = driver.find_element(By.XPATH,'//*[@id="observer"]/main/article/div[2]/div')
            body = " ".join(p.text for p in text_content.find_elements(By.TAG_NAME,'p'))
            
            #Add row
            data.append([title,author,body,url])

            print('[OK]')
            

        #Save to csv
        if pg_idx%save_every == 0:
            print('\nSaving...')
            (pd.DataFrame(columns=columns,data=data)
             .to_csv(os.path.join(m.NEWS_PATH,'data.csv'), index=False))
    
    except Exception as e:
        print(f'[ERR]')

