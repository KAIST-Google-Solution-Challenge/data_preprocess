from bs4 import BeautifulSoup
import pdb
import requests
import pandas as pd

from logger import getlogger

# 로그 생성
lg = getlogger()

def getSearchUrl(index: int):
    # url = f"https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691&bbsId=&cl1Cd=&pageIndex={index}&sdate=&edate=&searchCnd=1&searchWrd="
    url = f"https://www.fss.or.kr/fss/bbs/B0000203/list.do?menuNo=200686&bbsId=&cl1Cd=&pageIndex={index}&sdate=&edate=&searchCnd=1&searchWrd="
    
    lg.debug(f"fetched url: {url}")
    return url

def getUrlList(pageSource: str):

    # pdb.set_trace()
    # print(f'\033[93m after start \033[0m')
    html = pageSource
    # print(f'\033[93m after html pageSource \033[0m')
    # print(html[:100])
    soup = BeautifulSoup(html, "lxml")
    # soup = BeautifulSoup(r.content,"html.parser")
    print(f'\033[93m after soup \033[0m')
    
    srcUrls = list()

    try:
        # content = soup.select('.bd-list tbody')[0].text
        table = soup.select('.bd-list-thumb-a ul li')
        lg.debug(f"table content: {table}")
        for li in table:
            # lg.warning("1")
            srcUrl = li.select_one('a')["href"]
            srcUrls.append('https://www.fss.or.kr'+srcUrl)
            
            # lg.warning("2")
            # lg.debug(f"srcUrl: {srcUrl}")
            # lg.warning("3")
        # print(f'\033[93m after table \033[0m')
    except Exception as e:
        lg.error(f"error: {e}")
        
    return srcUrls

srcUrls = list()

for index in range(1, 11):
    response = requests.get(getSearchUrl(index))
    lg.info(f"{index}th driver get successful")
    # time.sleep(5)
    srcUrls += getUrlList(response.content)



resultsDf = pd.DataFrame(srcUrls)
# print(resultsDf)
resultsDf.columns = ['url']
resultsDf.to_csv('video_urls.csv', index=False)