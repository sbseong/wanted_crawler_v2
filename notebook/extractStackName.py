import csv, re
from collections import Counter
from extractJobName import changeJN

def stackName(stackList):

    total, jn = [], []

    for idx, rowData in enumerate(stackList):
        if idx == 0: continue
        
        total.extend(rowData[-1].split('\n'))

        insertData = re.split('[],(,[, -, _, /, )]', rowData[1])

        jobName = changeJN(insertData)
        if jobName == 'DE': DE.extend(rowData[-1].split('\n'))
        elif jobName == 'DA': DA.extend(rowData[-1].split('\n'))
        elif jobName == 'DS': DS.extend(rowData[-1].split('\n'))

    return [total, jobName, jn]


if __name__ == "__main__":

    stackList, DE, DA, DS = [], [], [], []

    with open('crawlingData/2023-01-24 20:19:04_wanted_crawling.csv', 'r') as file:
        data = csv.reader(file)

        for idx, rowData in enumerate(data):
            if idx == 0: continue
            stackList.extend(rowData[-1].split('\n'))

            insertData = re.split('[],(,[, -, _, /, )]', rowData[1])

            jobName = changeJN(insertData)
            if jobName == 'DE': DE.extend(rowData[-1].split('\n'))
            elif jobName == 'DA': DA.extend(rowData[-1].split('\n'))
            elif jobName == 'DS': DS.extend(rowData[-1].split('\n'))
            # stackList.append(rowData[-1])
            # print(rowData)
            
        #     if idx == 0: ...
        #     # elif idx == 2: break
        #     else:
        #         insertData = re.split('[],(,[, -, _, /, )]', rowData[1])
        #         # print(insertData)
        #         testList.append(insertData)
    
    print(Counter(stackList))
    print(Counter(DE))
    print(Counter(DS))
    print(Counter(DA))