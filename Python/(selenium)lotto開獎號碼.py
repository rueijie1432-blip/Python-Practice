# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 15:36:19 2026

@author: w10
"""

# 網頁自動化套件
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# 爬蟲套件
from bs4 import BeautifulSoup
# 日期套件
from time import sleep

# 期數搜尋
def issueQuery(issueNumber):
    # 用chrome當瀏覽器
    driver = webdriver.Chrome()
    url = "https://www.taiwanlottery.com/lotto/result/lotto649"
    driver.get(url)
    
    # 等
    sleep(2)
    
    # 找到輸入框
    input_box = driver.find_element(By.CLASS_NAME,"el-input__inner")
    # 自動輸入期別
    input_box.send_keys(issueNumber)
    
    # 自動按查詢
    driver.find_element(
    By.XPATH,
    '//button[@class="el-button el-button--primary"]'
    ).click()
    
    # 等
    sleep(2)
    
    # 取得網頁html+解析
    data = driver.page_source
    soup = BeautifulSoup(data,"html.parser")
    
    # 抓內容
    title = soup.find('div', class_='period-title').text
    date = soup.find('div', class_='period-date').text
    numbers = soup.find_all('div', class_='ball special-number')
    
    print(title,date,sep=" ")
    print("開獎號碼為： ", end="")
    for num in numbers:
        print(num.text, end=' ') 

    return

# 搜尋方式
choose = input("請輸入>(1)期別查詢 (2)年/月查詢 : ")

# 期別輸入
if choose == "1":
    issueNumber = input("請輸入期別 : ")
    issueQuery(issueNumber)
    
# 年月輸入
elif choose == "2":
    print("目前僅提供期別輸入")
    # %%
    '''
    while True:
        start_year = int(input("請輸入起始年份 : "))
        start_month = int(input("請輸入起始月份 : "))
        
        end_year = int(input("請輸入截止年份 : "))
        end_month = int(input("請輸入截止月份 : "))
        
        # 檢查月份1~12
        if not (1 <= start_month <= 12 and 1 <= end_month <= 12):
            print("請輸入正確的月份範圍1~12")
            continue
        
        #　計算是否最多相差兩個月
        total_start = start_year * 12 + start_month
        total_end = end_year * 12 + end_month
        total_diff = total_end - total_start
        
        # 檢查輸入範圍
        if total_diff < 0 :
            print("起始日不能大於截止日，請重新輸入")
            continue
        
        if total_diff > 1:
            print("查詢範圍在兩個月內，請重新輸入")
            continue
        
        # 民國年轉換 -1911
        today_year = datetime.date.today().year - 1911
        today_month = datetime.date.today().month
        
        # 檢查日期是否超過今天
        if end_year > today_year or start_year < today_year - 2:
            print("年份不能超過今年")
            print("最久查詢到",today_year - 2,"年")
    '''
    

