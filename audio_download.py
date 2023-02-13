from bs4 import BeautifulSoup
import re
import time
import logging
from colorlog import ColoredFormatter
import pdb
import requests
import pandas as pd

# 로그 생성
lg = logging.getLogger()
lg.handlers = []       # No duplicated handlers
lg.propagate = False   # workaround for duplicated logs in ipython

# 로그의 출력 기준 설정
lg.setLevel(logging.DEBUG)

# log 출력 형식
# formatter = logging.Formatter('\033[92m[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s\033[0m')
formatter = ColoredFormatter(
    # "%(log_color)s[%(asctime)s] %(message)s",
    '%(log_color)s [%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'blue',
        'INFO':     'white,bold',
        'INFOV':    'cyan,bold',
        'WARNING':  'yellow',
        'ERROR':    'red,bold',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
lg.addHandler(stream_handler)

import urllib.request
# ...

srcUrls = pd.read_csv('src_for_noscripts.csv')['0'].tolist()

for audioUrl in srcUrls:
    urllib.request.urlretrieve(audioUrl, f'audios/{audioUrl[55:61]}_{audioUrl[73:105]}.wav')



# def getSource(page_source: str):

#     # pdb.set_trace()
#     html = page_source
#     soup = BeautifulSoup(html, "lxml")
#     # soup = BeautifulSoup(r.content,"html.parser")
    
#     data = list()

#     try:
#         # content = soup.select('.bd-list tbody')[0].text
#         sourcePocket = soup.select('#content .bd-view .dbdata')
#         videoSource = sourcePocket[0].select_one('video')['src']
#         lg.warning(videoSource)
#         data.append('https://www.fss.or.kr/'+videoSource)
#         # pdb.set_trace()
#         scriptSource = sourcePocket[0].select('div p')
#         if len(scriptSource) == 0 or (len(scriptSource) == 1 and scriptSource[0].text == ''):
#             lg.error('No Script Source')
#             data.append("")
#         else:
#             # lg.warning(scriptSource[0].text)
#             for p in scriptSource:
#                 if not p.text.isspace():
#                     data.append(p.text)
            
        
#     except Exception as e:
#         lg.error(f"error: {e}")
        
#     return data

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

# srcUrls = pd.read_csv("voice_phishing_data_urls.csv")['url'].tolist()

# data = list()
# for index, url in enumerate(srcUrls):
#     response = requests.get(url)
#     lg.info(f"{index}th url get successful")
#     data.append(getSource(response.content))
    
#     # if index == 300:
#     #     break
    



# results_df = pd.DataFrame(data)
# # print(results_df)
# # results_df.columns = ['videosource_url', 'transcript']
# results_df.to_csv('videosource_and_transcript_utf8.csv', index=False)
# results_df.to_csv('videosource_and_transcript_cp949.csv', index=False, encoding='cp949')


# content = getUrlList(driver)

# lg.debug(content)

# https://www.fss.or.kr

