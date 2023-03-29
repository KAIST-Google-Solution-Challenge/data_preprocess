from bs4 import BeautifulSoup
import requests
import pandas as pd

from logger import getLogger

# 로그 생성
lg = getLogger()

def getSearchUrl(index: int):
    url = f"https://www.fss.or.kr/fss/bbs/B0000203/list.do?menuNo=200686&bbsId=&cl1Cd=&pageIndex={index}&sdate=&edate=&searchCnd=1&searchWrd="
    
    lg.debug(f"fetched url: {url}")
    return url

def getUrlList(pageSource: str):
    
    html = pageSource
    soup = BeautifulSoup(html, "lxml")
    # print(f'\033[93m after soup \033[0m')
    
    srcUrls = list()

    try:
        table = soup.select('.bd-list-thumb-a ul li')
        lg.debug(f"table content: \n {table}")
        for li in table:
            srcUrl = li.select_one('a')["href"]
            srcUrls.append('https://www.fss.or.kr'+srcUrl)
            
    except Exception as e:
        lg.error(f"error: {e}")
        
    return srcUrls

srcUrls = list()

for index in range(1, 11):
    response = requests.get(getSearchUrl(index))
    lg.info(f"{index}th driver get successful")
    srcUrls += getUrlList(response.content)



resultsDf = pd.DataFrame(srcUrls)
resultsDf.columns = ['url']
resultsDf.to_csv('video_pageurl.csv', index=False)