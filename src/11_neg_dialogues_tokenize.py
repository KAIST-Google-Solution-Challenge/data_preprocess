import json
import os
import pandas as pd
from logger import getLogger

lg = getLogger()

# concatenate corpuses into one.
def concatenateCorpuses(corpuses):
    completeSentence = ''
    for index, corpus in enumerate(corpuses):
        if index is not len(corpuses): completeSentence += f'{corpus} '
        else: completeSentence += corpus
    return completeSentence

# a list of multiple speeches. One element can be composed of multiple sentences, but they must be contiguous and spoken by one person.
def corpusesToDialogue(filePath):
    with open(filePath, 'r', encoding='utf8') as file:
        jsonObject = json.load(file)

    document = jsonObject['document'][0]


    corpusList = list()

    currentSpeaker = 'SD2000001'
    oneSpeech = list()
    for corpusJson in document['utterance']:
        if corpusJson['speaker_id'] != currentSpeaker:
            corpusList.append(concatenateCorpuses(oneSpeech))
            oneSpeech = [corpusJson['form']]
            currentSpeaker = corpusJson['speaker_id']
        else:
            oneSpeech.append(corpusJson['form'])
    corpusList.append(concatenateCorpuses(oneSpeech))

    return corpusList

# make a list of sentences. each element is a sentence.
def corpusesToSentences(filePath):
    with open(filePath, 'r', encoding='utf8') as file:
        jsonObject = json.load(file)

    document = jsonObject['document'][0]


    corpusList = list()

    currentSpeaker = 'SD2000001'
    oneSpeech = list()
    currentCorpus = ''
    for corpusJson in document['utterance']:
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
for index, fileName in enumerate(jsonFiles):
    if not fileName.endswith('.json'):
        continue
    filePath = f'{directoryPath}/{fileName}'
    dialogue = corpusesToSentences(filePath)
    dialogues.append(dialogue)
    print(f"{index}th file handled.")


dialoguesDataFrame = pd.DataFrame(dialogues)
dialoguesDataFrame = dialoguesDataFrame.applymap(lambda x: x.replace('\xa0','').replace('\xa9','') if type(x) is type('str') else x)
dialoguesDataFrame.to_csv('final_data/negative_data_utf8.csv', index = False)
dialoguesDataFrame.to_csv('final_data/negative_data_cp949.csv', index = False, encoding = 'cp949')