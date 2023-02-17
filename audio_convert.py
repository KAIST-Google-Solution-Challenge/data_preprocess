import os
from logger import getLogger
from moviepy.editor import *
from pydub import AudioSegment

lg = getLogger()

def convertAudio(source, sourceConverted):
    try:
        # sound = AudioSegment.from_mp3(source)
        sound = AudioSegment.from_file(source)
        sound.export(sourceConverted, format="wav")

        lg.debug("Converted mp3 to wav")

    except Exception as e:
        lg.error(e)


sourcePath = 'audios/'
savePath = 'audios_converted/'

srcList = os.listdir(sourcePath)

for index, source in enumerate(srcList):
    if source.find('.mp3') != -1:
        lg.warning(f'Source {index}: {source}')
        sourceConverted = savePath + source[:-4] + '.wav'
        source = sourcePath + source

        convertAudio(source, sourceConverted)
        lg.warning(f'successfully converted')

