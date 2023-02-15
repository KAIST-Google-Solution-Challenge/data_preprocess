import os
from logger import getLogger
from moviepy.editor import *

lg = getLogger()

def convert_video(source, source_converted):
    try:
        audClip = AudioFileClip(source)
        audClip.write_audiofile(source_converted + '.wav')
        lg.debug('Trimmed audio data')
    except Exception as e:
        lg.error(e)


source_path = 'videos/'
save_path = 'videos_converted/'

src_list = os.listdir(source_path)

for index, source in enumerate(src_list):
    if source.find('.mp4') != -1:
        source_converted = save_path + source[:-4]
        source = source_path + source

        convert_video(source, source_converted)
    lg.debug(f'successfully converted {index}th video')

    