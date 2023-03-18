import os
from logger import getLogger
from moviepy.editor import *

lg = getLogger()

def convert_video(source, sourceConverted):
    try:
        audClip = AudioFileClip(source)
        audClip.write_audiofile(sourceConverted + '.wav')
        lg.debug('Trimmed audio data')
    except Exception as e:
        lg.error(e)


sourcePath = 'videos/'
savePath = 'videos_converted/'

src_list = os.listdir(sourcePath)

for index, source in enumerate(src_list):
    if source.find('.mp4') != -1:
        sourceConverted = savePath + source[:-4]
        source = sourcePath + source

        convert_video(source, sourceConverted)
    lg.debug(f'successfully converted {index}th video')
