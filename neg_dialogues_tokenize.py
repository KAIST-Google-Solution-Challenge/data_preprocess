import json
import os
import pandas as pd
from logger import getLogger

lg = getLogger()

def concatenateCorpuses(corpuses):
    completeSentence = ''
    for index, corpus in enumerate(corpuses):
        if index is not len(corpuses): completeSentence += f'{corpus} '
        else: completeSentence += corpus
    return completeSentence


def corpusesToDialogue(filePath):
    with open(filePath, 'r', encoding='utf8') as file:
        jsonObject = json.load(file)

    # print(jsonObject['document'])
    # print(jsonObject)
    document = jsonObject['document'][0]


    corpusList = list()

    currentSpeaker = 'SD2000001'
    oneSpeech = list()
    for corpusJson in document['utterance']:
        # corpusList.append(corpusJson)
        if corpusJson['speaker_id'] != currentSpeaker:
            corpusList.append(concatenateCorpuses(oneSpeech))
            oneSpeech = [corpusJson['form']]
            currentSpeaker = corpusJson['speaker_id']
        else:
            oneSpeech.append(corpusJson['form'])
    corpusList.append(concatenateCorpuses(oneSpeech))

    return corpusList

def corpusesToSentences(filePath):
    with open(filePath, 'r', encoding='utf8') as file:
        jsonObject = json.load(file)

    # print(jsonObject['document'])
    # print(jsonObject)
    document = jsonObject['document'][0]


    corpusList = list()

    currentSpeaker = 'SD2000001'
    oneSpeech = list()
    currentCorpus = ''
    for corpusJson in document['utterance']:
        # corpusList.append(corpusJson)
        if corpusJson['speaker_id'] != currentSpeaker or currentCorpus.endswith('?') or currentCorpus.endswith('!') or currentCorpus.endswith('.'):
            corpusList.append(concatenateCorpuses(oneSpeech))
            oneSpeech = [corpusJson['form']]
            currentSpeaker = corpusJson['speaker_id']
        else:
            oneSpeech.append(corpusJson['form'])
        currentCorpus = corpusJson['form']
    corpusList.append(concatenateCorpuses(oneSpeech))

    return corpusList


dialogues = list()

directoryPath = 'NIKL_DIALOGUE_2020_v1.3'

jsonFiles = os.listdir(directoryPath)
for fileName in jsonFiles:
    if not fileName.endswith('.json'):
        continue
    filePath = f'{directoryPath}/{fileName}'
    dialogue = corpusesToSentences(filePath)
    dialogues.append(dialogue)
    

dialoguesDataFrame = pd.DataFrame(dialogues)
dialoguesDataFrame.to_csv('final_data/negative_data.csv', index = False)
    
    

# # print(corpusesToDialogue(filePath))
# for speech in corpusesToSentences(filePath):
#     # lg.debug(speech)
#     print(speech)