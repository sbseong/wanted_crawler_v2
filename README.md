# wanted_crawler_v2
DB화를 통한 속도 Up, 검색기능 추가한 버전

# 사용법
### 0. 가상환경 생성 및 활성화 (Optional)
```
$ conda create -n wanted python=3.8
$ conda activate wanted
```
### 1. `requirement.txt`에서 필요한 패키지 설치
```
$ pip install -r requirements.txt
```
### 2-1. `wanted_search.py` 실행
```
### 2-2. `url_wanted.py` 실행 : 원하는 페이지의 url을 복붙하면 그 페이지를 크롤링 해줌
```
### 3. 여러 DB를 하나 머지하는 방법
#### 3-1. 여러 DB를 하나의 폴더에 만들어서 넣어둡니다. 
#### 3-2. `auto_merge_to_csv.py` 실행
```
python wanted_search.py
```

## 💡 크롤러가 활용하는 창이 모니터에 노출되어 있으면 수집이 더 잘 됩니다.
