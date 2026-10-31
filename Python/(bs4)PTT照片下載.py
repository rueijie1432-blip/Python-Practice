# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:52:31 2026

@author: w10
"""

# 匯入爬蟲套件
from bs4 import BeautifulSoup
import requests
# 資料夾
import os
# 正規表示法
import re

def pttimage(keyword,image_count):

    # 圖片檔名計數
    piccount = 0
    
    # 假裝瀏覽器
    myHeader = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
        }
    # 保存登入資訊
    r = requests.Session()
    # 滿18的按鈕的資料
    payload ={
    "from":"/bbs/Beauty/index.html",
    "yes":"yes"
    }
    # 送出請求 網址，post fromdata,uesr
    r.post("https://www.ptt.cc/ask/over18",
        payload,
        headers=myHeader
        )     
    
    # 目標網址
    url = "https://www.ptt.cc/bbs/Beauty/index.html"
    
    # 建立等等要存圖片的資料夾(exist_ok資料夾 已經存在 要不要 報錯)
    os.makedirs(keyword,exist_ok=True)
    
    # 前置動作好了之後開始抓內容
    while 1:
        # 抓標題，網址
        title = []
        titleUrl = []
        # 抓網址(get)
        r2 = r.get(url,headers=myHeader)
        # 網址解析
        soup = BeautifulSoup(r2.text,"html.parser")
        
        # 抓標題
        sel = soup.select("div.title a")
        # 抓上頁按鈕 會抓到4個a 所以等等[1]才是上頁
        u = soup.select("div.btn-group.btn-group-paging a")
        # 自動輸入上頁
        url = "https://www.ptt.cc" + u[1]["href"]
        # 開始抓對應標題
        for s in sel:
            if keyword in s.text:
                title.append(s.text)
                titleUrl.append(s["href"])
                
        # 現在有整頁面網址，要逐一抓
        for i in range(len(titleUrl)):
            url2 = "https://www.ptt.cc" + titleUrl[i]
            # 已經抓到有圖片的該網址了
            r3 = r.get(url2,headers = myHeader)
            # 解析
            soup = BeautifulSoup(r3.text,"html.parser")
            
            # 爬出文章 圖片 網址
            # 用正規的方式找出 有 圖檔 名稱
            # $ 表示從網址尾端檢查是否一樣
            sel2 = soup.find_all("a",href = re.compile("(gif|jpg|jpeg|png)$"))
            # 現在有圖片對應標籤了，要下載然後存資料夾
            for s in sel2:
                # 抓圖片連結
                picUrl = s["href"]

                resp2 = r.get(picUrl,headers = myHeader)
                # 抓到圖檔後就不用再解析
                # 避免存到壞掉的連結圖檔
                if resp2.status_code == 200:
                    # 存檔名，把副檔名的部分找出來
                    dotPosition = picUrl.rfind(".")
                    # 圖片檔名 組合
                    foldername = keyword + "/" + str(piccount + 1) + picUrl[dotPosition:]
                    # "wb" 會建新檔
                    with open(foldername,"wb") as f:
                        # f.write(resp2.content)怕資料太大
                        # 所以分段下載(跑的是二進制資料)
                        # Response 物件提供的特殊行為所以這邊的for跑的資料比較特殊
                        # for chunk in resp2.iter_content(1024):
                        for chunk in resp2:
                            f.write(chunk)            
                        # 如果存檔的資料已經到了使用者要的數量
                        # 成功存檔的話圖片計數 + 1
                        piccount += 1
                        if piccount == image_count:
                            print("--------------------------------------------")
                            print("已經都抓完囉")
                            return



# 帥哥 正妹 新垣結衣"
# 輸入 誰的照片，要幾張
while 1:
    keyword = input("請輸入想搜尋誰的照片(Q)結束:")
    if keyword == "Q" or keyword == "q":
        print("程式結束")
        break
    else:
        image_count = eval(input("請輸入想搜尋幾張:"))
        pttimage(keyword,image_count)