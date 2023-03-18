import pandas as pd
from logger import getLogger

# 로그 생성
lg = getLogger()


import urllib.request


srcUrls = pd.read_csv('audio_srcurl_noscript.csv')['0'].tolist()

for audioUrl in srcUrls:
    urllib.request.urlretrieve(audioUrl, f'audios/{audioUrl[55:61]}_{audioUrl[73:105]}.mp3')
