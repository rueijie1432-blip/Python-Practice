# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:43:24 2026

@author: w10
"""
'''
把某某網站的資料爬下來
標題`連結‵時間然後輸出
'''

# 先import爬蟲相關的
import requests
from bs4 import BeautifulSoup
# 為了存成csv
import pandas as pd

titlelist = []
timelist = []
linklist = []
classlist = []
# 然後抓網址
r = requests.get('https://udn.com/news/cate/2/6639')
# 然確認網址有沒有爆掉
if r.status_code == requests.codes.ok:
    # 抓該網址的特定資料
    # 爬蟲套件爬的網址內容存成文本
    soup = BeautifulSoup(r.text,"html.parser")
    
    # 用選擇器抓
    # 標籤
    aTags1 = soup.select("div.context-box__content.story-list__holder div.story-list__text h3 a")
    aTags2 = soup.select("div.story-list__text h2 a")
    atag = aTags1+aTags2
    # 時間
    time = soup.select("time.story-list__time")
    # 抓資料
    #for titles in title:
    for atags,times in zip(atag,time):
        classlist.append("社會")
        # 標題
        titlelist.append(atags.text.strip())
        # 連結
        linklist.append("https://udn.com"+atags.get("href"))
        # 時間
        timelist.append(times.text.strip())

#建立表格
df = pd.DataFrame({
    "類別":classlist,
    "標題":titlelist,
    "連結":linklist,
    "時間":timelist,
    })

# print(df)

# 存成csv
df.to_csv("udn.csv",encoding="big5")