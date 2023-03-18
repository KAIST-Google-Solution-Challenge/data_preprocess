
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

def tokenizeTexts(texts):
    qmarkSplitResult = list()
    # print(texts)
    for text in texts:
        # print(type(text))
        # print(text)
        if type(text) != str:
            break
        text = text.replace('"', '').strip()
        
        splitResult = text.split('?')
        for index in range(len(splitResult)):
            if index != len(splitResult) - 1:
                splitResult[index] = splitResult[index] + '?'
        qmarkSplitResult += splitResult
    # print(qmarkSplitResult)


    dotSplitResult = list()
    for text in qmarkSplitResult:
        
        
        splitResult = text.split('.')
        for index in range(len(splitResult)):
            if index != len(splitResult) - 1:
                splitResult[index] = splitResult[index] + '.'
        dotSplitResult += splitResult
    # print(dotSplitResult)


    emarkSplitResult = list()
    for text in dotSplitResult:
        
        splitResult = text.split('!')
        for index in range(len(splitResult)):
            if index != len(splitResult) - 1:
                splitResult[index] = splitResult[index] + '!'
        emarkSplitResult += splitResult
    # print(emarkSplitResult)

    results = list(filter(lambda x: x != '', emarkSplitResult))
    # print(results)
    
    return results


def sttRecognition(gcs_uri, client):
    # The name of the audio file to transcribe
    # gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
    # gcs_uri = "https://storage.cloud.google.com/voicephishing_detection_stt/videos/0_004930e55471bb08da29d56c3d4c858_tr.wav"

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
        # response = client.recognize(config=config, audio=audio)
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

storage_client = storage.Client(project='PROJECT_NAME')

# Instantiates a client
speech_client = speech.SpeechClient()

lg.debug("1")
# lg.info(list(client.list_buckets(project='solution-challenge-kaist')))
files = list(storage_client.list_blobs(bucket_or_name='BUCKET_NAME', timeout=300))

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
        if index not in [129, 138, 148]:
            lg.debug(f"skipping index {index}")
            continue
        lg.debug(f"{index}th file")
        # lg.debug(file.name)
        # lg.warning(file.bucket.name)
        bucket = file.bucket.name
        path = file.name
        if not path.endswith(".wav"):
            lg.warning(f"{path} is not a wav file")
            continue
        gcs_uri = f"gs://{bucket}/{path}"
        lg.info(gcs_uri)
        transcripts = sttRecognition(gcs_uri=gcs_uri, client=speech_client)
        tokenizeResults = tokenizeTexts(transcripts)
        if "video" in path:
            # sttVideos = sttVideos.append([[index, *tokenizeResults]], ignore_index=True)
            sttVideos.append([index, *tokenizeResults])

            dataVideos = pd.DataFrame(sttVideos)
            # sttVideos.to_csv('stt_videos_utf8.csv', index=False)
            dataVideos.to_csv('stt_videos_utf8.csv', index=False)
            # dataVideos.to_csv('stt_videos_cp949.csv', index=False, encoding='cp949')
        else:
            lg.info([index, *tokenizeResults])
            # sttAudios = sttAudios.append([[float(index), *tokenizeResults]], ignore_index=True)
            sttAudios.append([index, *tokenizeResults])
            # sttAudios = sttAudios.append([tokenizeResults], ignore_index=True)
            dataAudios = pd.DataFrame(sttAudios)
            print(dataAudios)

            # sttAudios.to_csv('stt_audios_utf8.csv', index=False)
            dataAudios.to_csv('stt_audios_utf8.csv', index=False)
            # dataAudios.to_csv('stt_audios_cp949.csv', index=False, encoding='cp949')
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
    sttAudios.to_csv('stt_audios_utf8.csv', index=False)
