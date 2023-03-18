import pandas as pd
from logger import getLogger

lg = getLogger()

import urllib.request

srcUrls = pd.read_csv('video_srcurl_utf8.csv')['0'].tolist()

for index, videoUrl in enumerate(srcUrls):

    urllib.request.urlretrieve(videoUrl, f'videos/{videoUrl[109:140]}.mp4')
    lg.debug(f'Downloaded: {index}th video')