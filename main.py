"""
1. 입력받은 원티드 링크로 JD 검색 with.wantedCrawling.py
2. 직무만 따로 추출 with.extractJobName.py
3. 스택 분석을 위한 분류 with.extractStackName.py
"""

from jdLink import totalUrl
from webDriver import driver_start
from collections import Counter
import wantedCrawling as wc
import gspread, glob, csv, re, datetime, copy, time

def crawling(totalUrl, bool=True):

    driver = driver_start()

    countUrl = {
        'mle': '',
        'ds': '',
        'de': '',
        'da': ''
        # 'be': ''
    }

    dfResult = list()

    for name in totalUrl:
        ## mle > ds > de > da 순으로 진행되고 한 직무가 끝날 때마다 공고, 기술 스택이 구글시트에 입력됩니다.

        print(f'{name} 시작!')

        positionUrl, tempList = None, None
        tempList = list()

        for idx in range(len(totalUrl[name])):
            
            # print(totalUrl[name][idx])
            tempList.append(totalUrl[name][idx])

        positionUrl = wc.gatherJD(tempList, driver)
        # print(positionUrl)

        countUrl[name] = len(positionUrl)

        tempList = wc.crawling_wanted(positionUrl, driver)  # 직무 별 공고 크롤링
        existJD = sheetReadMain(f'{name}공고')  # 직무 시트에서 이전에 입력되있는 데이터 추출

        convertList = [list(i.values()) for i in tempList]

        insertData = compare(existJD, convertList)  # 겹치는 공고 제외를 위한 함수
        sheetWrite(f'{name}공고', insertData)  # 입력되어 있지 않은 공고 구글 시트에 입력

        stackList = copy.deepcopy(tempList)  # 스택을 따로 추출하기 위해서 copy
        extractStack(name, stackList)  # 직무 별 스택 구글 시트 입력

        dfResult += tempList  # df로 만들어주기 위해서 이전에 생성해놓은 list에 추가

    if bool:

        dfResult = wc.make_df(dfResult)
        wc.save_df(dfResult)

    return countUrl


def extractStack(name, data):
    ## 구글 시트에 기술스택을 입력하기 위해서 카운트를 하는 함수입니다.

    stackList = list()

    data = [i['기술스택 ・ 툴'] for i in data]

    for i in data:
        x = i.split('\n')
        stackList.extend(x)

    stackList = [i for i in stackList if i]
    stackList = Counter(stackList).most_common(20)
    print(f'{name}의 기술 스택 결과 : {stackList}')

    stackSheetReadAndWrite(name, stackList)


def loadCsvFile():

    csvFiles = sorted(glob.glob('crawlingData/*.csv'))
    cnt, data, compareJD = 0, list(), list()

    for cf in csvFiles:

        tempTotalList, tempCompanyInfo = None, None
        convertDate = re.split('[/, ]', cf)
        convertDate = datetime.datetime.strptime(convertDate[1], '%Y-%m-%d').date()

        if convertDate < datetime.date.today():

            cnt += 1
            break

        else:

            with open(cf, 'r') as file:

                tempTotalList = csv.reader(file)
                next(tempTotalList)
                tempTotalList = [i for i in tempTotalList]
                tempCompanyInfo = [i[:2] for i in tempTotalList]

            data.extend(tempTotalList)
            compareJD.extend(tempCompanyInfo)

    print(f'날짜가 지난 {cnt}개의 파일이 존재합니다.')

    return data, compareJD


def compare(existData, newData):

    # print(newData)
    for idx in range(len(newData)):

        if newData[idx][:2] in existData:
            print(f'{newData[idx]}는 존재.')
            newData[idx] = ''
    newData = [rowData for rowData in newData if rowData]

    return newData


gc = gspread.service_account(filename='/Users/taebeomkim/wanted_crawler_v2/stable-victory-376907-a8e79002c478.json')
doc = gc.open_by_url("https://docs.google.com/spreadsheets/d/1c1r9mdsQIzSYx1eDx_VWNBWBUhgIPvrTjTQYbvI5EPo/edit?usp=sharing")

def sheetWrite(sheetName, data):  # 구글 시트에 데이터를 입력하는 함수입니다.

    doc.worksheet(f"{sheetName}").append_rows(data, insert_data_option='INSERT_ROWS')


def sheetReadMain(sheetName):  # 구글 시트에 입력되있는 회사명과 공고 이름을 가져오는 함수입니다.

    sheetData = doc.worksheet(f"{sheetName}").get_all_records()
    existJD = []

    if sheetData == []:
        ...
    else:
        for i in sheetData:
            existJD.append(list(i.values())[:2])

    return existJD


def stackSheetReadAndWrite(sheetName, data):
    ## 직무 별 기술스택을 월 별로 기입하는 함수입니다.

    stackColList = doc.worksheet(f'{sheetName}').col_values(1)
    print(stackColList)

    month = datetime.date.today().month

    for rowData in data:

        if list(rowData)[0] in stackColList: ...
        else:
            doc.worksheet(f'{sheetName}').insert_row([f'{list(rowData)[0]}'], len(stackColList)+1)
            stackColList.append(list(rowData)[0])
    
        cell = doc.worksheet(f'{sheetName}').find(f'{list(rowData)[0]}')
        # print(f'{list(rowData)[0]}의 위치는 {cell.row}, {cell.col}')
        doc.worksheet(f'{sheetName}').update_cell(cell.row, cell.col+month, list(rowData)[1])
        time.sleep(2)


if __name__ == "__main__":

    """
    main 파일 실행 시
    1. jdLink 파일에 있는 직무 검색 링크로 각 기업 Url 크롤링
    2. 각 직무 별 기술/스택 추출 후 구글 시트에 저장
    3. 직무 별 크롤링 결과를 csv 파일로 저장
    4. csv 파일을 불러온뒤 구글 시트에 저장
    """
    countUrl = crawling(totalUrl)
    print(countUrl)
    

    # totalData, companyInfo = loadCsvFile()
    # existJD = sheetReadMain("da공고")
    # print(existJD)

    # sheetWrite("전체공고", totalData)
    # print(test)
    # test = [['슈프리마', '얼굴인식/비디오 분석 인공지능 알고리즘 개발자']]
    # test1 = [['슈프리마', '얼굴인식/비디오 분석 인공지능 알고리즘 개발자'], ['컬리', '[컬리] Data Scientist(데이터사이언티스트)']]
    # print(test1)
    # for idx in range(len(test1)):
    #     print(test1[idx])
    #     if test1[idx] in test:
    #         print(f'{test1[idx]}는 test안에 존재하므로 삭제.')
    #         test1[idx] = ''
    #         print(test1)
    # test1 = [i for i in test1 if i]
    # print(test1)
    # stackSheetReadAndWrite('da', [('SQL', 2), ('Trello', 1), ('Figma', 1), ('VueJS', 1), ('Python', 1), ('리팩토링', 1), ('ERP 소프트웨어', 1), ('백엔드 개발', 1), ('Spring Boot', 1)])