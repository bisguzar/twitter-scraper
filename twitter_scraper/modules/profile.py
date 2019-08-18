from requests_html import HTMLSession, HTML
from lxml.etree import ParserError
import mechanicalsoup

session = HTMLSession()

browser = mechanicalsoup.StatefulBrowser()
browser.addheaders = [('User-agent', 'Firefox')]

class Profile:
    """
        Parse twitter profile and split informations into class as attribute.
        
        Attributes:
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
        # parse location, also check is username valid 
        try:
            self.location = page.find(attrs={"class":"ProfileHeaderCard-locationText u-dir"}).contents[1].contents[0].strip()
        except AttributeError:
            raise ValueError(
                    f'Oops! Either "@{self.username}" does not exist or is private.')

        # parse birthday
        try:
            self.birthday = page.find(attrs={"class":"ProfileHeaderCard-birthdateText u-dir"}).find().contents[0].strip().replace("Born ", "")
        except:
            self.birthday = None

        # parse URL of profile photo
        self.profile_photo = page.find(attrs={"class":"ProfileAvatar-image"}).attrs['src']

        # parse full name
        name_text = page.find("title").contents[0]
        self.name = name_text[:name_text.find('(')].strip()

        # parse biography
        self.biography = self.__process_paragraph(page.find(attrs={"class":"ProfileHeaderCard-bio u-dir"}).contents)

        # parse user's website adress
        try:
            self.website = page.find(attrs={'class': 'ProfileHeaderCard-urlText u-dir'}).find().contents[0].strip()
        except:
            self.website = None
        
        # parse count of followers
        try:
            q=page.find(attrs={"data-nav":"followers"})
            self.followers_count = int(q.attrs["title"].split(' ')[0].replace(',',''))
        except:
            self.followers_count = 0

        # parse count of likes
        q=page.find(attrs={"data-nav":"favorites"})
        self.likes_count = int(q.attrs["title"].split(' ')[0].replace('.', ''))

        # parse count of following
        q=page.find(attrs={"data-nav":"following"})
        self.following_count = int(q.attrs["title"].split(' ')[0].replace(',',''))

        # parse count of tweets
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
