# crwaling with search on wanted

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import sqlite3
import time

def create_url(category : list):
    """
    category 번호를 받아서 url 반환하는 함수

    Note:
    파이썬개발자 : selected=899
    데이터엔지니어 : selected=655
    빅데이터엔지니어 : selected=1025
    머신러닝엔지니어 :selected=1634
    데이터사이언티스트 : selected=1024
    영상음성엔지니어 : selected=896
    """
    category_url = category[0] + "/" + category[1]
    # for temp_category in category:
    #     category_url += f"{temp_category}"
    # url = f"https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=0&years=2&{category_url}locations=all"
    url = f"https://www.wanted.co.kr/wdlist/{category_url}?country=kr&job_sort=company.response_rate_order&years=2&years=8&locations=all"
    
    # print(url)
    return url

def create_url_search(category : str):
   
    url = f"https://www.wanted.co.kr/search?query={search_word}"
    return url

def init_database():
    """
    데이터베이스 초기화

    urlinfo 테이블 
    : 크롤링 중 오류가 날 수 있기 때문에 URL 정보를 우선 적재합니다.
    
    JDinfo 테이블 
    : 각 JD의주요 업무, 요구 사항, 우대 사항, 혜택 및 복지, 기술스택 ・ 툴을 적재합니다.
    """
    timeinfo = int(time.time())
    conn = sqlite3.connect(f'wanted_{timeinfo}.db')
    cur = conn.cursor()
    SQL_CTEATE_URL_INFO_TABLE = """
    CREATE TABLE IF NOT EXISTS urlinfo (
        url TEXT PRIMARY KEY NOT NULL,
        title VARCHAR(32),
        company VARCHAR(16)
    );
    """
    cur.execute(SQL_CTEATE_URL_INFO_TABLE)

    SQL_CTEATE_JD_INFO_TABLE = """
    CREATE TABLE IF NOT EXISTS JDinfo (
        JD_id INTEGER PRIMARY KEY AUTOINCREMENT,
        CoName TEXT,
        Jikmu TEXT,
        CoTag TEXT,
        JobToDo TEXT,
        requirement TEXT,
        preferential TEXT,
        welfare TEXT,
        skills TEXT,
        close_date TEXT,
        location TEXT,
        url TEXT,
        --
        FOREIGN KEY (url) REFERENCES urlinfo(url)
    );
    """
    cur.execute(SQL_CTEATE_JD_INFO_TABLE)
    cur.close()
    conn.close()
    print("init database를 성공했습니다.")
    return timeinfo

def get_conn_cur(timeinfo: int):
    conn = sqlite3.connect(f'wanted_{timeinfo}.db')
    cur = conn.cursor()
    return conn, cur

def scroll_down(driver):
    """
    스크롤 끝까지 내리는 코드
    """
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

def url_crawler(driver, category_or_searchword):

    # 중간에 뜨는 이상한 팝업 제거
    try :
        driver.find_element(By.CLASS_NAME,'MaintenancePopUp_Maintenance_close__cHJg7').click()
    except:
        pass

    timeinfo = init_database()
    if isinstance(category_or_searchword, str):
    	URL = create_url_search(category_or_searchword)
    else:
    	URL = create_url(category_or_searchword)

    driver.get(URL)

    scroll_down(driver)

    ### 공고 URL 모으는 코드 ###
    elems = driver.find_elements(By.CLASS_NAME, 'Card_className__u5rsb')
    conn, cur = get_conn_cur(timeinfo)
    URL_list = []
    for elem in elems[0:3]:
        ### url, 공고 제목, 회사 데이터 수집 ###
        temp_card = elem.find_element(By.TAG_NAME, 'a')
        temp_text = temp_card.text
        temp_list = temp_text.split('\n')
        temp_url = temp_card.get_attribute('href')

        URL_list.append(temp_url)
        SQL_INSERT_URLINFO = f"INSERT INTO urlinfo (url, title, company) VALUES ('{temp_url}', '{temp_list[0]}', '{temp_list[1]}')"

        cur.execute(SQL_INSERT_URLINFO)
    conn.commit()
    cur.close()
    conn.close()
    return timeinfo

def jd_info_crawler(driver, timeinfo, sleep_time):
    """
    내용 크롤링 함수
    """
    conn, cur = get_conn_cur(timeinfo)
    SQL = """
        SELECT u.url
        FROM urlinfo AS u
        LEFT JOIN JDinfo AS j
        ON u.url=j.url
        WHERE j.url IS NULL
        """
    cur.execute(SQL)
    URL_list = [x[0] for x in cur.fetchall()]
    for URL in URL_list:               
        driver.get(URL)
        time.sleep(sleep_time)
        co_tag = []
        # try:
        # 	# tags
        #     for j in len(driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/section[2]/div[3]/ul/li/a')):
        #         tmp = driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[1]/div[1]/section[2]/div[3]/ul/li/a')[j].text
        #         co_tag.append(tmp)
        # except:
        # 	print("Tag 정보 오류")
        # 	continue
        try:
            jikmu = driver.find_element(By.CSS_SELECTOR, "#__next > div.JobDetail_cn__WezJh > div.JobDetail_contentWrapper__DQDB6 > div.JobDetail_relativeWrapper__F9DT5 > div.JobContent_className___ca57 > section.JobHeader_className__HttDA > h2").text
            co_name = driver.find_element(By.TAG_NAME, 'h5').text
            cont = driver.find_element(By.CLASS_NAME, 'JobDescription_JobDescription__VWfcb')
            contents_header = cont.find_elements(By.TAG_NAME, 'h6')
            preferential = ""
            skills = ""
            for header in contents_header:
                ### 주요업무, 자격요건, 우대사항, 혜택 및 복지, 기술스택&툴 데이터 수집 ###
                temp_contents = header.find_element(By.XPATH, 'following-sibling::*')
                if header.text == "주요업무":
                    JobToDo = temp_contents.text
                    JobToDo = JobToDo.replace("'", '"')
                elif header.text == "자격요건":
                    requirement = temp_contents.text
                    requirement = requirement.replace("'", '"')
                elif header.text == "우대사항":
                    preferential = temp_contents.text
                    preferential = preferential.replace("'", '"')
                elif header.text == "혜택 및 복지":
                    welfare = temp_contents.text
                    welfare = welfare.replace("'", '"')
                elif header.text == "기술스택 ・ 툴":
                    skills = temp_contents.text
                    skills = skills.replace("'", '"')
            # print("error : getinfo")
            ### 마감일, 근무지역 데이터를 위해 특정 부분까지 스크롤 다운 ###
            action = ActionChains(driver)
            cont = driver.find_element(By.CLASS_NAME, 'StealingWarning_StealingWarning_content__Ik3sn')
            action.move_to_element(cont).perform()
            time.sleep(sleep_time-1)
            parents_object = driver.find_element(By.CLASS_NAME, 'JobWorkPlace_className__ra6rp')
            text = parents_object.text
            text_split = text.split('\n')
            close_date = text_split[0].lstrip('마감일')
            location = text_split[1].lstrip('근무지역')

            SQL_INSERT_JDINFO = f"""
            INSERT INTO JDinfo (CoName, Jikmu, CoTag, JobToDo, requirement, preferential, welfare, skills, close_date, location, url) 
            VALUES ('{co_name}', '{jikmu}','{co_tag}', '{JobToDo}', '{requirement}', '{preferential}', '{welfare}', '{skills}', '{close_date}', '{location}', '{URL}')
            """
            cur.execute(SQL_INSERT_JDINFO)
            conn.commit()
        except:
            print("채용 정보를 가져오지 못 했습니다.")
            continue
    cur.close()
    conn.close()

def check_if_failed(timeinfo):
    conn, cur = get_conn_cur(timeinfo)
    SQL = """
        SELECT u.url
        FROM urlinfo AS u
        LEFT JOIN JDinfo AS j
        ON u.url=j.url
        WHERE j.url IS NULL
        """
    cur.execute(SQL)
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result:
        return True
    return False

def crawling_until_end(driver, timeinfo, sleep_time):
    CHECK = check_if_failed(timeinfo)
    SLEEP_TIME = sleep_time
    if CHECK:
        SLEEP_TIME += 1
        jd_info_crawler(driver, timeinfo, SLEEP_TIME)
        crawling_until_end(driver, timeinfo, SLEEP_TIME)

# 셀레니움 드라이버 시작
def driver_start():
    # user_agent
    user_agent = 'user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    user_agent = 'Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36'

    # options setting
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(user_agent) # Fake User Agent 설정
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
    chrome_options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
    chrome_options.add_argument('incognito') #시크릿 모드의 브라우저가 실행됩니다.
    chrome_options.add_argument('window-size={1000},{813}') #브라우저 사이즈 설정


    # driver start
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    return driver

if __name__=="__main__":
    from webdriver_manager.chrome import ChromeDriverManager

    searching = str(input(f"직무명/회사이름으로 검색은 (1 입력 후 엔터) 카테고리 검색은 (아무 키나 입력하세요.) >>>"))

    if searching == '0':
    	sub_c_num = str(input(f"파이썬개발자 : 899\n데이터엔지니어 : 655\n빅데이터엔지니어 : 1025\n머신러닝엔지니어 : 1634\n데이터사이언티스트 : 1024\n영상음성엔지니어 : 896\n데이터분석가 : 656\n\n프론트엔드 : 669\n직군코드를 입력해주세요>>>"))
    	if sub_c_num == "655" or sub_c_num == "899" or sub_c_num == "1024" or sub_c_num == "1025" or sub_c_num == "1634" or sub_c_num == "896" or sub_c_num == "669":
        	sub_b_num = "518"
    	elif sub_c_num == "656":
        	sub_b_num = "507"
    	CATEGORY_NUM_LIST = [sub_b_num, sub_c_num]
    	driver = driver_start()
    	timeinfo = url_crawler(driver, CATEGORY_NUM_LIST)
    else:
    	search_word = str(input(f"검색어를 입력해주세요 >>>"))
    	driver = driver_start()
    	timeinfo = url_crawler(driver, search_word)



    
    # try:
    #     sub_year_start = str(input(f"대상 직군 경력 시작 \n신입(=0), 2년차(=2)~를 입력해주세요>>>"))
    # except Exception as e:
    #     sub_year_start = 0
    # else:
    #     pass
    # finally:
    #     pass
    
    # sub_year_end = str(input(f"대상 연차를 입력해주세요>>>"))



    ### 원하는 카테고리 번호 & 첫 시도 sleep 초 입력 ###
    SLEEP_TIME = 1
    	
    jd_info_crawler(driver, timeinfo, SLEEP_TIME)
    crawling_until_end(driver, timeinfo, SLEEP_TIME)
    print("크롤링 끄-읕!")