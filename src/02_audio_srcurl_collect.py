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
        sourcePocket = soup.select('#content .bd-view .dbdata')
        videoSource = sourcePocket[0].select_one('video')['src']
        lg.warning(videoSource)
        data.append('https://www.fss.or.kr/'+videoSource)
        scriptSource = sourcePocket[0].select('div p')
        if len(scriptSource) == 0 or (len(scriptSource) == 1 and scriptSource[0].text == ''):
            lg.error('No Script Source')
            data.append("")
        else:
            for p in scriptSource:
                if not p.text.isspace():
                    data.append(p.text)
            
        
    except Exception as e:
        lg.error(f"error: {e}")
        
    return data

srcUrls = pd.read_csv("audio_pageurl.csv")['url'].tolist()

data = list()
for index, url in enumerate(srcUrls):
    response = requests.get(url)
    lg.info(f"{index}th url get successful")
    data.append(getSource(response.content))


resultsDf = pd.DataFrame(data)

resultsDf.to_csv('audio_srcurl_utf8.csv', index=False)
resultsDf.to_csv('audio_srcurl_cp949.csv', index=False, encoding='cp949')

dataWithTranscripts = data.loc[pd.notna(data['1']), '1':]
dataWithoutTranscripts = data.loc[pd.isna(data['1']), '0']

dataWithTranscripts.to_csv('audio_srcurl_withcripts.csv', index=False, encoding='utf-8')

dataWithoutTranscripts.to_csv('audio_srcurl_noscript.csv', index=False, encoding='utf-8')