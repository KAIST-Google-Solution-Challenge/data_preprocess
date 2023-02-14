# import wave
# import contextlib
# import os


# files = os.listdir('./audios')
# # for file in files:
# #     if not file.endswith('.wav'):
# #         os.rename('./audios/'+file, './audios/'+file.replace('wav','.wav'))

# fname = files[0]
# with contextlib.closing(wave.open(fname,'r')) as f:
#     frames = f.getnframes()
#     rate = f.getframerate()
#     duration = frames / float(rate)
#     print(duration)

import os
import librosa
from logger import getLogger
import soundfile as sf
import numpy as np
from moviepy.editor import *

lg = getLogger()

def convert_video(source, source_converted):
    # try:
        # sr = librosa.get_samplerate(source)
    audClip = AudioFileClip(source)
    audClip.write_audiofile(source_converted + '.wav')

    # lg.debug('Trimmed audio data')

    # except Exception as e:
    #     lg.error(e)


source_path = 'videos/'
save_path = 'videos_converted/'

# audio_path = save_path + '/audio'
# save_path = save_path + '/save'

src_list = os.listdir(source_path)

for index, source in enumerate(src_list):
    if source.find('.mp4') != -1:
        source_converted = save_path + source[:-4]
        source = source_path + source

        convert_video(source, source_converted)
    lg.debug(f'successfully converted {index}th video')

    