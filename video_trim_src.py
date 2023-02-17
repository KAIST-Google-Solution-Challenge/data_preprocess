import os
import librosa
from logger import getLogger
import soundfile as sf
import numpy as np

lg = getLogger()

def trimAudioData(source, sourceTrimmed):
    try:
        # sr = librosa.get_samplerate(source)

        startTrimSec = 10
        endTrimSec = 5
        y, sr = librosa.load(source, sr=None)

        ny = y[sr*startTrimSec: -sr*endTrimSec]

        # librosa.output.write_wav(sourceTrimmed+'_tr.mp3', ny, sr)
        
        sf.write(sourceTrimmed+'_tr.wav', ny, sr, 'PCM_16')

        lg.debug('Trimmed audio data')

    except Exception as e:
        lg.error(e)


sourcePath = 'videos_converted/'
savePath = 'videos_trimmed/'

src_list = os.listdir(sourcePath)

for source in src_list:
    if source.find('.wav') != -1:
        sourceTrimmed = savePath + source[:-4]
        source = sourcePath + source

        trimAudioData(source, sourceTrimmed)