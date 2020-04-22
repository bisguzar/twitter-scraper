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
            - biography
            - website
            - profile_photo
            - likes_count
            - tweets_count
            - followers_count
            - following_count
    """

    def __init__(self, username):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": f"https://twitter.com/{username}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
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

        # TODO: Check what kind of exception raising if no location
        self.location = html.find(".ProfileHeaderCard-locationText")[0].text

        # TODO: Check what kind of exception raising if no location
        self.birthday = html.find(".ProfileHeaderCard-birthdateText")[0].text
        if self.birthday:
            self.birthday = self.birthday.replace("Born ", "")
        else:
            self.birthday = None

        self.profile_photo = html.find(".ProfileAvatar-image")[0].attrs["src"]

        page_title = html.find("title")[0].text
        self.name = page_title[: page_title.find("(")].strip()

        self.biography = html.find(".ProfileHeaderCard-bio")[0].text

        self.website = html.find(".ProfileHeaderCard-urlText")[0].text

        # get total tweets count if available
        try:
            q = html.find('li[class*="--tweets"] span[data-count]')[0].attrs["data-count"]
            self.tweets_count = int(q)
        except:
            self.tweets_count = None

        # get total following count if available
        try:
            q = html.find('li[class*="--following"] span[data-count]')[0].attrs["data-count"]
            self.following_count = int(q)
        except:
            self.following_count = None

        # get total follower count if available
        try:
            q = html.find('li[class*="--followers"] span[data-count]')[0].attrs["data-count"]
            self.followers_count = int(q)
        except:
            self.followers_count = None

        # get total like count if available
        try:
            q = html.find('li[class*="--favorites"] span[data-count]')[0].attrs["data-count"]
            self.likes_count = int(q)
        except:
            self.likes_count = None

    def to_dict(self):
        return dict(
            name=self.name,
            username=self.username,
            birthday=self.birthday,
            biography=self.biography,
            website=self.website,
            profile_photo=self.profile_photo,
            likes_count=self.likes_count,
            tweets_count=self.tweets_count,
            followers_count=self.followers_count,
            following_count=self.following_count,
        )

    def __dir__(self):
        return [
            "name",
            "username",
            "birthday",
            "biography",
            "website",
            "profile_photo",
            "likes_count",
            "tweets_count",
            "followers_count",
            "following_count",
        ]

    def __repr__(self):
        return f"<profile {self.username}@twitter>"
