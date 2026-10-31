# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 17:39:22 2026

@author: w10
"""

# 自動打開google
from selenium import webdriver
# 找網頁元素
from selenium.webdriver.common.by import By
# 模擬鍵盤
from selenium.webdriver.common.keys import Keys
# 時間
import time
# 爬蟲
from bs4 import BeautifulSoup

def sele(keywords):
    
    # chrome啟動設定
    options = webdriver.ChromeOptions()
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36")
    # 禁用 blink 自動化偵測的核心參數
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 自動打開google(啟動設定)
    driver = webdriver.Chrome(options=options)
    url = "https://www.google.com"
    driver.get(url)
    
    # 找網頁元素 (定位屬性,定位值)
    box = driver.find_element(By.NAME, "q")
    
    time.sleep(1)
    # 自動輸入
    box.send_keys(keywords)
    box.send_keys(Keys.ENTER)
    time.sleep(3)
    
    # 直接用 selenium 取得 html
    html = driver.page_source
    ''' 這樣爬不到
    import requests
    url = driver.current_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    '''
    soup = BeautifulSoup(html,"html.parser")
    
    titles = soup.select("h3")
    for title in titles:
            print("標題:", title.text)
    
    driver.quit()
    
keywords = "爬蟲"
sele(keywords)