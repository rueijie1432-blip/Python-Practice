# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 21:20:48 2026

@author: w10
"""

# 自動控制套件
# 控制瀏覽器
from selenium import webdriver
# 等待網頁元素
from selenium.webdriver.support.ui import WebDriverWait
# 等待條件
from selenium.webdriver.support import expected_conditions
# 指定元素
from selenium.webdriver.common.by import By
# 爬蟲套件
from bs4 import BeautifulSoup

# chrome啟動設定
options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36")
# 禁用 blink 自動化偵測的核心參數
options.add_argument("--disable-blink-features=AutomationControlled")
# 自動打開google(啟動設定)
driver = webdriver.Chrome(options=options)
# 網址
url = "https://tw.yahoo.com/"
driver.get(url)

# 分析元素
element = driver.find_element(By.ID,'header-search-input')
element.send_keys('Hello World')

driver.find_element(By.ID,'header-desktop-search-button').click()

# 等待元素 表格id為div 出現
element = WebDriverWait(driver, 5).until(
    expected_conditions.presence_of_element_located((By.ID, 'web'))
)

# 解析網頁(page_source)
soup=BeautifulSoup(driver.page_source,"html.parser")
links = soup.select('div#web h3')

for link in links:
    print(link.text)

driver.quit()