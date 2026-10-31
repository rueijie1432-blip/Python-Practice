# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 17:05:42 2026

@author: w10
"""

# 爬蟲套件
from bs4 import BeautifulSoup
import requests
# 影像辨識套件
import pytesseract
# 開圖檔套件
from PIL import Image

def zipSearch(county,county2,road):
    while True: 

        s = requests.Session()
        r = s.get("https://www.post.gov.tw/post/internet/SearchZone/index.jsp?ID=130107")
        soup = BeautifulSoup(r.text,"html.parser")
        
        #找input的id
        vkey = soup.select_one("input#vKey").get("value")
        #爬驗證碼圖片
        checkimageurl = "https://www.post.gov.tw/post/internet/" + soup.select_one("img#imgCaptcha3_zip6").get("src")[3:]
        
        # 爬圖片網址
        rr = s.get(checkimageurl)
        if rr.status_code == 200:
            #把圖片存下來
            with open("checkimage.jpg","wb") as f:
                for data in rr:
                    f.write(data)
                    
            # ocr安裝位置
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\\tesseract.exe"
            # 開圖檔
            img = Image.open("checkimage.jpg")
            # 轉成灰階(L)圖片
            img = img.convert("L")
            # OCR辨識
            ans = str.strip(pytesseract.image_to_string(img,config='--psm 6'))
            
            # 建表單資料
            payload = { "list":"5",
                        "list_type": "1",
                        "firstView": "3",
                        "vKey": vkey,
                        "city_zip6": county,
                        "cityarea_zip6": county2,
                        "street_zip6": road,
                        "checkImange_zip6": ans,
                        "Submit": "查詢" }
            print("查詢中")
            r = s.post("https://www.post.gov.tw/post/internet/SearchZone/index.jsp?ID=130107" , data = payload)
            if r.status_code == 200:
                if "驗證碼輸入錯誤" in r.text:
                    continue
                soup = BeautifulSoup(r.text,'html.parser')

                zips = soup.find_all("td", attrs={"data-th":"郵遞區號"})
                ranges = soup.find_all("td", attrs={"data-th":"投遞範圍"})
                
                for z,r in zip(zips,ranges):
                    print(z.text,r.text)
                    
                break

county = input("請輸入想搜尋的縣市: ")
county2 = input("請輸入想搜尋的鄉鎮[市]區: ")
road = input("請輸入想搜尋的路(街)名或鄉里: ")
zipSearch(county,county2,road)
    
    
    
    
    