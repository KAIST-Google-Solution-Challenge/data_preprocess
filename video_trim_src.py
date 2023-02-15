import os
import librosa
from logger import getLogger
import soundfile as sf
import numpy as np

lg = getLogger()

def trim_audio_data(source, source_trimmed):
    try:
        # sr = librosa.get_samplerate(source)

        start_trim_sec = 10
        end_trim_sec = 5
        y, sr = librosa.load(source, sr=None)

        ny = y[sr*start_trim_sec: -sr*end_trim_sec]

        # librosa.output.write_wav(source_trimmed+'_tr.mp3', ny, sr)
        
        sf.write(source_trimmed+'_tr.wav', ny, sr, 'PCM_16')

        lg.debug('Trimmed audio data')

    except Exception as e:
        lg.error(e)


source_path = 'videos_converted/'
save_path = 'videos_trimmed/'

src_list = os.listdir(source_path)

for source in src_list:
    if source.find('.wav') != -1:
        source_trimmed = save_path + source[:-4]
        source = source_path + source

        trim_audio_data(source, source_trimmed)