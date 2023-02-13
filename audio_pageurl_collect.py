from bs4 import BeautifulSoup
import pdb
import requests
import pandas as pd
from logger import getLogger

# 로그 생성
lg = getLogger()




def get_search_url(index: int):
    # url = f"https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691&bbsId=&cl1Cd=&pageIndex={index}&sdate=&edate=&searchCnd=1&searchWrd="
    url = f"https://www.fss.or.kr/fss/bbs/B0000206/list.do?menuNo=200690&bbsId=&cl1Cd=&pageIndex={index}&sdate=&edate=&searchCnd=1&searchWrd="
    lg.debug(f"fetched url: {url}")
    return url

# def select_first(driver):
#     first = driver.find_elements_by_css_selector("div._aagw")[0]
#     first.click()
#     time.sleep(3)

def getUrlList(page_source: str):

    # pdb.set_trace()
    # print(f'\033[93m after start \033[0m')
    html = page_source
    # print(f'\033[93m after html page_source \033[0m')
    # print(html[:100])
    soup = BeautifulSoup(html, "lxml")
    # soup = BeautifulSoup(r.content,"html.parser")
    print(f'\033[93m after soup \033[0m')
    
    srcUrls = list()

    try:
        # content = soup.select('.bd-list tbody')[0].text
        table = soup.select('.bd-list tbody tr')
        lg.debug(f"table content: {table}")
        for tr in table:
            # lg.warning("1")
            srcUrl = tr.select_one('td:nth-child(2) a')["href"]
            srcUrls.append('https://www.fss.or.kr'+srcUrl)
            
            # lg.warning("2")
            # lg.debug(f"srcUrl: {srcUrl}")
            # lg.warning("3")
        # print(f'\033[93m after table \033[0m')
    except Exception as e:
        lg.error(f"error: {e}")
        
    return srcUrls

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


srcUrls = pd.read_csv("voice_phishing_data_urls.csv")['url'].tolist()
for index in range(1, 19):
    response = requests.get(get_search_url(index))
    lg.info(f"{index}th driver get successful")
    # time.sleep(5)
    srcUrls += getUrlList(response.content)



results_df = pd.DataFrame(srcUrls)
# print(results_df)
results_df.columns = ['url']
results_df.to_csv('audio_pageurl.csv', index=False)


# content = getUrlList(driver)

# logger.debug(content)



# * login mechanism for instagram login
# email = "abepje@naver.com"
# input_id = driver.find_elements_by_css_selector('input._aa4b._add6._ac4d')[0]
# input_id.clear()
# input_id.send_keys(email)

# password = "qkrWhd@34E"
# input_pw = driver.find_elements_by_css_selector('input._aa4b._add6._ac4d')[1]
# input_pw.clear()
# input_pw.send_keys(password)
# input_pw.submit()

# time.sleep(5)



# # word = input("검색어를 입력하세요 : ")
# word = "kingcharles"
# word = str(word)
# url = get_search_url(word)

# driver.get(url)
# time.sleep(10)

# select_first(driver)

# results = []

# target_number = 10
# for i in range(target_number):
#     # data = getUrlList(driver)
#     try:
#         data = getUrlList(driver)
#         print(f'\033[92m {data} \033[0m')
#         results.append(data)
#         move_next(driver)
#     except Exception as err:
#         time.sleep(2)
#         print(f'\033[91m ERROR!!! {err}\033[0m')
#         move_next(driver)
#     time.sleep(3)
# print(results[:2])

# import pandas as pd
# from datetime import datetime

# date = datetime.today().strftime('%Y-%m-%d')

# results_df = pd.DataFrame(results)
# print(results_df)
# results_df.columns = ['content', 'date', 'like', 'place', 'tags']
# results_df.to_csv(date + '_about' + word + ' insta crawling.csv')