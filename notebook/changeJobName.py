import pandas as pd
import csv, re, json
from collections import Counter
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

DE = ['Data', '데이터', '빅데이터', '엔지니어', 'Engineer', '데이터엔지니어', 'MLOps']
DA = ['Data', '데이터', '분석가', 'Analyst', '데이터분석가', '애널리스트']
DS = ['AI', '인공지능', '과학자', '연구원', '엔지니어', 'Researcher', 'Scientist', 'ML', 'DL', '연구자', '머신러닝', '딥러닝', 'Machine', 'Deep']

# # test = "데이터 엔지니어(신입가능)"
# test = "인공지능연구원"
# new = re.split('[],(,[, -, _, /, )]', test)
# if t[0] in DE: print('ok')

def changeJN(wordList):

    sumJob = []
    month = '1월'
    testDict = {f'{month}': {
        'DA': '',
        'DE': '',
        'DS': ''
    }}

    for rowData in wordList:

        de, da, ds = 0, 0, 0

        for idx in range(len(rowData)):
            if rowData[idx] in DE:
                if rowData[idx] in ['데이터엔지니어', 'DataEngineer']: de += 2
                else: de += 1
            elif rowData[idx] in DA:
                if rowData[idx] in ['데이터분석가', '애널리스트', '분석가', 'Analyst']: da += 2
                else: da += 1
            elif rowData[idx] in DS:
                if rowData[idx] in ['인공지능', 'ML', 'DL', 'Machine', 'Deep']: ds += 2
                else: ds += 1

        if de >= 2: sumJob.append('DE')
        elif da >= 2: sumJob.append('DA')
        elif ds >= 2: sumJob.append('DS')

    test = dict(Counter(sumJob))

    testDict[f'{month}']['DA'] = test['DA']
    testDict[f'{month}']['DE'] = test['DE']
    testDict[f'{month}']['DS'] = test['DS']
    print(testDict)

    with open('jd.json', 'w', encoding='UTF-8') as file:
        json.dump(testDict, file, indent='\t', ensure_ascii=False)
    
    # for i in test:
    #     job = test[f'{i}']
    #     testDict[month][job] = test[f'{i}']
    
    # print(testDict)


# def uploadGoogleDrive(jsonFile):

    # try :
    #     import argparse
    #     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    # except ImportError:
    #     flags = None

    # SCOPES = 'https://www.googleapis.com/auth/drive.file'
    # store = file.Storage('storage.json')
    # creds = store.get()

    # if not creds or creds.invalid:
    #     print("make new storage data file ")
    #     flow = client.flow_from_clientsecrets('client_secret_drive.json', SCOPES)
    #     creds = tools.run_flow(flow, store, flags) \
    #             if flags else tools.run(flow, store)

    # DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    # request_body = {'name': '업로드할 엑셀.xlsx'} # 업로드할 파일의 정보 정의
    # media = MediaFileUpload('업로드할 엑셀.xlsx') # 업로드할 파일
    # file = DRIVE.files().create(body=request_body,media_body=media).execute()
    # print("File ID :",file.get('id'))

    # try :
    #     import argparse
    #     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    # except ImportError:
    #     flags = None

    # SCOPES = 'https://www.googleapis.com/auth/drive.file'
    # store = file.Storage('storage.json')
    # creds = store.get()

    # if not creds or creds.invalid:
    #     print('make new storage data file')
    #     flow = client.flow_from_clientsecrets('/Users/taebeomkim/wanted_crawler_v2/credentials.json', SCOPES)
    #     creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)

    # service = build('drive', 'v3', http=creds.authorize(Http()))

    # folderId = '1lI3JjNqDseTHu66yl_yNcQbe7l5TkPqZ'
    # filePath = jsonFile

    # requestBody = {'name': filePath, 'parents': [folderId], 'uploadType': 'multipart'}
    # media = MediaFileUpload(filePath, mimetype=None)
    # fileInfo = service.files().create(body=requestBody, mediaBody=media, fields='id').execute()

    # print(fileInfo.get('id'))


if __name__ == "__main__":

    testList = []

    with open('crawlingData/2023-01-24 20:19:04_wanted_crawling.csv', 'r') as file:
        data = csv.reader(file)

        for idx, rowData in enumerate(data):
            if idx == 0: ...
            # elif idx == 2: break
            else:
                insertData = re.split('[],(,[, -, _, /, )]', rowData[1])
                # print(insertData)
                testList.append(insertData)
    changeJN(testList)
    # uploadGoogleDrive(test)
    # test = [['1', 'a']]
    # test1 = ['a', '3']

    # for rowData in test:
    #     for idx in range(len(rowData)):
    #         if rowData[idx] in test1: print(True)
    #         else: print(False)