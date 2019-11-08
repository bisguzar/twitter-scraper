from requests_html import HTMLSession, HTML
from lxml.etree import ParserError
import mechanicalsoup

session = HTMLSession()

browser = mechanicalsoup.StatefulBrowser()
browser.addheaders = [('User-agent', 'Firefox')]

class Profile:
    """
        트위터 프로파일을 구문 분석하여 정보를 속성으로 분류하십시오.
        
        속성:
            - name
            - username
            - birthday
            - biography
            - website
            - profile_photo
            - likes_count
            - tweets_count
            - followers_count
            - following_count
    """
    def __init__(self, username):
        browser.open("https://twitter.com/"+username)
        page = browser.get_current_page()
        self.username = username
        self.__parse_profile(page)

    def __parse_profile(self, page):
        # 구문 분석 위치, 또한 사용자 이름이 올바른지 확인하기
        try:
            self.location = page.find(attrs={"class":"ProfileHeaderCard-locationText u-dir"}).contents[1].contents[0].strip()
        except AttributeError:
            raise ValueError(
                    f'웁스! "@{self.username}" 가 존재하지 않거나 은닉화되어 있습니다.')

        # birthday 파싱하기
        try:
            self.birthday = page.find(attrs={"class":"ProfileHeaderCard-birthdateText u-dir"}).find().contents[0].strip().replace("Born ", "")
        except:
            self.birthday = None

        # 프로필 사진의 URL을 파싱하기
        self.profile_photo = page.find(attrs={"class":"ProfileAvatar-image"}).attrs['src']

        # 전체 이름을 파싱하기
        name_text = page.find("title").contents[0]
        self.name = name_text[:name_text.find('(')].strip()

        # 인물 정보를 파싱하기
        self.biography = self.__process_paragraph(page.find(attrs={"class":"ProfileHeaderCard-bio u-dir"}).contents)

        # 사용자의 웹 사이트 주소를 파싱하기
        try:
            self.website = page.find(attrs={'class': 'ProfileHeaderCard-urlText u-dir'}).find().contents[0].strip()
        except:
            self.website = None
        
        # 팔로워 수를 파싱하기
        try:
            q=page.find(attrs={"data-nav":"followers"})
            self.followers_count = int(q.attrs["title"].split(' ')[0].replace(',',''))
        except:
            self.followers_count = 0

        # 좋아요 수를 파싱하기
        q=page.find(attrs={"data-nav":"favorites"})
        self.likes_count = int(q.attrs["title"].split(' ')[0].replace('.', ''))

        # 팔로잉 수를 파싱하기
        q=page.find(attrs={"data-nav":"following"})
        self.following_count = int(q.attrs["title"].split(' ')[0].replace(',',''))

        # 트윗의 횟수를 파싱하기
        q=page.find(attrs={"data-nav":"tweets"})
        self.tweets_count = int(q.attrs["title"].split(' ')[0].replace(',',''))

    def __process_paragraph(self, contents):
        output = ''
        links = []
        for i in contents:
            try:
                output+=i
            except:
                if i.name=="a":
                    tmp_txt, tmp_lnk = process_paragraph(i.contents)
                    links+=tmp_lnk
                    output+=tmp_txt#+'@['+i.attrs['href']+']'
                    links.append(i.attrs['href'])
                elif i.name in ['s', 'b']:
                    tmp_txt, tmp_lnk = process_paragraph(i.contents)
                    links+=tmp_lnk
                    output+=tmp_txt
        return output, links

    def __dir__(self):
        return [
            'name',
            'username',
            'birthday',
            'biography',
            'website',
            'profile_photo',
            'likes_count',
            'tweets_count',
            'followers_count',
            'following_count'
        ]

    def __repr__(self):
        return f'<profile {self.username}@twitter>'
