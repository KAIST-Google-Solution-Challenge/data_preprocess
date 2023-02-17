from bs4 import BeautifulSoup
import re
import pdb
import requests
import pandas as pd


from logger import getLogger

# 로그 생성
lg = getLogger()

def getSource(pageSource: str):

    # pdb.set_trace()
    html = pageSource
    soup = BeautifulSoup(html, "lxml")
    # soup = BeautifulSoup(r.content,"html.parser")
    
    data = list()

    try:
        # content = soup.select('.bd-list tbody')[0].text
        sourcePocket = soup.select('#content .bd-view .dbdata')
        videoSource = sourcePocket[0].select_one('video')['src']
        lg.warning(videoSource)
        data.append('https://www.fss.or.kr/'+videoSource)
        # pdb.set_trace()
        scriptSource = sourcePocket[0].select('div p')
        if len(scriptSource) == 0 or (len(scriptSource) == 1 and scriptSource[0].text == ''):
            lg.error('No Script Source')
            data.append("")
        else:
            # lg.warning(scriptSource[0].text)
            for p in scriptSource:
                if not p.text.isspace():
                    data.append(p.text)
            
        
    except Exception as e:
        lg.error(f"error: {e}")
        
    return data

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

srcUrls = pd.read_csv("audio_pageurl.csv")['url'].tolist()

data = list()
for index, url in enumerate(srcUrls):
    response = requests.get(url)
    lg.info(f"{index}th url get successful")
    data.append(getSource(response.content))
    
    # if index == 300:
    #     break
    



resultsDf = pd.DataFrame(data)
# print(resultsDf)
# resultsDf.columns = ['videosource_url', 'transcript']
resultsDf.to_csv('audio_srcurl_utf8.csv', index=False)
resultsDf.to_csv('audio_srcurl_cp949.csv', index=False, encoding='cp949')

dataWithTranscripts = data.loc[pd.notna(data['1']), '1':]
dataWithoutTranscripts = data.loc[pd.isna(data['1']), '0']

dataWithTranscripts.to_csv('audio_srcurl_transcripts.csv', index=False, encoding='utf-8')

dataWithoutTranscripts.to_csv('audio_srcurl_noscript.csv', index=False, encoding='utf-8')


# content = getUrlList(driver)

# lg.debug(content)

# https://www.fss.or.kr

