# import wave
# import contextlib
# import os


# files = os.listdir('./videos')
# # for file in files:
# #     if not file.endswith('.wav'):
# #         os.rename('./videos/'+file, './videos/'+file.replace('wav','.wav'))

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

lg = getLogger()

def trim_audio_data(source, source_trimmed):
    # try:
        # sr = librosa.get_samplerate(source)

    sec1 = 10
    sec2 = 5

    y, sr = librosa.load(source, sr=None)
    
    lg.debug(y)

    ny = y[sr*sec1: -sr*sec2]
    
    lg.info(ny)

    # librosa.output.write_wav(source_trimmed+'_tr.mp3', ny, sr)
    sf.write(source_trimmed+'_tr.wav', ny, sr, 'PCM_16')

    
    lg.debug('Trimmed audio data')

    # except Exception as e:
    #     lg.error(e)


source_path = 'videos_converted/'
save_path = 'videos_trimmed/'

# audio_path = save_path + '/audio'
# save_path = save_path + '/save'

src_list = os.listdir(source_path)

for source in src_list:
    if source.find('.wav') != -1:
        source_trimmed = save_path + source[:-4]
        source = source_path + source

        trim_audio_data(source, source_trimmed)