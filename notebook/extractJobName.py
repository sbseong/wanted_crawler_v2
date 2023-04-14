import pandas as pd
import csv, re
from collections import Counter

DE = ['Data', '데이터', '빅데이터', '엔지니어', 'Engineer', '데이터엔지니어', 'MLOps']
DA = ['Data', '데이터', '분석가', 'Analyst', '데이터분석가', '애널리스트']
DS = ['AI', '인공지능', '과학자', '연구원', '엔지니어', 'Researcher', 'Scientist', 'ML', 'DL', '연구자', '머신러닝', '딥러닝', 'Machine', 'Deep']

def changeJN(wordList):

    de, da, ds = 0, 0, 0

    for idx in range(len(wordList)):
        if wordList[idx] in DE:
            if wordList[idx] in ['데이터엔지니어', 'DataEngineer']: de += 2
            else: de += 1
        elif wordList[idx] in DA:
            if wordList[idx] in ['데이터분석가', '애널리스트', '분석가', 'Analyst']: da += 2
            else: da += 1
        elif wordList[idx] in DS:
            if wordList[idx] in ['인공지능', 'ML', 'DL', 'Machine', 'Deep']: ds += 2
            else: ds += 1

    if de >= 2: return 'DE'
    elif da >= 2: return 'DA'
    elif ds >= 2: return 'DS'


if __name__ == "__main__":

    # testList, result = [], []

    # with open('crawlingData/2023-01-24 20:19:04_wanted_crawling.csv', 'r') as file:
    #     data = csv.reader(file)

    #     for idx, rowData in enumerate(data):
    #         if idx == 0: ...
    #         # elif idx == 2: break
    #         else:
    #             insertData = re.split('[],(,[, -, _, /, )]', rowData[1])
    #             # print(insertData)
    #             testList.append(insertData)
    
    # for rowData in testList:
    #     a = changeJN(rowData)
    #     result.append(a)
    
    # print(Counter(result))
    
    # word = 'AML 자금세탁방지 담당자'
    import os
    word = 'MLB/디스커버리 의류 브랜드 본사 IT 백엔드 개발자(ERP, SCM 시스템 Back-end 개발 및 운영) MachineLearning'
    word = re.split('[],(,[, -, _, /, )]', word)
    a = [i.lower() for i in word]
    print(a)
    print(['machinelearning'] in a)