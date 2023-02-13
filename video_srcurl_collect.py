from bs4 import BeautifulSoup
import re
import pdb
import requests
import pandas as pd
from logger import getLogger

# 로그 생성
lg = getLogger()

def getSource(page_source: str):

    # pdb.set_trace()
    html = page_source
    soup = BeautifulSoup(html, "lxml")
    # soup = BeautifulSoup(r.content,"html.parser")
    
    data = list()

    try:
        # content = soup.select('.bd-list tbody')[0].text
        videoSource = soup.select_one('.file-list dd a')["href"]
        lg.warning(videoSource)
        data.append('https://www.fss.or.kr'+videoSource)
            
        
    except Exception as e:
        lg.error(f"error: {e}")
        
    return data[0]

# def move_next(driver):
#     right = driver.find_element_by_css_selector("div._aaqg._aaqh")
#     right.click()
#     time.sleep(2)

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')        # Head-less 설정
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# # driver = webdriver.Chrome('chromedriver', options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

srcUrls = pd.read_csv("video_pageurl.csv")['url'].tolist()

data = list()
for index, url in enumerate(srcUrls):
    response = requests.get(url)
    lg.info(f"{index}th url get successful")
    data.append(getSource(response.content))
    
    # if index == 300:
    #     break
    



results_df = pd.DataFrame(data)
# print(results_df)
# results_df.columns = ['v']
results_df.to_csv('video_srcurl_utf8.csv', index=False)
results_df.to_csv('video_srcurl_cp949.csv', index=False, encoding='cp949')


# content = getUrlList(driver)

# lg.debug(content)

# https://www.fss.or.kr

