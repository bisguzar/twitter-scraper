# Twitter Scraper

![GitHub](https://img.shields.io/github/license/bisguzar/twitter-scraper) ![GitHub contributors](https://img.shields.io/github/contributors/bisguzar/twitter-scraper) ![code size](https://img.shields.io/github/languages/code-size/bisguzar/twitter-scraper) ![maintain status](https://img.shields.io/maintenance/yes/2020)

[🇰🇷 Read Korean Version](https://github.com/bisguzar/twitter-scraper/blob/master/twitter_scraper/__init__.py)

Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

You can use this library to get the text of any user's Tweets trivially.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+

## Installing twitter-scraper

If you want to use latest version, install from source. To install twitter-scraper from source, follow these steps:

Linux and macOS:
```bash
git clone https://github.com/bisguzar/twitter-scraper.git
cd twitter-scraper
sudo python3 setup.py install
```

Also, you can install with PyPI.

```bash
pip3 install twitter_scraper
```

## Using twitter_scraper

Just import **twitter_scraper** and call functions!


### → function **get_tweets(query: str, search: str [, pages: int])** -> dictionary
You can get tweets of profile or parse tweets from hashtag, **get_tweets** takes username or hashtag on first parameter as string and how many pages you want to scan on second parameter as integer.

*get_tweets* function now supporting 'search' paramter for new search functionality.

To enable backwards compatibility with existing twitter_scraper API users, `query` can be directly addressed by using `query=` or by providing a positional string. You can get tweets of a given twitter user or parse tweets from a provided hashtag.

Example:

```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19)
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import get_tweets
>>>
>>> for tweet in get_tweets('twitter', pages=1):
...     print(tweet['text'])
...
Which will function identically to:
>>> from twitter_scraper import get_tweets
>>>
>>> for tweet in get_tweets(query='twitter', pages=1):
...     print(tweet['text'])
...
…
```

If `search` is specified, **get_tweets** will yield a dictionary for each tweet which contains the given term. The term can be any string, supporting search keywords of twitter.


#### Keep in mind:
* You must specify either `query`, or `search`. If you supply one string, `query` will be used by default.
* You can not use more than one string, and you cannot specify more than one of the two search arguments (`query`,`search`)
* **pages** parameter is optional, default is 25.

```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19)
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import get_tweets
>>>
>>> for tweet in get_tweets(search='to:bugraisguzar', pages=1):
...     print(tweet['text'])
...
pic.twitter.com/h24Q6kWyX8
…
```

It returns a dictionary for each tweet. Keys of the dictionary;

| Key       | Type       | Description                                                      |
|-----------|------------|------------------------------------------------------------------|
| tweetId   | string     | Tweet's identifier, visit twitter.com/USERNAME/ID to view tweet. |
| userId    | string     | Tweet's userId                                                   |
| username  | string     | Tweet's username                                                 |
| tweetUrl  | string     | Tweet's URL                                                      |
| isRetweet | boolean    | True if it is a retweet, False otherwise                         |
| isPinned | boolean    | True if it is a pinned tweet, False otherwise                     |
| time      | datetime   | Published date of tweet                                          |
| text      | string     | Content of tweet                                                 |
| replies   | integer    | Replies count of tweet                                           |
| retweets  | integer    | Retweet count of tweet                                           |
| likes     | integer    | Like count of tweet                                              |
| entries   | dictionary | Has hashtags, videos, photos, urls keys. Each one's value is list|

### → function **get_trends()** -> list
You can get the Trends of your area simply by calling `get_trends()`. It will return a list of strings.

```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19)
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import get_trends
>>> get_trends()
['#WHUTOT', '#ARSSOU', 'West Ham', '#AtalantaJuve', '#バビロニア', '#おっさんずラブinthasky', 'Southampton', 'Valverde', '#MMKGabAndMax', '#23NParoNacional']
```

### → class **Profile(username: str)** -> class instance
You can get personal information of a profile, like birthday and biography if exists and public. This class takes username parameter. And returns itself. Access informations with class variables.


```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19)
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import Profile
>>> profile = Profile('bugraisguzar')
>>> profile.location
'Istanbul'
>>> profile.name
'Buğra İşgüzar'
>>> profile.username
'bugraisguzar'
```

#### → **.to_dict()** -> dict

**to_dict** is a method of *Profile* class. Returns profile datas as Python dictionary.

```python
Python 3.7.3 (default, Mar 26 2019, 21:43:19)
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from twitter_scraper import Profile
>>> profile = Profile("bugraisguzar")
>>> profile.to_dict()
{'name': 'Buğra İşgüzar', 'username': 'bugraisguzar', 'birthday': None, 'biography': 'geliştirici@peptr', 'website': 'bisguzar.com', 'profile_photo': 'https://pbs.twimg.com/profile_images/1199305322474745861/nByxOcDZ_400x400.jpg', 'banner_photo': 'https://pbs.twimg.com/profile_banners/1019138658/1555346657/1500x500', 'likes_count': 2512, 'tweets_count': 756, 'followers_count': 483, 'following_count': 255, 'is_verified': False, 'is_private': False, user_id: "1019138658"}
```

## Contributing to twitter-scraper
To contribute to twitter-scraper, follow these steps:

1. Fork this repository.
2. Create a branch with clear name: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

* @kennethreitz (author)
* @bisguzar (maintainer)
* @lionking6792
* @ozanbayram
* @sean-bailey
* @xeliot


## Contact
If you want to contact me you can reach me at [@bugraisguzar](https://twitter.com/bugraisguzar).


## License
This project uses the following license: [MIT](https://github.com/bisguzar/twitter-scraper/blob/master/LICENSE).
