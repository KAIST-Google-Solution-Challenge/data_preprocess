from bs4 import BeautifulSoup
import requests
import pandas as pd
from logger import getLogger

# 로그 생성
lg = getLogger()




def getSearchUrl(index: int, type: int, menuNo: int):
    # url = f"https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691&bbsId=&cl1Cd=&pageIndex={index}&sdate=&edate=&searchCnd=1&searchWrd="
    url = f"https://www.fss.or.kr/fss/bbs/B0000{type}/list.do?menuNo={menuNo}&bbsId=&cl1Cd=&pageIndex={index}&sdate=&edate=&searchCnd=1&searchWrd="
    lg.debug(f"fetched url: {url}")
    return url


def getUrlList(pageSource: str):

    html = pageSource
    
    soup = BeautifulSoup(html, "lxml")
    
    print(f'\033[93m after soup \033[0m')
    
    srcPageUrls = list()

    try:
        
        table = soup.select('.bd-list tbody tr')
        lg.debug(f"table content: {table}")
        for tr in table:
            
            srcUrl = tr.select_one('td:nth-child(2) a')["href"]
            srcPageUrls.append('https://www.fss.or.kr'+srcUrl)
            
    except Exception as e:
        lg.error(f"error: {e}")
        
    return srcPageUrls


# srcUrls = pd.read_csv("audio_pageurl.csv")['url'].tolist()
srcPageUrls = list()
for index in range(1, 19):
    response = requests.get(getSearchUrl(index, 206, 200690))
    lg.info(f"{index}th driver get successful")
    srcPageUrls += getUrlList(response.content)

for index in range(1, 23):
    response = requests.get(getSearchUrl(index, 207, 200691))
    lg.info(f"{index}th driver get successful")
    srcPageUrls += getUrlList(response.content)



resultsDf = pd.DataFrame(srcPageUrls)
resultsDf.columns = ['url']
resultsDf.to_csv('audio_pageurl.csv', index=False)