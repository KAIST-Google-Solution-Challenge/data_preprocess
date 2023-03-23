# Google-Solution-Challenge Data Preprocessing

## Prerequisite

### Development Environment

`Python` version `3.8`

### Dependencies

You need to download following manually or use `docker`.

[`ffmpeg: 5.1.2`](https://ffmpeg.org/download.html)

### Google Cloud Storage Authentication

To access `Google Cloud Storage Bucket` and  [`Google Cloud Speech To Text`](https://cloud.google.com/speech-to-text/docs/libraries?hl=ko), 

1. Install cloud CLI following  [`This Link`](https://cloud.google.com/sdk/docs/install)
2. Set up default credential following [`This Link`](https://cloud.google.com/docs/authentication/provide-credentials-adc).
3. Install `Cloud Storage Client Library` (python in this case) following  [`This Link`](https://cloud.google.com/storage/docs/reference/libraries#python).

### .env

```
# GCLOUD Config
GCLOUD_PROJECT_NAME = {your-project-name}
GCLOUD_STORAGE_BUCKET = {your-bucket-name}
```

### Run

1. We should web-scrape the Audio Files’ Urls from  [`Financial Supervisory Service of Korea`](https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691).`

The Code below crawls through Financial Supervisory Service of Korea website, and collects the Audio Files’ Urls from the website and downloads them, and transforms them into suitable form. Those data will be used as voicephishing-positive train sets.
You should type following commands in order in the terminal.

```
python 1_audio_pageurl_collect.py
```
```
python 2_audio_srcurl_collect.py
```
```
python 3_audio_src_download.py
```
```
python 4_audio_convert.py
```

2. We should web-scrape the Video Files’ Urls from  [`Financial Supervisory Service of Korea`](https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691).

The Code below crawls through Financial Supervisory Service of Korea website, and collects the Video Files’ Urls from the website and downloads them, and trims/transforms them into suitable form. Those data will be used as voicephishing-positive train sets.
You should type following commands in order in the terminal.

```
python 5_video_pageurl_collect.py
```
```
python 6_video_srcurl_collect.py
```
```
python 7_video_src_download.py
```
```
python 8_video_trim_src.py
```
```
python 9_video_convert.py
```

3. We should call speech to text api call from  [`Google Cloud Speech To Text`](https://cloud.google.com/speech-to-text/docs/libraries?hl=ko) following  [`This Link`](https://cloud.google.com/speech-to-text/docs/reference/rest/v1/speech/longrunningrecognize).
You should type following command in the terminal.

```
python 10_speech_to_text.py
```

4. We should collect the voicephishing-negative train sets.

They can be achieved from [`National Institute of Korean Language`](https://corpus.korean.go.kr/request/reausetMain.do#none) .

The data is in form of each ‘corpus’es in json form, so we should tokenize and reconstruct them into list of sentences.
You should type following command in the terminal.

```
python 11_neg_dialogues_tokenize.py
```

# Result : Train Dataset

You can check the train data obtained by the procedure above in the 'final data' folder.

### negative_data_cp949.csv

This file contains the data achieved from [`National Institute of Korean Language`](https://corpus.korean.go.kr/request/reausetMain.do#none).

You can retrieve them by registering and making a reception in the website.

These data are used as negative trainsets for voicephishing classification task, and fed into pretrained koBERT model when fine-tuning the model.

### negative_data_utf8.csv

This file’s content is identical to negative_data_cp929.csv, but written in ***utf8*** encoding format.

### positive_data_cp949.csv

This file contains the data achieved from  [`Financial Supervisory Service of Korea`](https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691).

The data are achieved by crawling through the website and download the audio sources.

These data are used as positive trainsets for voicephishing classification task, and fed into pretrained koBERT model when fine-tuning the model.

### positive_data_utf8.csv

This file’s content is identical to positive_data_cp929.csv, but written in ***utf8*** encoding format.

## Format

The files in the repository are written in ***cp949*** encoding format or ***utf8*** encoding format.

You can use any of them.

If you are trying to open the data with ***plain text editor*** or ***vscode***, using ***negative_data_utf8.csv*** and ***positive_data_utf8.csv*** is recommended.

If you are trying to open the data with ***Microsoft Excel***, then using ***negative_data_cp949.csv*** and ***positive_data_cp949.csv*** is recommended.

(***Caution*** : There might be a problem opening cp949 encoded file with ***Mac OS Excel***, so be aware of it.)