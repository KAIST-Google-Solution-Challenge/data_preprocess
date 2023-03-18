
# Imports the Google Cloud client library
from google.cloud import speech
import pandas as pd
from logger import getLogger
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_NAME = os.environ.get('GCLOUD_PROJECT_NAME')
BUCKET_NAME = os.environ.get('GCLOUD_BUCKET_NAME')


lg = getLogger()

# Below Function splits the given input string into tokens splitted by '?', '!', '.', to split into separate sentences
def tokenizeTexts(texts):
    qmarkSplitResult = list()
    for text in texts:
        if type(text) != str:
            break
        text = text.replace('"', '').strip()
        
        splitResult = text.split('?')
        for index in range(len(splitResult)):
            if index != len(splitResult) - 1:
                splitResult[index] = splitResult[index] + '?'
        qmarkSplitResult += splitResult


    dotSplitResult = list()
    for text in qmarkSplitResult:
        
        
        splitResult = text.split('.')
        for index in range(len(splitResult)):
            if index != len(splitResult) - 1:
                splitResult[index] = splitResult[index] + '.'
        dotSplitResult += splitResult


    emarkSplitResult = list()
    for text in dotSplitResult:
        
        splitResult = text.split('!')
        for index in range(len(splitResult)):
            if index != len(splitResult) - 1:
                splitResult[index] = splitResult[index] + '!'
        emarkSplitResult += splitResult

    results = list(filter(lambda x: x != '', emarkSplitResult))
    
    return results

#Given a source uri in the google cloud bucket, than makes an speech_to_text api call using the source audio file and returns the result string.
def sttRecognition(gcs_uri, client):
    # The name of the audio file to transcribe
    audio = speech.RecognitionAudio(uri=gcs_uri)
    try:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            # sample_rate_hertz=44100,
            language_code="ko-KR",
            enable_automatic_punctuation=True,
            audio_channel_count=1,
            model='latest_long'
        )
        # Detects speech in the audio file
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=2000)
    except Exception as e:
        lg.warning(f"error: {e}")
        lg.warning("switching audio_channel_count to 2")
        try:            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                # sample_rate_hertz=44100,
                language_code="ko-KR",
                enable_automatic_punctuation=True,
                audio_channel_count=2,
                model='latest_long'
            )
            # Detects speech in the audio file
            # response = client.recognize(config=config, audio=audio)
            operation = client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=2000)
        except Exception as e:
            lg.warning(f"error: {e}")
            lg.warning("switching to mono channel")
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                # sample_rate_hertz=44100,
                language_code="ko-KR",
                enable_automatic_punctuation=True,
                model='latest_long'
            )
            # Detects speech in the audio file
            # response = client.recognize(config=config, audio=audio)
            operation = client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=2000)
    transcripts = list()

    for result in response.results:
        # lg.info(result)
        transcript = result.alternatives[0].transcript
        # lg.debug(transcript)
        transcripts.append(transcript)
    return transcripts

from google.cloud import storage

storage_client = storage.Client(project=PROJECT_NAME)

# Instantiates a client
speech_client = speech.SpeechClient()

# lg.info(list(client.list_buckets(project='solution-challenge-kaist')))
files = list(storage_client.list_blobs(bucket_or_name=BUCKET_NAME, timeout=300))


# to get ready of stt_audios_utf8.csv and stt_videos_utf8.csv files are recommended.
sttAudios = pd.read_csv('stt_audios_utf8.csv').values.tolist()
sttVideos = pd.read_csv('stt_videos_utf8.csv').values.tolist()

# sttAudios = list()
# sttVideos = list()

# print(sttVideos)
# print(sttAudios)

import pdb

# for index in [129, 138, 148]:
#     file = files[index]
#     print(str(index) + " : ")
#     print(f"gs://{file.bucket.name}/{file.name}")

try:
    for index, file in enumerate(files):
        # if index not in [129, 138, 148]:
        #     lg.debug(f"skipping index {index}")
        #     continue
        lg.debug(f"{index}th file")
        # lg.debug(file.name)
        # lg.warning(file.bucket.name)
        
        # get saudio ource's google cloud uri path
        bucket = file.bucket.name
        path = file.name
        
        ## skipping files that aren't .wav files such as directory
        if not path.endswith(".wav"):
            lg.warning(f"{path} is not a wav file")
            continue
        gcs_uri = f"gs://{bucket}/{path}"
        lg.info(gcs_uri)
        
        # make an speech to text api call on the audio source.
        transcripts = sttRecognition(gcs_uri=gcs_uri, client=speech_client)
        
        # tokenize the stt result into list of separate sentences
        tokenizeResults = tokenizeTexts(transcripts)
        
        #save results
        if "video" in path:
            # sttVideos = sttVideos.append([[index, *tokenizeResults]], ignore_index=True)
            sttVideos.append([index, *tokenizeResults])

            dataVideos = pd.DataFrame(sttVideos)
            # sttVideos.to_csv('stt_videos_utf8.csv', index=False)
            dataVideos.to_csv('stt_videos_utf8.csv', index=False)
            dataVideos.to_csv('stt_videos_cp949.csv', index=False, encoding='cp949')
        else:
            lg.info([index, *tokenizeResults])
            # sttAudios = sttAudios.append([[float(index), *tokenizeResults]], ignore_index=True)
            sttAudios.append([index, *tokenizeResults])
            # sttAudios = sttAudios.append([tokenizeResults], ignore_index=True)
            dataAudios = pd.DataFrame(sttAudios)
            print(dataAudios)

            # sttAudios.to_csv('stt_audios_utf8.csv', index=False)
            dataAudios.to_csv('stt_audios_utf8.csv', index=False)
            dataAudios.to_csv('stt_audios_cp949.csv', index=False, encoding='cp949')
            # pdb.set_trace()
        lg.warning(tokenizeResults)
        lg.debug(sttAudios)
    lg.debug("successfully done!")
except Exception as e:
    lg.error(f"error occurred while trascribing {index}th file. \n path: {gcs_uri}")
    lg.error(e)
    lg.debug(sttVideos)
    lg.debug(sttAudios)
    sttVideos.to_csv('stt_videos_utf8.csv', index=False)
    sttVideos.to_csv('stt_videos_cp949.csv', index=False)
    sttAudios.to_csv('stt_audios_utf8.csv', index=False)
    sttAudios.to_csv('stt_audios_cp949.csv', index=False)
