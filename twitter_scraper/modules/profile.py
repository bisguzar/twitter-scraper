from requests_html import HTMLSession, HTML
from lxml.etree import ParserError

session = HTMLSession()


class Profile:
    """
        Parse twitter profile and split informations into class as attribute.

        Attributes:
            - name
            - username
            - birthday
            - location
            - biography
            - website
            - profile_photo
            - banner_photo
            - likes_count
            - tweets_count
            - followers_count
            - following_count
            - is_verified
            - is_private
            - user_id
    """

    def __init__(self, username):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": f"https://twitter.com/{username}",
            # Getting mobile webpage by using Chrome < 38
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062 Safari/537.36',
            "X-Twitter-Active-User": "yes",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-US",
        }

        page = session.get(f"https://twitter.com/{username}", headers=headers)
        self.username = username
        self.__parse_profile(page)
        
    def __parse_profile(self, page):
        try:
            html = HTML(html=page.text, url="bunk", default_encoding="utf-8")
        except KeyError:
            raise ValueError(
                f'Oops! Either "{self.username}" does not exist or is private.'
            )
        except ParserError:
            pass
        
        # TODO cannot find ProfileHeaderCard-badges
        try:
            self.is_private = html.find(".ProfileHeaderCard-badges .Icon--protected")[0]
            self.is_private = True
        except Exception as e:
            self.__failed_fetching('is_private', e)
            self.is_private = False

        # blue badge
        self.is_verified = True
        try:
            q = html.find("a.badge")[0]
            if not q:
                self.is_verified = False
        except Exception as e:
            self.__failed_fetching('is_verified', e)
            self.is_verified = False

        try:
            self.location = html.find('div.location')[0].text
            if not self.location:
                self.location = None
        except Exception as e:
            self.__failed_fetching('location', e)
            self.location = None

        # TODO cannot find ProfileHeaderCard-birthdateText
        try:
            self.birthday = html.find(".ProfileHeaderCard-birthdateText")[0].text
            if self.birthday:
                self.birthday = self.birthday.replace("Born ", "")
            else:
                self.birthday = None
        except Exception as e:
            self.__failed_fetching('birthday', e)
            self.birthday = None

        try:
            self.profile_photo = html.find("td.avatar img")[0].attrs["src"]
        except Exception as e:
            self.__failed_fetching('profile_photo', e)
            self.profile_photo = None

        # TODO cannot find ProfileCanopy-headerBg
        try:
            self.banner_photo = html.find(".ProfileCanopy-headerBg img")[0].attrs["src"]
        except Exception as e:
            self.__failed_fetching('banner_photo', e)
            self.banner_photo = None

        try:
            page_title = html.find("title")[0].text
            self.name = page_title[: page_title.find("(")].strip()
        except Exception as e:
            self.__failed_fetching('name', e)
            self.name = None
        
        try:
            self.user_id = html.find(".ProfileNav")[0].attrs["data-user-id"]
        except Exception as e:
            self.__failed_fetching('user_id', e)
            self.user_id = None

        try:
            self.biography = html.find("div.bio div.dir-ltr")[0].text     
            if not self.biography:
                self.biography = None
        except Exception as e:
            self.__failed_fetching('biography', e)
            self.biography = None

        try:
            self.website = html.find("div.url div.dir-ltr")[0].text
            if not self.website:
                self.website = None
        except Exception as e:
            self.__failed_fetching('website', e)
            self.website = None

        # get stats table if available
        stats_table = None
        stats = None
        try:
            stats_table = html.find('table.profile-stats')[0]
            stats = stats_table.find('td div.statnum')
        except:
            self.stats = None
            
        # get total tweets count if available
        try:
            self.tweets_count = int(stats[0].text.replace(',',''))
        except Exception as e:
            self.__failed_fetching('tweets_count', e)
            self.tweets_count = None

        # get total following count if available
        try:
            self.following_count = int(stats[1].text.replace(',',''))
        except Exception as e:
            self.__failed_fetching('following_count', e)
            self.following_count = None

        # get total follower count if available
        try:
            self.followers_count = int(stats[2].text.replace(',',''))
        except Exception as e:
            self.__failed_fetching('followers_count', e)
            self.followers_count = None

        # get total like count if available
        # TODO unfixed
        try:
            q = html.find('li[class*="--favorites"] span[data-count]')[0].attrs["data-count"]
            self.likes_count = int(q)
        except Exception as e:
            self.__failed_fetching('likes_count', e)
            self.likes_count = None

    def __failed_fetching(self, var: str, except_msg: str):
        print(f'Unable to get {var} in html, exception - {except_msg}')

    def to_dict(self):
        return dict(
            name=self.name,
            username=self.username,
            birthday=self.birthday,
            biography=self.biography,
            location=self.location,
            website=self.website,
            profile_photo=self.profile_photo,
            banner_photo=self.banner_photo,
            likes_count=self.likes_count,
            tweets_count=self.tweets_count,
            followers_count=self.followers_count,
            following_count=self.following_count,
            is_verified=self.is_verified,
            is_private=self.is_private,
            user_id=self.user_id
        )

    def __dir__(self):
        return [
            "name",
            "username",
            "birthday",
            "location",
            "biography",
            "website",
            "profile_photo",
            'banner_photo'
            "likes_count",
            "tweets_count",
            "followers_count",
            "following_count",
            "is_verified",
            "is_private",
            "user_id"
        ]

    def __repr__(self):
        return f"<profile {self.username}@twitter>"
