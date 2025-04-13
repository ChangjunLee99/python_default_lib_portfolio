# 네이버 지도 크롤링
#pip install selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# run webdriver
driver = webdriver.Chrome()
keyword = '서울 강남구 정보통신'
url = f'https://map.naver.com/p/search/{keyword}'
driver.get(url)
action = ActionChains(driver)

naver_res = pd.DataFrame(columns=['업체명','업종','주소','URL'])
last_name = ''
def search_iframe():
    driver.switch_to.default_content()
    driver.switch_to.frame("searchIframe")

def entry_iframe():
    driver.switch_to.default_content()
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="entryIframe"]')))

    for i in range(5):
        time.sleep(.5)

        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="entryIframe"]'))
            break
        except:
            pass

def chk_names():
    search_iframe()
    elem = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li/div[1]/div/a[1]/div/div/span[1]')
    name_list = [e.text for e in elem]

    return elem, name_list

def crawling_main():
    global naver_res
    addr_list = []
    category_list = []
    url_list = []

    for e in elem:
        e.click()
        entry_iframe()
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # append data
        try:
            category_list.append(soup.select('span.DJJvD')[0].text)
        except:
            category_list.append(float('nan'))
        try:
            addr_list.append(soup.select('span.LDgIH')[0].text)
        except:
            addr_list.append(float('nan'))
        try:
            url_list.append(soup.select('a.place_bluelink.CHmqa')[0]['href'])
        except:
            url_list.append(float('nan'))

        search_iframe()

    naver_temp = pd.DataFrame([name_list,category_list,addr_list,url_list], index=naver_res.columns).T
    naver_res = pd.concat([naver_res, naver_temp])
    naver_res.to_excel('./naver_crawling_result.xlsx')

page_num = 1

while 1:
    time.sleep(.5)
    search_iframe()
    elem, name_list = chk_names()
    if last_name == name_list[-1]:
        pass

    while 1:
        # auto scroll
        action.move_to_element(elem[-1]).perform()
        elem, name_list = chk_names()

        if last_name == name_list[-1]:
            break
        else:
            last_name = name_list[-1]

    crawling_main()

    # next page
    driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div[2]/div[2]/a[7]').click()
    time.sleep(1.5)
    
    
#멜론 크롤링
# pip install requests
# pip install bs4
# import requests
# from bs4 import BeautifulSoup
    
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://www.melon.com/chart/',headers=headers)
    
# soup = BeautifulSoup(data.text, 'html.parser')
    
# top_100 = soup.select('#lst50 > td > div') #tr로 이루어진 list
    
# for tr in top_100 :
#     rank = tr.select_one('span.rank')
        
#     if rank is not None:
#         print(rank.text, end=". ")
        
#     title = tr.select_one('div > div.ellipsis.rank01 > span > a')
    
#     if title is not None:
#         artist = tr.select_one('div.ellipsis.rank02 > a').text
#         print(artist,'-', title.text)

a=0