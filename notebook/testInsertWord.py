from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import webDriver, time
from checkingOfficeName import check

def officeInfo(officeNameList):

    driver = webDriver.driver_start()

    for idx, rowData in enumerate(officeNameList):

        if idx == 5: break

        result, originJson = check(rowData)

        # 수집된 회사면 Pass
        if result == True: ...

        # 수집하지 않은 회사
        else:

            try:

                tempList = []
                url = f'https://www.saramin.co.kr/zf_user/search/company?searchType=search&keydownAccess=&searchword={rowData}&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y'

                # 사람인 기업 정보
                driver.get(url)
                time.sleep(1)

                officeUrl = driver.find_element(By.CLASS_NAME, 'content').find_element(By.CSS_SELECTOR, 'div').find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                # print(officeUrl)

                driver.get(officeUrl)
                dataLen = len(driver.find_element(By.CLASS_NAME, 'box_company_view.company_intro').find_element(By.CLASS_NAME, 'summary').find_elements(By.CSS_SELECTOR, 'li'))
                # print(dataLen)

                for i in range(dataLen):
                    # class이름에 공백이 있어 . 추가
                    # 0 : 업력 / 1 : 기업형태 / 2 : 사원수 / 3 : 매출액
                    # 2020년 0월 0일 설립은 span / 중소기업, 매출액은 strong

                    try:
                        getData = driver.find_element(By.CLASS_NAME, 'box_company_view.company_intro').find_element(By.CLASS_NAME, 'summary').find_elements(By.CSS_SELECTOR, 'li')[i].find_element(By.CSS_SELECTOR, 'strong')
                        tempList.append(getData.text)
                        # print(getData.text)

                    # 기업형태가 복수일 떄
                    except:
                        getData = driver.find_element(By.CLASS_NAME, 'box_company_view.company_intro').find_element(By.CLASS_NAME, 'summary').find_elements(By.CSS_SELECTOR, 'li')[i].find_element(By.CLASS_NAME, 'btn_company_scale')
                        tempList.append(getData.text)
                        # print(getData.text)

                # print(tempList)

                ### 회사마다 정보가 다름. e.g. [기업형태, 사원수] / [업력, 기업형태, 매출액] 등등... 같은 길이더라도 정보가 다를 수 있음.
                # 사원수가 나오지 않을 경우
                if len(tempList) == 3:
                    originJson[f'{rowData}'] = {'업력': tempList[0], '기업형태': tempList[1], '사원수': '', '매출액': tempList[2]}
                # 사원수가 나온 경우
                elif len(tempList) == 4:
                    originJson[f'{rowData}'] = {'업력': tempList[0], '기업형태': tempList[1], '사원수': tempList[2], '매출액': tempList[3]}

            except:
                # driver.find_element(By.CLASS_NAME, 'info_no_result').text
                print(f"{rowData}는 검색결과가 없습니다.")


if __name__ == "__main__":
    import csv, re

    officeNameList = []

    with open('/Users/taebeomkim/wanted_crawler_v2/crawlingData/2023-01-24 20:19:04_wanted_crawling.csv', 'r') as test:
        data = csv.reader(test)

        for idx, rowData in enumerate(data):
            if idx == 0: ...
            # elif idx == 5: break
            else:
                insertData = re.split('[],(,[, -, _, /, )]', rowData[0])
                officeNameList.append(insertData[0])

    officeNameList = list(set(officeNameList))
    officeNameList.sort()
    # print(officeNameList)

    officeInfo(officeNameList)

    # for rowData in officeNameList:
    #     print(rowData)
    #     time.sleep(1)

    # driver = webDriver.driver_start()

    # testUrl = 'https://www.saramin.co.kr/zf_user/search/company?searchType=search&keydownAccess=&searchword=코드스테이츠&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y'
    # # officeInfo([testUrl])

    # driver.get(testUrl)
    # try:
    #     test = driver.find_element(By.CLASS_NAME, 'info_no_result').text
    #     print(test)
    # except:
    #     print('정보를 검색합니다!')
    #     pass