# 트위터 스크래퍼

![GitHub](https://img.shields.io/github/license/bisguzar/twitter-scraper) ![GitHub contributors](https://img.shields.io/github/contributors/bisguzar/twitter-scraper) ![code size](https://img.shields.io/github/languages/code-size/bisguzar/twitter-scraper) ![maintain status](https://img.shields.io/maintenance/yes/2020)

트위터의 API는 작업하기 힘들고 제약도 많다. 다행히도 그들의 프런트엔드(JavaScript)에는 내가 역설계한 자체 API가 있다. 그 API는 속도 제한과 규제가 없고 굉장히 빠르다.

어떤 유저의 트윗이라도 이 라이브러리를 사용해 쉽게 얻을 수 있을 것이다.

## 요구사항

일단 시작하기 전에 다음 사항들을 지켜주길 바란다.

* 인터넷 연결
* 파이썬 3.6+

## 트위터 스트래퍼 설치

만약 최신 버전을 원한다면 소스를 통해 설치해라. 소스로 트위터 스크래퍼를 설치하려면 다음 과정을 따르면 된다:

리눅스와 맥 os에서:
```bash
git clone https://github.com/bisguzar/twitter-scraper.git
cd twitter-scraper
sudo python3 setup.py install 
```

아니면 PyPI로 설치 할 수도 있다.

```bash
pip3 install twitter_scraper
```

## Using twitter_scraper

**twitter-scraper**를 설치하고 함수를 호출하면 된다!


### → 함수 **get_tweets(query: str [, pages: int])** -> 딕셔너리
프로필에서 트윗을 얻거나 해쉬태그에서 단어로 이루어진 트윗을 얻을 수 있다. **get_tweets** 는 유저 이름이나 문자열로 이루어진 해쉬테그를 첫번째 인자로, 스캔을 원하는 페이지 수 만큼을 두번째 정수 인자로 사용한다.

#### 염두해 둘 것:
* 해쉬테그에서 트윗을 얻고 싶다면 첫번째 파라미터는 #, 숫자로 이루어져야 한다. 
* **pages** 파라미터는 옵션이니 꼭 필요한 것은 아니다.

```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import get_tweets
>>> 
>>> for tweet in get_tweets('twitter', pages=1):
...     print(tweet['text'])
... 
spooky vibe check
…
```

반환값은 각 트윗의 딕셔너리이다. 다음은 딕셔너리의 키이다;

| 키       | 유형       | Description                                                      |
|-----------|------------|------------------------------------------------------------------|
| tweetId   | string     | 트윗을 찾는 역할, twitter.com/USERNAME/ID 을 방문해 트윗을 본다. |
| isRetweet | boolean    | 리트윗 되었다면 True , 그렇지 않다면 False                          |
| time      | datetime   | 트윗이 쓰여진 날짜                                              |
| text      | string     | 트윗의 내용                                                   |
| replies   | integer    | 트윗이 답변된 횟수                                           |
| retweets  | integer    | 트윗이 리트윗된 횟수                                           |
| likes     | integer    | 트윗의 '좋아요' 갯수                                             |
| entries   | dictionary | 트윗에 해쉬태그, 비디오, 사진, urls 키가 있을 때. 각각의 값이 배열로 들어간다. | 


### → 클래스 **Profile(username: str)** -> 클래스 인스턴스
존재하고 공개되어 있다면 생일이나 업적 같은 개인 정보를 프로필에서 언을 수 있다. 이 클래스는 유저의 이름을 인자로 사용한다. 그리고 반환은 알아서 한다. 클래스 변수를 사용하여 정보에 접근한다.


```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import Profile
>>> profile = Profile('bugraisguzar')
>>> 
>>> vars(profile)
{'username': 'bugraisguzar', 'location': 'Kocaeli, Türkiye', 'birthday': None, 'profile_photo': 'https://pbs.twimg.com/profile_images/1116760468633288715/9prl254I_400x400.png', 'name': 'Buğra İşgüzar', 'biography': ('geliştirici', []), 'website': 'bisguzar.com', 'followers_count': 432, 'likes_count': 2468, 'following_count': 240, 'tweets_count': 749}
>>> 
>>> profile.location
'Kocaeli, Türkiye'
>>> profile.name
'Buğra İşgüzar'
>>> profile.username
'bugraisguzar'
```


## 트위터 스크래피에 기여하기
트위터 스크래퍼에 기여하려면, 다음 과정을 따라라:

1. 이 저장소를 포크하라.
2. 이 이름으로 브랜치를 만들어라: `git checkout -b <branch_name>`.
3. 바꾸고 나서 커밋하라: `git commit -m '<commit_message>'`
4. 원래 브랜치를 푸쉬하라: `git push origin <project_name>/<location>` 
5. 풀 리퀘스트를 해라.

대안적으로 깃허브의 [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) 를 참고하라.

## 기여자들

이 프로젝트에 기여해주신 다음 분들께 감사드립니다:

* @kennethreitz (author)
* @bisguzar (maintainer)
* @lionking6792

## 연락
저와 연락하고 싶다면 [@bugraisguzar](https://twitter.com/bugraisguzar)을 통해 연락하라.


## 라이센스
이 프로젝트는 다음 라이선스를 따릅니다: [MIT](https://github.com/bisguzar/twitter-scraper/blob/master/LICENSE).
