import os
from logger import getLogger
from moviepy.editor import *
from pydub import AudioSegment

lg = getLogger()

def convert_audio(source, source_converted):
    try:
        # sound = AudioSegment.from_mp3(source)
        sound = AudioSegment.from_file(source)
        sound.export(source_converted, format="wav")

        lg.debug("Converted mp3 to wav")

    except Exception as e:
        lg.error(e)


source_path = 'audios/'
save_path = 'audios_converted/'

src_list = os.listdir(source_path)

for index, source in enumerate(src_list):
    if source.find('.mp3') != -1:
        lg.warning(f'Source {index}: {source}')
        source_converted = save_path + source[:-4] + '.wav'
        source = source_path + source

        convert_audio(source, source_converted)
        lg.warning(f'successfully converted')

