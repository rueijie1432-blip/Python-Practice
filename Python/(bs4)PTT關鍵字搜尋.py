# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:36:31 2026

@author: w10
"""

# 爬蟲相關套件
import requests
from bs4 import BeautifulSoup
# 日期套件
from datetime import date

# 取得今天
today = date.today()
# 分割
dateDate = (str(today)).split("-")
# 分別儲存年月日
year = dateDate[0]
month = str(int(dateDate[1]))
day = int(dateDate[2])

def ptt(keyword,search):
    
    # ptt的網址
    ptturl = "https://www.ptt.cc/ask/over18"
    
    # 剛進去會有18歲驗證，用 F12 查看 按下我已滿18歲 時送出的 payload
    payload={
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
        }
    
    # 紀錄登入身分
    rss = requests.session()
    
    # 模擬使用chrom
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'}
    rss.post(
        ptturl,
        data = payload,
        headers = headers
        )
    
    # 輸入完之後會進下頁
    url = "https://www.ptt.cc/bbs/gossiping/index.html"
    
    
    # 要搜尋的日期範圍 dat是今天，search是使用者輸入要搜尋幾天內的
    daterange = [day-search,day]
    
    while 1:
        # 抓網址(有登入身分)
        r = rss.get(url)
        # 確認網址回應
        if r.status_code == requests.codes.ok:
            # 轉文本，解析器
            soup = BeautifulSoup(r.text,"html.parser")
            # 抓日期
            date = soup.select("div.date")
            title = soup.select("div.title > a")
            link = soup.select("div.title > a")
            # 上一頁
            u = soup.select("a.btn.wide")
            # 因為 u 有四個按鈕 ， u[1]是上一頁
            url = "https://www.ptt.cc" + u[1]["href"]
            
            #用迴圈依序抓
            for dates,titles,links in zip(date,title,link):
                # 比對抓到的日期是不是我要的範圍
                dd = dates.text.strip()
                tt = titles.text.strip()
                if "Re:" in tt:
                    continue
                if keyword not in tt:
                    continue
                for i in range(daterange[1],daterange[0],-1):
                    if month + "/" + str(i) == dd:
                        print(tt,dd)
                    if month + "/" + str(daterange[0]-1) == dd:
                        print("已經抓完了!")
                        return
            
"""
讓使用者輸入 新聞關鍵字 還有 想搜尋幾天
跑入函式
"""

while 1:
    keyword = input("請輸入想搜尋的新聞關鍵字(或按Q結束程式):")
    if keyword == "Q" or keyword == "q":
        break
    else:
        search = int(input("請輸入想搜尋幾天的新聞:"))
        ptt(keyword,search)







