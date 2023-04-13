# 초기에 selenium은 install 해야할 수 있음
# !pip install selenium
# !pip install pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from jdLink import filter
import time, datetime, sys, webDriver, re, os
import pandas as pd

# ### Python의 버전, 웹 드라이버 버전, Pandas 버전 확인
# print(f'Python Version : {sys.version}')
# print(f'Selenium webdriver Version : {webdriver.__version__}')
# print(f'Pandas Version : {pd.__version__}')

# ‘chromedriver’은(는) Apple에서 악성 소프트웨어가 있는지 확인할 수 없기 때문에 열 수 없습니다. 가 뜨면
# !xattr -d com.apple.quarantine chromedriver

# 스크롤 다운
def scroll():
    #스크롤 내리기 이동 전 위치
    scroll_location = driver.execute_script("return document.body.scrollHeight")

    while True:
        #현재 스크롤의 가장 아래로 내림
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        #전체 스크롤이 늘어날 때까지 대기
        time.sleep(3)

        #늘어난 스크롤 높이
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        #늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
        if scroll_location == scroll_height:
            break

        #같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복
        else:
            #스크롤 위치값을 수정
            scroll_location = driver.execute_script("return document.body.scrollHeight")


# 스크롤 끝까지 내리는 코드
def scroll_down(driver):
    SCROLL_PAUSE_SEC = 3

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("스크롤 다운 완료!")


# 채용공고 url 획득

def get_urls(driver, url):

    driver.get(url)
    time.sleep(3)

    # urls 저장
    position_urls = []

#     # 50인 이하 클릭
#     driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div/div[1]/div[1]/section/div/div/div/div/div[6]/div/button').click()

    scroll_down(driver)

    # 채용공고를 아래로 스크롤하여 더 추가할 경우 아래 주석을 풀고 실행, 오래걸림 주의
    # 4/13(목) : CLASS_NAME 수정 
    # position_length = len(driver.find_elements(By.CLASS_NAME, 'JobCard_container__FqChn')) # 'Card_className__u5rsb'))
    # print(position_length)

    totalUrl = driver.find_elements(By.CLASS_NAME, 'JobCard_container__FqChn')

    time.sleep(1)

    for i in range(len(totalUrl)):

        tempCard = totalUrl[i].find_element(By.TAG_NAME, 'a') # driver.find_element(By.CLASS_NAME, 'List_List_container__JnQMS').find_element(By.CSS_SELECTOR, 'ul').find_elements(By.CSS_SELECTOR, 'li')[i].find_element(By.CSS_SELECTOR, 'div').find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

        # print(tempCard.get_attribute('href'))
        position_urls.append(tempCard.get_attribute('href'))

        # break

    print("링크 개수 : ", end='')
    print(len(totalUrl))

    return position_urls


# 각 채용공고 별 상세 jd 획득
def crawling_wanted(position_urls, driver):

    results =[]

    for i in range(len(position_urls)):

        # print(f'{i+1} / {len(position_urls)}')

        cnt = 0
        driver.get(position_urls[i])
        result = {
            '기업명': '',
            '공고 제목' : '',
            '산업분류' : '',
            '마감일' : '',
            '주요업무' : '',
            '자격요건' : '',
            '우대사항' : '',
            'URL' : '',
            '기술스택 ・ 툴' : '',
        }
        time.sleep(1.5)

        # 기업명, 공고 제목, URL
        try:
            company_name =  driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/section[2]/div[1]/h6/a')[0].text
            result['기업명'] = company_name

            job_title = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/section[2]/h2')[0].text

            words = re.split('[],(,[, -, _, /, )]', job_title)
            words = [i.lower() for i in words]
            words = ' '.join(words).split()

            for idx in range(len(words)):
                if words[idx] not in filter:
                    # result['공고 제목'] = job_title
                    cnt += 1

            if cnt == len(words):
                print(f"{job_title}은 적절하지 않은 공고같습니다.\n{position_urls[i]}")
                continue
            else: result['공고 제목'] = job_title

            industry = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/section[3]/button[1]/div[2]/h6')[0].text
            result['산업분류'] = industry

            # tag = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/section[2]/div[3]')[0].text
            # result['태그'] = tag
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # 마감일 동적 페이지 로딩을 위해 페이지 이동
            action = ActionChains(driver)
            element = driver.find_elements(By.CLASS_NAME, 'WarningHeader_WarningHeader__F1ikW')[0]
            action.move_to_element(element).perform()
            # time.sleep(1.5)


            # 마감일
            date = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[2]/div[1]/span[2]')[0].text
            result['마감일'] = date
            result['URL'] = position_urls[i]

            # JD - title
            driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/h6')
            size = len(driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/h6'))
            # time.sleep(1.5)

            for j in range(1, size+1):
                title = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/h6')[j-1].text
                if title in ['주요업무', '자격요건', '우대사항', '기술스택 ・ 툴']:
                    content = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p')[j].text
                    result[title] = content
                    # time.sleep(1.5)

            results.append(result)
            time.sleep(1.5)

        except:
            print("채용 정보를 가져오지 못 했습니다.")
            print(position_urls[i])
            continue

    return results


def make_df(results):
    wanted_crawling = pd.DataFrame(results)
    # 중복체크
    if wanted_crawling.duplicated('URL').sum():
        print(f'Drop Duplicated : {wanted_crawling.duplicated("URL").sum()}')
        wanted_crawling = wanted_crawling.drop_duplicates()
    return wanted_crawling


def save_df(wanted_crawling):
    # Data Frame save
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    wanted_crawling.to_csv(f'./crawlingData/{today}_wanted_crawling.csv', index=False, line_terminator = '\n')
    print('Save 완료!')


def gatherJD(urls, driver):

    for i in range(len(urls)):
        if i == 0:
            positionUrls = get_urls(driver, urls[i])
        else:
            positionUrls.extend(get_urls(driver, urls[i]))

    return positionUrls


if __name__ == "__main__":
    # driver 객체 생성
    driver = webDriver.driver_start()

    # 데이터 과학자는 공고 X / ML과 MLOps는 같이 크롤링됨.
    MLE_url = ['https://www.wanted.co.kr/search?query=ML',
    'https://www.wanted.co.kr/search?query=machine%20learning',
    'https://www.wanted.co.kr/search?query=%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D',
    'https://www.wanted.co.kr/search?query=deep%20learning',
    'https://www.wanted.co.kr/search?query=%EB%94%A5%EB%9F%AC%EB%8B%9D',
    'https://www.wanted.co.kr/search?query=%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5']
    DS_url = ['https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%82%AC%EC%9D%B4%EC%96%B8%ED%8B%B0%EC%8A%A4%ED%8A%B8',
    'https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%82%AC%EC%9D%B4%EC%96%B8%ED%8B%B0%EC%8A%A4%ED%8A%B8',
    'https://www.wanted.co.kr/search?query=data%20scientist',
    'https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EA%B3%BC%ED%95%99%EC%9E%90']
    DA_url = ['https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%EC%84%9D%EA%B0%80',
    'https://www.wanted.co.kr/search?query=data%20analyst',
    'https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%95%A0%EB%84%90%EB%A6%AC%EC%8A%A4%ED%8A%B8']
    DE_url = ['https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4',
    'https://www.wanted.co.kr/search?query=data%20engineer',
    'https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4']
    BE_url = ['https://www.wanted.co.kr/search?query=%EB%B0%B1%EC%97%94%EB%93%9C%20%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4',
        'https://www.wanted.co.kr/search?query=Backend%20Engineer']

    get_urls(driver, 'https://www.wanted.co.kr/search?query=ML')
    ## Test용
    # testResult = crawling_wanted(['https://www.wanted.co.kr/wd/143199'], driver)
    # testResult2 = crawling_wanted(['https://www.wanted.co.kr/wd/97166'], driver)

    # print(testResult)
    # print(testResult2)
    # print("=======================")
    # print(testResult+testResult2)
    # print(testResult+testResult)
    # t = []
    # for i in testResult:
    #     # print(i['기술스택 ・ 툴'])
    #     t.append(i['기술스택 ・ 툴'])
    #     # print(f'for 문 안의 출렵입니다. : {t}')
    # print(f'첫번째 : {t}')

    ###########################################################################
    # tempList = list()
    # tempList = gatherJD(MLE_url+DS_url+DA_url+DE_url+BE_url)
    # totalResult = crawling_wanted(tempList, driver)
    # print(totalResult)

    # # 기업명을 담기 위한 변수
    # companyName = list()

    # # 괄호 안의 문자를 삭제하기 위한 정규표현식
    # pattern = r'\([^)]*\)'

    # # 기업명 추출
    # for rowData in totalResult:
    #     name = rowData['기업명']
    #     name = re.sub(pattern=pattern, repl='', string=name)
    #     companyName.append(name)
    # print(companyName)

    # totalResult = make_df(totalResult)
    # save_df(totalResult)