from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


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

    # try:
    #     # driver start
    #     driver = webdriver.Chrome(executable_path='/Users/taebeomkim/wanted_crawler_v2/chromedriver', options=chrome_options)
    # except:
    #     # !xattr -d com.apple.quarantine chromedriver
    #       print('test')

    driver = webdriver.Chrome(executable_path='/Users/taebeomkim/wanted_crawler_v2/chromedriver', options=chrome_options)

    return driver


if __name__ == "__main__":
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

    print(MLE_url+DS_url+DA_url+DE_url+BE_url)

    driver = driver_start()