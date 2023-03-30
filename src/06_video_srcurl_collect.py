from bs4 import BeautifulSoup
import requests
import pandas as pd
from logger import getLogger

# 로그 생성
lg = getLogger()

def getSource(pageSource: str):

    html = pageSource
    soup = BeautifulSoup(html, "lxml")
    
    data = list()

    try:
        videoSource = soup.select_one('.file-list dd a')["href"]
        lg.warning(videoSource)
        data.append('https://www.fss.or.kr'+videoSource)
            
        
    except Exception as e:
        lg.error(f"error: {e}")
        
    return data[0]

srcUrls = pd.read_csv("video_pageurl.csv")['url'].tolist()

data = list()
for index, url in enumerate(srcUrls):
    response = requests.get(url)
    lg.info(f"{index}th url get successful")
    data.append(getSource(response.content))
    

resultsDf = pd.DataFrame(data)
resultsDf.to_csv('video_srcurl_utf8.csv', index=False)
resultsDf.to_csv('video_srcurl_cp949.csv', index=False, encoding='cp949')
